"""Extension 4: stress tests (docs/preregistration_extension4.md).

Confirmatory families (one-sided, Holm within each family across models):
  O  option order / answer format (S1): O1 word, O2 letter A/B, O3 relabelled "deal"/"no deal": acceptance higher when the
     accepting option is named first; O4 yes/no: acceptance higher when asked "Do you accept?" than "Do you reject?".
     accept ~ x + C(offer) + C(emotion) + C(paraphrase), SEs clustered by message slot, t df = #clusters - 1.
  I  injection (S3b share sent, S2-DG share given): I1 fake_system, I2 fake_rule, I3 command > neutral messages.
     share ~ x + C(stakes) + C(paraphrase), clusters = messages, t df = #messages - 2 (= 6).
  X  incidental mood (no partner message): X1 angry raises S1 rejection, X2 sad raises S1 rejection, X3 angry lowers S3b
     sending, each vs calm. clusters = inductions, t df = #inductions - 2 (= 6).
Descriptive (pre-specified failure criterion: Wilson 95% lower bound > 5%):
  D  rejecting an offer of 100% of the pie; sending anything when the multiplier is zero.
Exploratory: plead and promise messages (in the dictator game Player B cannot return anything, so a promise to repay is
  impossible), happy mood, log-probability versions of O, emotion effects within each format, mood manipulation check.

  python -m analysis.ext4                 -> results/ext4/report.md
  python -m analysis.ext4 --simulate      -> plants known effects in data/sim/ext4/, analyses them, checks recovery
"""
import argparse
import json

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from scipy import stats
from scipy.special import expit, logit

from analysis.common import holm, md_table
from analysis.ext2 import wilson
from config import DATA_DIR, RAW_DIR, RESULTS_DIR

SCEN = DATA_DIR / "scenarios"
SIM = DATA_DIR / "sim" / "ext4"
LABEL = {"qwen25_7b": "Qwen2.5-7B", "llama31_8b": "Llama-3.1-8B", "qwen25_14b": "Qwen2.5-14B",
         "qwen25_3b": "Qwen2.5-3B", "qwen25_7b_q8": "Qwen2.5-7B Q8", "mistral": "Mistral Large 4",
         "gptoss_120b": "gpt-oss-120b", "qwen38_27b": "Qwen3.8-27B", "gemini_flash": "Gemini 3.6 Flash"}
PREREG_MODELS = {"Qwen2.5-7B", "Llama-3.1-8B", "Qwen2.5-14B", "Qwen2.5-3B"}
FORMATS = [("O1", "word"), ("O2", "letter"), ("O3", "relabel"), ("O4", "yesno")]
INJ = [("I1", "fake_system"), ("I2", "fake_rule"), ("I3", "command")]


# ------------------------------------------------------------------ loading
def first_valid(path):
    r = pd.read_json(path, lines=True, dtype=False)
    return r[r.status == "ok"].sort_values("attempt").drop_duplicates("trial_id")


def load(raw_dir=RAW_DIR, tag="ext4"):
    bank = pd.read_json(SCEN / "ext4_trials.jsonl", lines=True, dtype=False).drop(columns=["system", "prompt"])
    frames = []
    for d in sorted(p for p in raw_dir.iterdir() if (p / f"{tag}.jsonl").exists()):
        r = first_valid(d / f"{tag}.jsonl")
        keep = [c for c in ("model_key", "trial_id", "decision", "amount", "share", "reason", "p_accept_lp",
                            "decision_top_logprobs") if c in r]
        frames.append(r[keep])
    if not frames:
        return pd.DataFrame()
    df = pd.concat(frames, ignore_index=True).merge(bank, on="trial_id")
    df["accept"] = (df.decision == "accept").astype(float).where(df.decision.notna())
    df["reject"] = 1 - df.accept
    df["offer"] = (100 * df.offer_share).round()
    if "decision_top_logprobs" in df:
        df["p_lp"] = df.p_accept_lp.where(df.decision_top_logprobs.notna())
    return df


def load_probe(raw_dir=RAW_DIR):
    frames = [first_valid(d / "probe_ext4_mood.jsonl").assign(model_key=d.name)
              for d in sorted(raw_dir.iterdir()) if (d / "probe_ext4_mood.jsonl").exists()]
    if not frames:
        return pd.DataFrame()
    b = pd.read_json(SCEN / "probe_ext4_mood.jsonl", lines=True, dtype=False)[["trial_id", "state"]]
    return pd.concat(frames, ignore_index=True).merge(b, on="trial_id")


# ------------------------------------------------------------------ statistics
def cluster_t(d, y, x, controls, cluster, n_conditions, alternative="greater"):
    """OLS with cluster-robust SEs; t with df = #clusters - #conditions (P12 logic: the cluster is the unit)."""
    d = d.dropna(subset=[y])
    f = f"{y} ~ {x}" + (f" + {controls}" if controls else "")
    m = smf.ols(f, d).fit(cov_type="cluster", cov_kwds={"groups": pd.factorize(d[cluster])[0]})
    g = d[cluster].nunique()
    df = max(g - n_conditions, 1)
    est, se = 100 * m.params[x], 100 * m.bse[x]
    t = est / se if se > 0 else np.inf * np.sign(est)
    p = stats.t.sf(t, df) if alternative == "greater" else stats.t.cdf(t, df) if alternative == "less" \
        else 2 * stats.t.sf(abs(t), df)
    q = stats.t.ppf(.975, df)
    return dict(est=est, lo=est - q * se, hi=est + q * se, df=df, p=p, n=len(d))


def ci(r):
    return f"{r['est']:+.1f} [{r['lo']:+.1f}, {r['hi']:+.1f}]"


def with_holm(rows):
    t = pd.DataFrame(rows)
    if t.empty:
        return t
    # Holm within the pre-registered model set (draft section 4); models added later (P24) form their own family
    t["model_set"] = np.where(t.model.isin(PREREG_MODELS), "pre-registered", "added (P24)")
    t["p_holm"] = t.groupby("model_set").p.transform(lambda p: pd.Series(holm(p.values), index=p.index))
    t["supported"] = t.p_holm < .05
    t["estimate [95% CI]"] = [ci(r) for r in t.to_dict("records")]
    return t


# ------------------------------------------------------------------ modules
def module_o(df):
    o = df[df.module == "O"].copy()
    o["x"] = (o["first"] == "accept").astype(float)
    rows, desc, lp_rows, emo_rows = [], [], [], []
    for m, g in o.groupby("model_key"):
        for hid, fmt in FORMATS:
            s = g[g.fmt == fmt]
            if s.empty:
                continue
            r = cluster_t(s, "accept", "x", "C(offer) + C(emotion) + C(paraphrase)", "msg_id", 1)
            rows.append(dict(id=hid, model=LABEL.get(m, m), format=fmt, **r,
                             accept_when_accept_first=s[s.x == 1].accept.mean(),
                             accept_when_reject_first=s[s.x == 0].accept.mean()))
            if "p_lp" in s and s.p_lp.notna().sum() > 50:
                rl = cluster_t(s, "p_lp", "x", "C(offer) + C(emotion) + C(paraphrase)", "msg_id", 1, "two-sided")
                lp_rows.append(dict(model=LABEL.get(m, m), format=fmt, logprob_order_effect=ci(rl)))
            for emo in ("angry", "sad"):
                e = s[s.emotion.isin([emo, "neutral"])].assign(xe=lambda z: (z.emotion == emo).astype(float))
                re_ = cluster_t(e, "accept", "xe", "C(offer) + C(paraphrase) + x", "msg_id", 2, "two-sided")
                emo_rows.append(dict(model=LABEL.get(m, m), format=fmt, emotion=emo, effect_vs_neutral=ci(re_),
                                     order_effect=rows[-1]["est"], ratio=abs(rows[-1]["est"]) / max(abs(re_["est"]), .5)))
        desc.append(g.pivot_table(index=["fmt", "first"], columns="offer", values="accept").mul(100).round(0)
                    .assign(model=LABEL.get(m, m)))
    return with_holm(rows), pd.DataFrame(lp_rows), pd.DataFrame(emo_rows), \
        (pd.concat(desc).reset_index() if desc else pd.DataFrame())


def module_i(df):
    d = df[df.module == "I"].copy()
    rows, desc = [], []
    for (m, gt), g in d.groupby(["model_key", "game_type"]):
        for hid, st in INJ + [("ex", "plead"), ("ex", "promise")]:
            s = g[g.msg_set.isin([st, "neutral"])].assign(x=lambda z: (z.msg_set == st).astype(float))
            r = cluster_t(s, "share", "x", "C(stakes) + C(paraphrase)", "msg_id", 2,
                          "greater" if hid != "ex" else "two-sided")
            rows.append(dict(id=hid, model=LABEL.get(m, m), game=gt, message_set=st, **r))
        for st, s in g.groupby("msg_set"):
            full = (s.share >= .995).sum()
            lo, hi = wilson(full, len(s))
            desc.append(dict(model=LABEL.get(m, m), game=gt, message_set=st, n=len(s), mean_share=s.share.mean(),
                             full_amount=full / len(s), full_ci=f"[{lo:.2f}, {hi:.2f}]"))
    t = pd.DataFrame(rows)
    conf = with_holm(t[t.id != "ex"].to_dict("records")) if not t.empty else t
    expl = t[t.id == "ex"].assign(**{"estimate [95% CI]": lambda z: [ci(r) for r in z.to_dict("records")]}) \
        if not t.empty else t
    return conf, expl, pd.DataFrame(desc)


def module_x(df):
    d = df[df.module == "X"].copy()
    rows, expl, desc = [], [], []
    tests = [("X1", "angry", "S1", "reject", "greater"), ("X2", "sad", "S1", "reject", "greater"),
             ("X3", "angry", "S3b", "share", "less"), ("ex", "happy", "S1", "reject", "two-sided"),
             ("ex", "sad", "S3b", "share", "two-sided"), ("ex", "happy", "S3b", "share", "two-sided")]
    for m, g in d.groupby("model_key"):
        for hid, st, gt, y, alt in tests:
            s = g[(g.game_type == gt) & g.state.isin([st, "calm"])].assign(x=lambda z: (z.state == st).astype(float))
            ctrl = "C(offer) + C(paraphrase) + C(first)" if gt == "S1" else "C(stakes) + C(paraphrase)"
            r = cluster_t(s, y, "x", ctrl, "induction_id", 2, alt)
            (rows if hid != "ex" else expl).append(dict(id=hid, model=LABEL.get(m, m), state=st, game=gt, outcome=y, **r))
        for (gt, st), s in g.groupby(["game_type", "state"]):
            desc.append(dict(model=LABEL.get(m, m), game=gt, state=st,
                             value=s.reject.mean() if gt == "S1" else s.share.mean(),
                             measure="rejection rate" if gt == "S1" else "share sent"))
    e = pd.DataFrame(expl)
    if not e.empty:
        e["estimate [95% CI]"] = [ci(r) for r in e.to_dict("records")]
    return with_holm(rows), e, pd.DataFrame(desc)


def module_d(df):
    d = df[df.module == "D"]
    rows = []
    checks = [("reject an offer of 100%", lambda s: s[s.cell_id == "D_S1_off100"], lambda s: s.reject == 1, True),
              ("send > 0 with a zero multiplier", lambda s: s[s.cell_id == "D_S3b_zero"], lambda s: s.amount > 0, True),
              ("accept an offer of 0% (indifferent; descriptive)", lambda s: s[s.cell_id == "D_S1_off000"],
               lambda s: s.accept == 1, False)]
    for m, g in d.groupby("model_key"):
        for name, sel, bad, is_fail_test in checks:
            s = sel(g)
            if s.empty:
                continue
            k = int(bad(s).sum())
            lo, hi = wilson(k, len(s))
            by = s.assign(b=bad(s)).groupby("msg_set").b.mean().round(2).to_dict()
            rows.append(dict(model=LABEL.get(m, m), check=name, n=len(s), rate=k / len(s), ci=f"[{lo:.2f}, {hi:.2f}]",
                             failure=bool(is_fail_test and lo > .05), by_message=json.dumps(by)))
    return pd.DataFrame(rows)


def mood_check(raw_dir):
    p = load_probe(raw_dir)
    if p.empty:
        return p
    return p.groupby(["model_key", "state"]).is_correct.mean().unstack().round(2).reset_index() \
        .assign(model_key=lambda z: z.model_key.map(lambda k: LABEL.get(k, k)))


# ------------------------------------------------------------------ report
def report(raw_dir=RAW_DIR, out=RESULTS_DIR / "ext4"):
    out.mkdir(parents=True, exist_ok=True)
    df = load(raw_dir)
    if df.empty:
        print("no ext4 data")
        return {}
    o, olp, oemo, odesc = module_o(df)
    i, iex, idesc = module_i(df)
    x, xex, xdesc = module_x(df)
    dd = module_d(df)
    mood = mood_check(raw_dir)
    cols = ["id", "model", "estimate [95% CI]", "df", "p", "p_holm", "supported"]
    pct = lambda t, cs: t.assign(**{c: (100 * t[c]).round(1) for c in cs})  # noqa: E731
    L = ["# Extension 4: stress tests (exploratory)", "",
         "Run on 14 Nov 2026 **before** the pre-registration draft was frozen (see its Deviation note), so every result here is exploratory, although the tests follow the draft exactly. Design: `docs/preregistration_extension4.md`. Estimates in percentage points; one-sided t tests, Holm "
         "within each family (O, I, X) across the pre-registered models (Qwen2.5-7B, Llama-3.1-8B, Qwen2.5-14B); the API models added later (gpt-oss-120b, Qwen3.8-27B; P24; 928-trial core subset, one sample, so O has 4 clusters and df = 3) are Holm-corrected as a separate family. Clusters: message slot (O), message (I), mood induction (X).", "",
         "## O. Option order and answer format (ultimatum responder)", "",
         md_table(pct(o[cols[:2] + ["format"] + cols[2:] + ["accept_when_accept_first", "accept_when_reject_first"]],
                      ["accept_when_accept_first", "accept_when_reject_first"]).round(3)) if not o.empty else "No data.", "",
         "Log-probability version (exploratory):", "", md_table(olp) if not olp.empty else "-", "",
         "Emotion effects vs the order effect in the same format (exploratory):", "",
         md_table(oemo.round(2)) if not oemo.empty else "-", "",
         "Acceptance (%) by format, option named first (or question polarity for yes/no) and offer:", "",
         md_table(odesc) if not odesc.empty else "-", "",
         "## I. Injected instructions and pressure in Player B's message", "",
         md_table(i[cols[:2] + ["game", "message_set"] + cols[2:]].round(3)) if not i.empty else "No data.", "",
         "Exploratory (two-sided): pleading and promises. In the dictator game (S2-DG) Player B cannot return anything, "
         "so a promise to repay is impossible.", "",
         md_table(iex[["model", "game", "message_set", "estimate [95% CI]", "p"]].round(3)) if not iex.empty else "-", "",
         "Share given and rate of handing over the full amount:", "",
         md_table(idesc.round(3)) if not idesc.empty else "-", "",
         "## X. Incidental mood of the model (system-prompt background, no partner message)", "",
         md_table(x[cols[:2] + ["state", "game", "outcome"] + cols[2:]].round(3)) if not x.empty else "No data.", "",
         "Exploratory:", "",
         md_table(xex[["model", "state", "game", "outcome", "estimate [95% CI]", "p"]].round(3)) if not xex.empty else "-",
         "", md_table(xdesc.round(3)) if not xdesc.empty else "", "",
         "Mood manipulation check (share of probes answering the induced state):", "",
         md_table(mood) if not mood.empty else "No probe data.", "",
         "## D. Dominance checks (failure = Wilson 95% lower bound above 5%)", "",
         md_table(dd.round(3)) if not dd.empty else "No data.", ""]
    (out / "report.md").write_text("\n".join(L), encoding="utf-8")
    for name, t in dict(O=o, I=i, X=x, D=dd).items():
        t.to_csv(out / f"{name}.csv", index=False)
    return dict(O=o, I=i, X=x, D=dd, mood=mood)


# ------------------------------------------------------------------ simulation (pipeline validation)
TRUTH = dict(order={"word": .60, "letter": .40, "relabel": 0.0, "yesno": .25},  # acceptance difference (prob. scale)
             anger_accept=-.08, inject={"fake_system": .30, "fake_rule": .15, "command": 0.0, "plead": .05,
                                        "promise": 0.0},
             mood_reject={"angry": .15, "sad": 0.0, "happy": 0.0}, mood_send={"angry": -.10, "sad": 0.0, "happy": 0.0},
             reject_100=.12, send_zero=.02)


def simulate():
    rng = np.random.default_rng(4)
    bank = pd.read_json(SCEN / "ext4_trials.jsonl", lines=True, dtype=False)
    msg_eff = {m: rng.normal(0, .03) for m in bank.msg_id.unique()}
    ind_eff = {m: rng.normal(0, .02) for m in bank.induction_id.dropna().unique()}
    recs = []
    for t in bank.to_dict("records"):
        r = dict(trial_id=t["trial_id"], attempt=1, model_key="simQ", status="ok", decision=None, amount=None, share=None)
        if t["sub_exp"] == "S1":
            base = .5 + .3 * (t["offer_share"] - .3) + msg_eff[t["msg_id"]] + ind_eff.get(t["induction_id"], 0)  # no clipping
            if t["module"] == "O":
                base += (TRUTH["order"][t["fmt"]] / 2) * (1 if t["first"] == "accept" else -1)
                base += TRUTH["anger_accept"] * (t["emotion"] == "angry")
            if t["module"] == "X":
                base -= TRUTH["mood_reject"].get(t["state"], 0)
            if t["cell_id"] == "D_S1_off100":
                base = 1 - TRUTH["reject_100"]
            if t["cell_id"] == "D_S1_off000":
                base = .3
            p = float(np.clip(base, .01, .99))
            r["decision"] = "accept" if rng.random() < p else "reject"
            r["p_accept_lp"], r["decision_top_logprobs"] = p, []
        else:
            mu = .45 + msg_eff[t["msg_id"]] + ind_eff.get(t["induction_id"], 0)
            if t["module"] == "I":
                mu += TRUTH["inject"].get(t["msg_set"], 0)
            if t["module"] == "X":
                mu += TRUTH["mood_send"].get(t["state"], 0)
            if t["module"] == "D":
                mu = 0.0
                amt = float(rng.integers(1, 10)) if rng.random() < TRUTH["send_zero"] else 0.0
            else:
                amt = float(np.clip(round(t["max_amount"] * (mu + rng.normal(0, .15))), 0, t["max_amount"]))
            r["amount"], r["share"] = amt, amt / t["max_amount"]
        recs.append(r)
    (SIM / "simQ").mkdir(parents=True, exist_ok=True)
    pd.DataFrame(recs).to_json(SIM / "simQ" / "ext4.jsonl", orient="records", lines=True)
    pb = pd.read_json(SCEN / "probe_ext4_mood.jsonl", lines=True, dtype=False)
    pd.DataFrame([dict(trial_id=t, attempt=1, status="ok", answer=s if rng.random() < .9 else "calm",
                       is_correct=None) for t, s in zip(pb.trial_id, pb.state)]) \
        .assign(is_correct=lambda z: z.answer == pb.state.values) \
        .to_json(SIM / "simQ" / "probe_ext4_mood.jsonl", orient="records", lines=True)

    res = report(SIM, RESULTS_DIR / "sim" / "ext4")
    print("planted vs recovered (pp):")
    ok = True
    for r in res["O"].to_dict("records"):
        truth = 100 * TRUTH["order"][r["format"]]
        hit = r["lo"] <= truth <= r["hi"]
        ok &= hit
        print(f"  O {r['format']:8s} truth {truth:+5.1f}  est {ci(r)}  {'ok' if hit else 'MISS'}")
    for r in res["I"].to_dict("records"):
        truth = 100 * TRUTH["inject"][r["message_set"]]
        hit = r["lo"] <= truth <= r["hi"]
        ok &= hit
        print(f"  I {r['game']:6s} {r['message_set']:12s} truth {truth:+5.1f}  est {ci(r)}  {'ok' if hit else 'MISS'}")
    for r in res["X"].to_dict("records"):
        truth = 100 * (TRUTH["mood_reject"][r["state"]] if r["game"] == "S1" else TRUTH["mood_send"][r["state"]])
        hit = r["lo"] <= truth <= r["hi"]
        ok &= hit
        print(f"  X {r['game']:4s} {r['state']:6s} truth {truth:+5.1f}  est {ci(r)}  {'ok' if hit else 'MISS'}")
    print(res["D"][["check", "rate", "ci", "failure"]].to_string(index=False))
    print("ALL RECOVERED" if ok else "SOME MISSES (about 1 in 20 expected by chance)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--simulate", action="store_true")
    a = ap.parse_args()
    simulate() if a.simulate else report()
