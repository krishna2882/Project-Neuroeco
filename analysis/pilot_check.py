"""Apply protocol decision D11 to the pilot: is either model at ceiling or floor in S1?

  python -m analysis.pilot_check            # reads data/raw/*/pilot.jsonl

Ceiling: P(reject | 10% offer) <= 0.10.  Floor: P(accept | 50% offer) <= 0.10 (pooled over emotion, stakes).
If either rule fires for any model, the fallback applies to both models:
  python build_scenarios.py --fallback      (adds the 5% / 45% offer cells)
  and run S1 with --logprobs where the runtime supports it.
"""
import pandas as pd

from analysis.common import load_raw, md_table, quality_table, tidy_trials
from config import RESULTS_DIR


def main(tag="pilot"):
    raw = load_raw(tag, "trials")
    df = tidy_trials(tag)
    out = ["# Pilot check (D11)", "", "## Data quality", "", md_table(quality_table(raw)), ""]
    s1 = df[df.sub_exp == "S1"]
    fire = False
    rows = []
    for m, g in s1.groupby("model_key"):
        r10 = g[g.offer_share == g.offer_share.min()].reject.mean()
        a50 = g[g.offer_share == 0.5].accept.mean()
        ceiling, floor = r10 <= 0.10, a50 <= 0.10
        fire |= ceiling or floor
        rows.append(dict(model=m, n_S1=len(g), reject_at_10pct=r10, accept_at_50pct=a50,
                         ceiling=ceiling, floor=floor))
        rate = g.groupby(["stakes", "offer_share"]).reject.agg(["mean", "size"]).unstack("offer_share")
        out += [f"### {m}: S1 rejection rate by stakes x offer (mean, n)", "", md_table(rate.round(2)), ""]
    out += ["## Rule", "", md_table(pd.DataFrame(rows)), "",
            f"**Fallback {'APPLIES' if fire else 'does not apply'}.**", ""]
    for sub in ["S2", "S3a", "S3b"]:
        g = df[df.sub_exp == sub]
        if len(g):
            t = g.groupby(["model_key", "game" if sub == "S2" else "stakes"]).share.describe()[["count", "mean", "std", "min", "max"]]
            out += [f"### {sub} share distribution", "", md_table(t.round(3)), ""]
    path = RESULTS_DIR / "pilot_check.md"
    RESULTS_DIR.mkdir(exist_ok=True)
    path.write_text("\n".join(out))
    print("\n".join(out))


if __name__ == "__main__":
    main()
