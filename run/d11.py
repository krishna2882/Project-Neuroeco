"""Protocol decision D11 on a pilot tag: decide whether the 5%/45% offer fallback applies, and
report whether token log-probabilities came back. Writes data/FALLBACK_DECISION.txt.

  python -m run.d11 pilot_ada llama31_8b
"""
import sys

from analysis.common import tidy_trials
from config import DATA_DIR


def main(tag, model):
    d = tidy_trials(tag)
    d = d[d.model_key == model]
    s1 = d[d.sub_exp == "S1"]
    r10 = s1[s1.offer_share == 0.10].reject.mean()
    a50 = s1[s1.offer_share == 0.50].accept.mean()
    fire = bool((r10 <= 0.10) or (a50 <= 0.10))
    n_lp = int(s1.p_accept_lp.notna().sum()) if "p_accept_lp" in s1 else 0
    msg = f"{model} {tag}: P(reject|10%)={r10:.3f} P(accept|50%)={a50:.3f} fallback={fire} logprobs={n_lp}/{len(s1)}"
    print(msg)
    (DATA_DIR / f"FALLBACK_DECISION_{model}.txt").write_text(msg + "\n")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
