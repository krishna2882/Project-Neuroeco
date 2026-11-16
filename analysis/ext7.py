"""Extension 7 (docs/preregistration_extension7.md): pre-registered generalisation of the extension-4 and extension-5
findings to new model families (family G), and what kind of effect the incidental angry mood is (family N).

  python -m analysis.ext7             -> results/ext7/report.md, N.csv, N_pooled.csv, G_models.csv, G_pooled.csv
  python -m analysis.ext7 --simulate  -> validation of module N and of the pooled tests on simulated models

Per model: linear probability models with cluster-robust SEs (clusters = background paragraphs or events), as before.
Across models (the confirmatory generalisation tests): each model contributes one estimate, and the mean over models is
tested with a one-sample t test (df = number of models - 1). The model is the unit, so the inference is about open-weight
models like these, not about more samples from one model.
"""
import argparse

import numpy as np
import pandas as pd
from scipy import stats

from analysis import ext4, ext5
from analysis.common import holm, md_table
from analysis.ext4 import LABEL, ci, cluster_t, first_valid
from config import DATA_DIR, RAW_DIR, RESULTS_DIR

SCEN = DATA_DIR / "scenarios"
SIM = DATA_DIR / "sim" / "ext7"
NEW_MODELS = ["gemma3_12b", "gemma3_4b", "mistral_nemo_12b", "phi4_14b", "granite33_8b", "llama32_3b"]
LABEL.update({"gemma3_12b": "Gemma-3-12B", "gemma3_4b": "Gemma-3-4B", "mistral_nemo_12b": "Mistral-Nemo-12B",
              "phi4_14b": "Phi-4-14B", "granite33_8b": "Granite-3.3-8B", "llama32_3b": "Llama-3.2-3B"})
CTRL = "C(offer) + C(paraphrase) + accept_first"


# ------------------------------------------------------------------ module N
def load_n(raw_dir=RAW_DIR):
    bank = pd.read_json(SCEN / "ext7_trials.jsonl", lines=True, dtype=False).drop(columns=["system", "prompt"])
    frames = [first_valid(d / "ext7.jsonl")[["model_key", "trial_id", "decision"]]
              for d in sorted(raw_dir.iterdir()) if (d / "ext7.jsonl").exists()]
    if not frames:
        return pd.DataFrame()
    df = pd.concat(frames, ignore_index=True).merge(bank, on="trial_id")
    df["reject"] = (df.decision == "reject").astype(float).where(df.decision.notna())
    df["offer"] = (100 * df.offer_share.astype(float)).round()
    df["accept_first"] = (df["first"] == "accept").astype(float)
    return df


def contrast(g, a, b, cluster, n_conditions, alternative):
    """Rejection in condition a minus condition b (pp)."""
    s = g[g.cond.isin([a, b])].assign(x=lambda q: (q.cond == a).astype(float))
    return cluster_t(s, "reject", "x", CTRL, cluster, n_conditions, alternative)


N_TESTS = [  # id, label, a, b, cluster, n_conditions, alternative
    ("N1", "event only - calm (the feeling is inferred)", "event_only", "calm", "induction_id", 2, "greater"),
    ("N2", "label only - calm (the feeling without a cause)", "label_only", "calm", "induction_id", 2, "greater"),
    ("N3", "own anger - another person's anger", "full", "other_person", "event_id", 1, "greater"),
    ("N4", "furious - slightly annoyed (same event)", "full", "mild", "event_id", 1, "greater"),
]
N_EXPL = [("full - calm (replication)", "full", "calm", "induction_id", 2), ("mild - calm", "mild", "calm", "induction_id", 2),
          ("another person's anger - calm", "other_person", "calm", "induction_id", 2),
          ("full - event only (what the stated feeling adds)", "full", "event_only", "event_id", 1)]


def module_n(df):
    conf, expl, desc = [], [], []
    for m, g in df.groupby("model_key"):
        lab = dict(model_key=m, model=LABEL.get(m, m))
        for hid, test, a, b, cl, nc, alt in N_TESTS:
            conf.append(dict(id=hid, **lab, test=test, **contrast(g, a, b, cl, nc, alt)))
        for test, a, b, cl, nc in N_EXPL:
            expl.append(dict(**lab, test=test, **contrast(g, a, b, cl, nc, "two-sided")))
        desc.append(dict(**lab, **(100 * g.groupby("cond").reject.mean()).round(1).to_dict()))
    t = pd.DataFrame(conf)
    if not t.empty:
        t["p_holm"] = holm(t.p.values)
        t["supported"] = t.p_holm < .05
        t["estimate [95% CI]"] = [ci(r) for r in t.to_dict("records")]
    e = pd.DataFrame(expl)
    if not e.empty:
        e["estimate [95% CI]"] = [ci(r) for r in e.to_dict("records")]
    return t, e, pd.DataFrame(desc)


def mood_check(raw_dir):
    frames = [first_valid(d / "probe_ext7_mood.jsonl").assign(model_key=d.name)
              for d in sorted(raw_dir.iterdir()) if (d / "probe_ext7_mood.jsonl").exists()]
    if not frames:
        return pd.DataFrame()
    b = pd.read_json(SCEN / "probe_ext7_mood.jsonl", lines=True, dtype=False)[["trial_id", "state"]]
    p = pd.concat(frames, ignore_index=True).merge(b, on="trial_id")
    p["says_angry"] = (p.answer == "angry").astype(float)
    t = p.groupby(["model_key", "state"]).says_angry.mean().unstack().round(2).reset_index()
    return t.assign(model_key=t.model_key.map(lambda k: LABEL.get(k, k)))


# ------------------------------------------------------------------ pooled tests over models
def pooled(est, alternative, mu0=0.0):
    x = np.asarray([v for v in est if v is not None and not np.isnan(v)], float)
    k = len(x)
    if k < 2:
        return dict(k=k, mean=float(x.mean()) if k else np.nan, lo=np.nan, hi=np.nan, p=np.nan, same_sign=np.nan)
    se = x.std(ddof=1) / np.sqrt(k)
    q = stats.t.ppf(.975, k - 1)
    p = stats.ttest_1samp(x, mu0, alternative=alternative).pvalue if se > 0 else float(not (
        (x.mean() > mu0) if alternative == "greater" else (x.mean() < mu0)))
    sign = (x > mu0).sum() if alternative == "greater" else (x < mu0).sum()
    return dict(k=k, mean=x.mean(), lo=x.mean() - q * se, hi=x.mean() + q * se, p=p, same_sign=f"{sign}/{k}")


def pool_table(per_model, specs):
    """per_model: rows with id, model_key, est. specs: [(id, label, alternative, mu0)]."""
    rows = []
    for hid, label, alt, mu0 in specs:
        est = per_model[per_model.id == hid].est.values
        rows.append(dict(id=hid, test=label, **pooled(est, alt, mu0)))
    t = pd.DataFrame(rows)
    ok = t.p.notna()
    t.loc[ok, "p_holm"] = holm(t.loc[ok, "p"].values)
    t["supported"] = t.p_holm < .05
    t["mean [95% CI]"] = [f"{r.mean:+.1f} [{r.lo:+.1f}, {r.hi:+.1f}]" for r in t.itertuples()]
    return t


# ------------------------------------------------------------------ family G: new models on the frozen banks
G_SPECS = [  # id, label, alternative, null value (pp)
    ("G1", "fake SYSTEM notice raises the share handed over (vs neutral message)", "greater", 0),
    ("G2", "a 100% offer is rejected more than 5% of the time", "greater", 5),
    ("G3", "incidental anger raises rejection of unfair offers (no regulation)", "greater", 0),
    ("G4", "reappraisal shrinks the anger effect (vs filler)", "less", 0),
    ("G5", "suppression shrinks the anger effect (vs filler)", "less", 0),
    ("G6", "the reminder defence lowers the share handed over after injection", "less", 0),
    ("G7", "anger raises MAO* (share of the pie)", "greater", 0),
    ("G8", "anger lowers acceptance of offers above 50%", "less", 0),
]


def g_models(raw_dir=RAW_DIR, models=NEW_MODELS, n_boot=ext5.N_BOOT):
    rows, extra = [], []
    d4, d5 = ext4.load(raw_dir), ext5.load(raw_dir)
    d4 = d4[d4.model_key.isin(models)] if not d4.empty else d4
    d5 = d5[d5.model_key.isin(models)] if not d5.empty else d5
    if not d4.empty:
        for m, g in d4.groupby("model_key"):
            i = g[(g.module == "I") & g.msg_set.isin(["fake_system", "neutral"])] \
                .assign(x=lambda q: (q.msg_set == "fake_system").astype(float))
            r = cluster_t(i, "share", "x", "C(game_type) + C(stakes) + C(paraphrase)", "msg_id", 2, "greater")
            rows.append(dict(id="G1", model_key=m, est=r["est"], lo=r["lo"], hi=r["hi"]))
            rows.append(dict(id="G2", model_key=m, est=100 * g[g.cell_id == "D_S1_off100"].reject.mean()))
            fs = g[(g.module == "I") & (g.msg_set == "fake_system")]
            o = g[g.module == "O"].assign(x=lambda z: (z["first"] == "accept").astype(float))
            fmt = {f: cluster_t(o[o.fmt == f], "accept", "x", "C(offer) + C(emotion) + C(paraphrase)", "msg_id", 1,
                                "two-sided") for f in ("word", "letter", "relabel", "yesno")}
            big = max(fmt, key=lambda f: abs(fmt[f]["est"]))
            extra.append(dict(model_key=m, full_handover_fake_system=100 * (fs.share >= .995).mean(),
                              send_destroyed_money=100 * (g[g.cell_id == "D_S3b_zero"].amount > 0).mean(),
                              largest_format_effect=fmt[big]["est"], largest_format=big, format_p=fmt[big]["p"]))
    if not d5.empty:
        r, rex, _ = ext5.module_r(d5)
        p, _, pdesc = ext5.module_p(d5)
        f, _ = ext5.module_f(d5, n_boot)
        for hid, src, key in [("G3", r, "R0"), ("G4", r, "R1"), ("G6", p, "P2"), ("G7", f, "F1")]:
            for q in src[src.id == key].to_dict("records"):
                rows.append(dict(id=hid, model_key=q["model_key"], est=q["est"], lo=q["lo"], hi=q["hi"]))
        for q in rex[rex.test == "anger effect: suppression - filler"].to_dict("records"):
            rows.append(dict(id="G5", model_key=q["model_key"], est=q["est"], lo=q["lo"], hi=q["hi"]))
        for q in f.to_dict("records"):
            rows.append(dict(id="G8", model_key=q["model_key"],
                             est=100 * (q["accept_above_half_angry"] - q["accept_above_half_calm"])))
        still = pdesc[pdesc.message_set.isin(ext5.INJ) & (pdesc.defence != "none")].groupby("model_key").still_breaks.mean()
        for m, v in still.items():
            extra.append(dict(model_key=m, injection_sets_still_breaking_under_defence=100 * v))
    t = pd.DataFrame(rows)
    e = pd.DataFrame(extra)
    if not e.empty:
        e = e.groupby("model_key").first().reset_index()
    return t, e


# ------------------------------------------------------------------ report
N_SPECS = [(hid, test, alt, 0) for hid, test, _, _, _, _, alt in N_TESTS]


def report(raw_dir=RAW_DIR, out=RESULTS_DIR / "ext7", n_boot=ext5.N_BOOT, with_g=True):
    out.mkdir(parents=True, exist_ok=True)
    show = lambda t, c=None: md_table((t[c] if c else t).round(3)) if not t.empty else "No data."  # noqa: E731
    res = {}
    L = ["# Extension 7: generalisation to new model families, and what kind of effect the mood is", "",
         "Design and hypotheses: `docs/preregistration_extension7.md`. Estimates in percentage points. Pooled tests: one "
         "estimate per model, one-sample t test over models (one-sided), Holm within each family.", ""]
    if with_g:
        gm, ge = g_models(raw_dir, n_boot=n_boot)
        if not gm.empty:
            gp = pool_table(gm, G_SPECS)
            wide = gm.pivot(index="model_key", columns="id", values="est").round(1).reset_index()
            wide.insert(0, "model", wide.model_key.map(lambda k: LABEL.get(k, k)))
            L += ["## G. The extension-4 and extension-5 findings in models from new developers", "",
                  show(gp, ["id", "test", "k", "mean [95% CI]", "same_sign", "p", "p_holm", "supported"]), "",
                  "Per-model estimates (pp):", "", show(wide.drop(columns="model_key")), "",
                  "Descriptive, per model:", "", show(ge.assign(model=ge.model_key.map(lambda k: LABEL.get(k, k)))), ""]
            gm.to_csv(out / "G_models.csv", index=False)
            gp.to_csv(out / "G_pooled.csv", index=False)
            res.update(G=gp, G_models=gm)
    df = load_n(raw_dir)
    if not df.empty:
        n, nex, ndesc = module_n(df)
        npool = pool_table(n.rename(columns={}), N_SPECS)
        L += ["## N. What kind of effect is the angry mood? (ultimatum responder, offers of 10% and 30%)", "",
              "Across models:", "", show(npool, ["id", "test", "k", "mean [95% CI]", "same_sign", "p", "p_holm", "supported"]), "",
              "Per model (Holm across all models and tests):", "",
              show(n, ["id", "model", "test", "estimate [95% CI]", "df", "p", "p_holm", "supported"]), "",
              "Rejection (%) by condition:", "", show(ndesc.drop(columns="model_key")), "",
              "Exploratory (two-sided):", "", show(nex, ["model", "test", "estimate [95% CI]", "p"]), "",
              "Mood check: share answering \"angry\":", "", show(mood_check(raw_dir)), ""]
        n.to_csv(out / "N.csv", index=False)
        npool.to_csv(out / "N_pooled.csv", index=False)
        res.update(N=n, N_pooled=npool)
    (out / "report.md").write_text("\n".join(L), encoding="utf-8")
    print(out / "report.md")
    return res


# ------------------------------------------------------------------ simulation (module N and the pooled tests)
TRUTH = {"calm": 0.0, "full": .30, "event_only": .20, "label_only": .25, "other_person": .05, "mild": .10}


def simulate(k_models=6):
    rng = np.random.default_rng(7)
    bank = pd.read_json(SCEN / "ext7_trials.jsonl", lines=True, dtype=False)
    truth_m = {}
    for j in range(k_models):
        key = f"sim{j}"
        shift = {c: v + (rng.normal(0, .04) if c != "calm" else 0) for c, v in TRUTH.items()}  # model-specific effects
        truth_m[key] = shift
        item = {i: rng.normal(0, .03) for i in bank.induction_id.unique()}
        recs = []
        for t in bank.to_dict("records"):
            p = .35 - .5 * (t["offer_share"] - .2) + item[t["induction_id"]] + shift[t["cond"]] \
                + .10 * (.5 - (t["first"] == "accept"))
            recs.append(dict(trial_id=t["trial_id"], attempt=1, model_key=key, status="ok",
                             decision="reject" if rng.random() < p else "accept"))
        (SIM / key).mkdir(parents=True, exist_ok=True)
        pd.DataFrame(recs).to_json(SIM / key / "ext7.jsonl", orient="records", lines=True)
    res = report(SIM, RESULTS_DIR / "sim" / "ext7", with_g=False)
    pair = {"N1": ("event_only", "calm"), "N2": ("label_only", "calm"), "N3": ("full", "other_person"), "N4": ("full", "mild")}
    hits = 0
    for r in res["N"].to_dict("records"):
        a, b = pair[r["id"]]
        tr = 100 * (truth_m[r["model_key"]][a] - truth_m[r["model_key"]][b])
        hits += r["lo"] <= tr <= r["hi"]
    print(f"per-model: {hits}/{len(res['N'])} planted effects inside their 95% CI (about 95% expected)")
    ok = True
    for r in res["N_pooled"].to_dict("records"):
        a, b = pair[r["id"]]
        tr = 100 * np.mean([truth_m[m][a] - truth_m[m][b] for m in truth_m])
        hit = r["lo"] <= tr <= r["hi"]
        ok &= hit
        print(f"  pooled {r['id']} truth {tr:+5.1f}  est {r['mean [95% CI]']}  p_holm {r['p_holm']:.4f}  {'ok' if hit else 'MISS'}")
    print("POOLED ALL RECOVERED" if ok else "POOLED: SOME MISSES")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--simulate", action="store_true")
    a = ap.parse_args()
    simulate() if a.simulate else report()
