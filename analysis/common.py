"""Loading, cleaning and shared helpers for all analyses."""
import json
from pathlib import Path

import numpy as np
import pandas as pd

from config import DATA_DIR, EMOTIONS, RAW_DIR

SCEN = DATA_DIR / "scenarios"
EMO_ORDER = ["none"] + EMOTIONS  # baseline first for tables


def read_jsonl(path: Path) -> pd.DataFrame:
    with open(path) as f:
        return pd.DataFrame([json.loads(line) for line in f])


def load_bank(bank="trials") -> pd.DataFrame:
    return pd.read_json(SCEN / f"{bank}.jsonl", lines=True, dtype=False)


def load_raw(tag="main", bank="trials", raw_dir: Path = RAW_DIR) -> pd.DataFrame:
    """All attempts from every model directory that has <tag>.jsonl."""
    frames = []
    for d in sorted(Path(raw_dir).iterdir()):
        p = d / f"{tag}.jsonl"
        if d.is_dir() and p.exists():
            r = read_jsonl(p)
            r = r[r.bank == bank] if "bank" in r else r
            frames.append(r)
    if not frames:
        raise FileNotFoundError(f"no {tag}.jsonl under {raw_dir}")
    return pd.concat(frames, ignore_index=True)


def quality_table(raw: pd.DataFrame, bank_name="trials") -> pd.DataFrame:
    """Off-format / refusal accounting (reported, never silently dropped)."""
    first = raw[raw.attempt == 1]
    last = raw.sort_values("attempt").groupby(["model_key", "trial_id"]).tail(1)
    bank = load_bank(bank_name)[["trial_id", "sub_exp"]]
    first = first.merge(bank, on="trial_id", how="left")
    last = last.merge(bank, on="trial_id", how="left")
    q = first.groupby(["model_key", "sub_exp"]).status.value_counts().unstack(fill_value=0)
    q["n_trials"] = q.sum(axis=1)
    q["first_attempt_ok_%"] = 100 * q.get("ok", 0) / q["n_trials"]
    final_ok = last.groupby(["model_key", "sub_exp"]).status.apply(lambda s: 100 * (s == "ok").mean())
    q["final_ok_%"] = final_ok
    q["n_reasks"] = raw[raw.attempt > 1].merge(bank, on="trial_id").groupby(["model_key", "sub_exp"]).size()
    return q.fillna(0).round(2)


def tidy_trials(tag="main", raw_dir: Path = RAW_DIR, include_extension=True, bank="trials") -> pd.DataFrame:
    """One row per (model, trial): the first valid attempt, merged with the design."""
    raw = load_raw(tag, bank, raw_dir)
    ok = raw[raw.status == "ok"].sort_values("attempt").groupby(["model_key", "trial_id"]).head(1)
    keep = ["model_key", "trial_id", "attempt", "decision", "amount", "share", "reason", "model_version"]
    # Records from the corrected logprob parser carry decision_top_logprobs; earlier p_accept_lp values
    # (Llama main run) came from a parser that read the wrong token and are discarded.
    if "decision_top_logprobs" in ok:
        ok = ok.assign(p_accept_lp_main=ok.p_accept_lp.where(ok.decision_top_logprobs.notna()))
        keep.append("p_accept_lp_main")
    df = ok[keep].merge(load_bank(bank).drop(columns=["system", "prompt"]), on="trial_id", how="left")
    # Graded S1 DV: P(accept) from token logprobs, collected in a separate pass (<tag>_lp, same prompts
    # and seeds) with the corrected decision-token parser. p_accept_lp in the <tag> files themselves came
    # from an earlier parser that read the wrong token and is deliberately not used.
    try:
        lp = load_raw(f"{tag}_lp", bank, raw_dir)
        lp = lp[lp.status == "ok"].sort_values("attempt").groupby(["model_key", "trial_id"]).head(1)
        lp = lp[["model_key", "trial_id", "p_accept_lp", "decision"]].rename(columns={"decision": "decision_lp_pass"})
        df = df.merge(lp, on=["model_key", "trial_id"], how="left")
        if "p_accept_lp_main" in df:
            df["p_accept_lp"] = df.p_accept_lp.fillna(df.p_accept_lp_main)
    except FileNotFoundError:
        if "p_accept_lp" in ok:  # simulated data carries a valid p_accept_lp directly
            df = df.merge(ok[["model_key", "trial_id", "p_accept_lp"]], on=["model_key", "trial_id"], how="left")
            if not str(raw_dir).endswith("sim/raw"):
                df["p_accept_lp"] = df.get("p_accept_lp_main", np.nan)
        elif "p_accept_lp_main" in df:
            df["p_accept_lp"] = df.p_accept_lp_main
    df = df.drop(columns=["p_accept_lp_main"], errors="ignore")
    if not include_extension:
        df = df[~df.extension]
    df["reject"] = (df.decision == "reject").astype(float).where(df.sub_exp == "S1")
    df["accept"] = 1 - df["reject"]
    df["emotion"] = pd.Categorical(df.emotion, EMO_ORDER)
    df["stakes_c"] = np.where(df.stakes == df.stakes.max(), 0.5, -0.5)  # effect-coded stakes
    return df


def tidy_checks(tag="checks", raw_dir: Path = RAW_DIR, bank="checks") -> pd.DataFrame:
    raw = load_raw(tag, bank, raw_dir)
    ok = raw[raw.status == "ok"].sort_values("attempt").groupby(["model_key", "trial_id"]).head(1)
    cols = [c for c in ["perceived_emotion", "intensity", "fairness", "p_retaliate"] if c in ok]
    df = ok[["model_key", "trial_id"] + cols].merge(
        load_bank(bank).drop(columns=["system", "prompt"]), on="trial_id", how="left")
    return df


def holm(pvals) -> np.ndarray:
    p = np.asarray(pvals, float)
    order = np.argsort(p)
    adj = np.empty_like(p)
    running = 0.0
    m = len(p)
    for rank, i in enumerate(order):
        running = max(running, (m - rank) * p[i])
        adj[i] = min(1.0, running)
    return adj


def cohens_d(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    n1, n2 = len(a), len(b)
    sp = np.sqrt(((n1 - 1) * a.var(ddof=1) + (n2 - 1) * b.var(ddof=1)) / (n1 + n2 - 2))
    d = (a.mean() - b.mean()) / sp if sp > 0 else np.nan
    se = np.sqrt((n1 + n2) / (n1 * n2) + d ** 2 / (2 * (n1 + n2)))
    return d, d - 1.96 * se, d + 1.96 * se


def md_table(df: pd.DataFrame, floatfmt=3) -> str:
    """Small markdown table writer (avoids a tabulate dependency)."""
    df = df.reset_index() if not isinstance(df.index, pd.RangeIndex) else df
    cols = [str(c) for c in df.columns]

    def fmt(v):
        if isinstance(v, (float, np.floating)):
            return "" if np.isnan(v) else f"{v:.{floatfmt}f}"
        return str(v)
    lines = ["| " + " | ".join(cols) + " |", "|" + "|".join("---" for _ in cols) + "|"]
    lines += ["| " + " | ".join(fmt(v) for v in row) + " |" for row in df.itertuples(index=False)]
    return "\n".join(lines)


def fit_mixedlm(formula, data, groups):
    """statsmodels MixedLM (REML) with optimizer fallbacks: lbfgs can hit a singular X'V^-1X
    on these designs while bfgs/powell converge to the same optimum."""
    import warnings

    import statsmodels.formula.api as smf
    last = None
    for method in ("bfgs", "lbfgs", "powell", "nm"):
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                m = smf.mixedlm(formula, data, groups=groups).fit(reml=True, method=method)
            if m.converged:
                return m
            last = m
        except (np.linalg.LinAlgError, ValueError) as e:
            last = e
    if isinstance(last, Exception):
        raise last
    return last
