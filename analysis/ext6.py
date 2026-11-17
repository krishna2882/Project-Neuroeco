"""Extension 6: probing and steering (docs/preregistration_extension6.md). Reads data/mech/<key>/*.csv.

  python -m analysis.ext6            -> results/ext6/report.md, tests.csv, probe.csv, sweep.csv
  python -m analysis.ext6 --dev      -> the same for development runs (keys starting with dev_; results/ext6_dev/, not reported)

Steering statistic: for each direction, the slope of the decision on the steering strength k (k = 0 is the unsteered
model), fitted per target prompt and averaged over prompts. The anger direction's slope is compared with the slopes of
random directions of the same norm: p = (1 + #random at least as extreme in the predicted direction) / (1 + #random).
Ablation statistic: the anger effect on held-out messages (neutral - angry share sent) that remains when a direction is
projected out of every layer, compared in the same way with random directions.
A steering strength is used only if, under the anger direction, at least 90% of sampled amounts are valid (trust game) and
at least half of the next-token probability is on "accept"/"reject" (ultimatum).
"""
import argparse

import numpy as np
import pandas as pd

from analysis.common import holm, md_table
from analysis.ext4 import cluster_t
from config import DATA_DIR, RESULTS_DIR

MECH = DATA_DIR / "mech"
VALID = {"S3b": .90, "S1": .50}


def slopes(d, base):
    """Mean over prompts of the OLS slope of outcome on k, per direction (base = the k = 0 rows)."""
    out = {}
    b = base.set_index("prompt_id").outcome
    for name, g in d.groupby("direction"):
        w = g.pivot(index="prompt_id", columns="k", values="outcome")
        w.insert(0, 0.0, b.reindex(w.index))
        ks = np.array(w.columns, float)
        out[name] = float(np.nanmean([np.polyfit(ks, row, 1)[0] for row in w.values]))
    return out


def rank_p(x, null, tail):
    null = np.asarray(null)
    hits = (null <= x).sum() if tail == "less" else (null >= x).sum()
    return (1 + hits) / (1 + len(null))


def steering(s, layer):
    rows, extra = [], []
    s = s[s.layer == layer]
    for game, tail, hid, label in [("S3b", "less", "M1", "share sent"), ("S1", "greater", "M2", "P(reject)")]:
        g = s[s.game == game]
        base = g[g.direction == "none"]
        anger = g[g.direction == "anger"]
        ok = anger.groupby("k").valid.mean()
        keep = [k for k, v in ok.items() if v >= VALID[game]]
        g = g[g.k.isin(keep) & (g.direction != "none")]
        if not keep:
            rows.append(dict(id=hid, game=game, test=f"steering lowers {label}" if tail == "less" else f"steering raises {label}",
                             est=np.nan, p=1.0, note="no valid steering strength"))
            continue
        sl = slopes(g, base)
        rnd = [v for k, v in sl.items() if k.startswith("random")]
        rows.append(dict(id=hid, game=game, test=f"anger direction {'lowers' if tail == 'less' else 'raises'} {label}",
                         est=100 * sl["anger"], null_mean=100 * np.mean(rnd), null_lo=100 * np.quantile(rnd, .025),
                         null_hi=100 * np.quantile(rnd, .975), p=rank_p(sl["anger"], rnd, tail), n_random=len(rnd),
                         k_used=str(keep), baseline=100 * base.outcome.mean(),
                         at_max_k=100 * anger[anger.k == max(keep)].outcome.mean()))
        for name in ("sad", "happy", "own_anger"):
            if name in sl:
                extra.append(dict(game=game, direction=name, slope_pp_per_k=100 * sl[name],
                                  p_two_sided=min(1, 2 * min(rank_p(sl[name], rnd, "less"), rank_p(sl[name], rnd, "greater")))))
    return rows, extra


def ablation(ab):
    rows = []
    for game, hid in [("S3b", "M3"), ("S1", "ex")]:
        g = ab[ab.game == game]
        if g.empty:
            continue
        m = g.groupby(["direction", "emotion"]).outcome.mean().unstack()
        eff = (m["neutral"] - m["angry"]) if game == "S3b" else (m["angry"] - m["neutral"])  # the anger effect, positive
        rnd = eff[eff.index.str.startswith("random")]
        rows.append(dict(id=hid, game=game, test="ablating the anger direction shrinks the anger effect",
                         est=100 * eff["anger"], unablated=100 * eff["none"], null_mean=100 * rnd.mean(),
                         null_lo=100 * rnd.quantile(.025), null_hi=100 * rnd.quantile(.975),
                         p=rank_p(eff["anger"], rnd, "less"), n_random=len(rnd),
                         valid_anger=g[g.direction == "anger"].valid.mean()))
    return rows


def behaviour(b):
    rows = []
    m = b[(b.set == "msg") & b.emotion.isin(["angry", "neutral"])].assign(angry=lambda z: (z.emotion == "angry").astype(float))
    d = b[(b.set == "mood") & b.emotion.isin(["angry", "calm"])].assign(angry=lambda z: (z.emotion == "angry").astype(float))
    for data, name in [(m, "angry - neutral message"), (d, "angry - calm mood")]:
        for game in ("S3b", "S1"):
            g = data[data.game == game].dropna(subset=["outcome"])
            if g.angry.nunique() < 2:
                continue
            ctrl = " + ".join(f"C({c})" for c in ("paraphrase", "first") if g[c].nunique() > 1)  # dev runs subsample
            r = cluster_t(g, "outcome", "angry", ctrl, "source_id", 2, "two-sided")
            rows.append(dict(game=game, contrast=name, est=r["est"], lo=r["lo"], hi=r["hi"], p=r["p"],
                             baseline=100 * g[g.angry == 0].outcome.mean()))
    return rows


def main(dev=False):
    out = RESULTS_DIR / ("ext6_dev" if dev else "ext6")
    out.mkdir(parents=True, exist_ok=True)
    tests, extras, behs, probes, sweeps = [], [], [], [], []
    for d in sorted(p for p in MECH.iterdir() if (p / "meta.json").exists() and p.name.startswith("dev_") == dev):
        meta = pd.read_json(d / "meta.json", typ="series")
        s, ab = pd.read_csv(d / "steer.csv"), pd.read_csv(d / "ablate.csv")
        t, e = steering(s, meta.steer_layer)
        t += ablation(ab)
        t = pd.DataFrame(t).assign(model=d.name)
        conf = t.id.isin(["M1", "M2", "M3"])
        t.loc[conf, "p_holm"] = holm(t.loc[conf, "p"].values)
        t["supported"] = t.p_holm < .05
        tests.append(t)
        extras.append(pd.DataFrame(e).assign(model=d.name))
        behs.append(pd.DataFrame(behaviour(pd.read_csv(d / "behaviour.csv"))).assign(model=d.name))
        probes.append(pd.read_csv(d / "probe.csv").assign(model=d.name, steer_layer=meta.steer_layer))
        if not (d / "sweep.csv").exists():  # the exploratory sweep runs last and may still be running
            continue
        sw = pd.read_csv(d / "sweep.csv")
        base = s[s.direction == "none"]
        for (layer, game), g in sw.groupby(["layer", "game"]):
            sl = slopes(g, base[base.game == game])
            rnd = [v for k, v in sl.items() if k.startswith("random")]
            sweeps.append(dict(model=d.name, layer=layer, game=game, anger_slope=100 * sl["anger"],
                               random_min=100 * min(rnd), random_max=100 * max(rnd),
                               valid=g[g.direction == "anger"].valid.mean()))
    if not tests:
        print("no extension-6 runs found")
        return
    T, E, B, P, S = (pd.concat(x, ignore_index=True) if len(x) else pd.DataFrame() for x in
                     (tests, extras, behs, probes, [pd.DataFrame(sweeps)]))
    show = lambda t: md_table(t.round(3)) if not t.empty else "-"  # noqa: E731
    L = ["# Extension 6: probing and steering" + (" (DEVELOPMENT RUN, not analysed)" if dev else ""), "",
         "Design: `docs/preregistration_extension6.md`. Estimates in percentage points (steering: change per unit of "
         "steering strength k; k = 1 adds the mean angry - neutral difference once). p = rank of the anger direction among "
         "random directions of the same norm (one-sided); Holm over M1-M3 within a model.", "",
         "## Confirmatory tests", "", show(T), "",
         "## Does the Hugging Face model show the behavioural effects? (unsteered)", "", show(B), "",
         "## Other directions at the steering layer (exploratory)", "", show(E), "",
         "## Layer sweep (exploratory): steering slope of each layer's anger direction vs 10 random directions", "", show(S), "",
         "## Probes by layer", "", show(P), ""]
    (out / "report.md").write_text("\n".join(L), encoding="utf-8")
    for name, t in [("tests", T), ("probe", P), ("sweep", S), ("behaviour", B), ("other_directions", E)]:
        t.to_csv(out / f"{name}.csv", index=False)
    print(out / "report.md")
    print(T.round(3).to_string())


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--dev", action="store_true")
    main(ap.parse_args().dev)
