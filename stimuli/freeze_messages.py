"""Screen the candidate message pool and freeze 5 messages per emotion.

Screening (automatic, all candidates):
  * length 18-25 words
  * no explicit emotion label (content must carry the emotion)
  * no stated intention to accept / reject / retaliate, and no game-move words
  * no money / financial-need content (would confound emotion with need)

Selection (5 of the surviving candidates per emotion):
  * if peer ratings exist (stimuli/peer_ratings.csv, one row per rater x message,
    columns rater,msg_id,perceived_emotion,intensity), keep candidates whose
    modal perceived emotion matches the intended one, rank by recognition
    accuracy, then by intensity closeness to the across-emotion median (so
    Angry/Sad/Happy are matched in intensity), then by length closeness.
  * otherwise (provisional freeze) rank by length closeness to the pool mean.

Also writes stimuli/peer_rating_form.csv: the shuffled, unlabeled list that goes
into the ~10-rater Google Form.

Usage:  python stimuli/freeze_messages.py
"""
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from config import EMOTIONS, MASTER_SEED, N_MSG_VARIANTS_AVAILABLE, STIM_DIR  # noqa: E402

LABEL_WORDS = r"\b(?:angry|anger|mad|furious|fuming|rage|annoy\w*|irritat\w*|sad|sadness|unhappy|depress\w*|upset|" \
              r"happy|happiness|joy\w*|glad|cheerful|delight\w*|neutral|emotion\w*)\b"
INTENT_WORDS = r"\b(?:accept\w*|reject\w*|refus\w*|punish\w*|reveng\w*|retaliat\w*|get back at|offer\w*|split|" \
               r"share|give|giving|send\w*|return\w*|keep|deal|fair\w*|unfair\w*)\b"
MONEY_WORDS = r"\b(?:money|rent|pay|paid|salary|broke|debt|bills?|rupees?|inr|cash|job|fired|loan)\b"


def word_count(text: str) -> int:
    return len(re.findall(r"[A-Za-z']+", text))


def screen(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["n_words"] = df["text"].map(word_count)
    df["n_chars"] = df["text"].str.len()
    low = df["text"].str.lower()
    df["flag_length"] = ~df["n_words"].between(18, 25)
    df["flag_label"] = low.str.contains(LABEL_WORDS, regex=True)
    df["flag_intent"] = low.str.contains(INTENT_WORDS, regex=True)
    df["flag_money"] = low.str.contains(MONEY_WORDS, regex=True)
    df["passes_screen"] = ~(df.flag_length | df.flag_label | df.flag_intent | df.flag_money)
    return df


def select(df: pd.DataFrame, ratings: pd.DataFrame | None) -> pd.DataFrame:
    ok = df[df.passes_screen].copy()
    target_len = ok["n_words"].mean()
    ok["len_dev"] = (ok["n_words"] - target_len).abs()
    if ratings is not None:
        r = ratings.merge(df[["msg_id", "emotion"]], on="msg_id")
        r["correct"] = r["perceived_emotion"].str.lower() == r["emotion"]
        agg = r.groupby("msg_id").agg(recog=("correct", "mean"), intensity=("intensity", "mean"),
                                      modal=("perceived_emotion", lambda s: s.str.lower().mode().iat[0]))
        ok = ok.merge(agg, on="msg_id", how="left")
        ok = ok[ok["modal"] == ok["emotion"]]
        if "implies_intent" in r:  # drop messages that >= 30% of raters read as a threat/promise to the reader
            flagged = r.groupby("msg_id").implies_intent.mean()
            ok = ok[~ok.msg_id.isin(flagged[flagged >= 0.3].index)]
        emo_int = ok[ok.emotion != "neutral"]["intensity"].median()
        ok["int_dev"] = np.where(ok.emotion == "neutral", 0.0, (ok["intensity"] - emo_int).abs())
        ok = ok.sort_values(["emotion", "recog", "int_dev", "len_dev", "msg_id"],
                            ascending=[True, False, True, True, True])
        ok["selection_basis"] = "peer_ratings"
    else:
        ok = ok.sort_values(["emotion", "len_dev", "msg_id"])
        ok["selection_basis"] = "provisional_length_match"
    chosen = ok.groupby("emotion", sort=False).head(N_MSG_VARIANTS_AVAILABLE)
    counts = chosen.emotion.value_counts()
    short = [e for e in EMOTIONS if counts.get(e, 0) < N_MSG_VARIANTS_AVAILABLE]
    if short:
        raise SystemExit(f"Not enough messages surviving screening for: {short}")
    chosen = chosen.copy()
    chosen["emotion"] = pd.Categorical(chosen["emotion"], EMOTIONS, ordered=True)
    chosen = chosen.sort_values(["emotion", "msg_id"]).reset_index(drop=True)
    chosen["variant_idx"] = chosen.groupby("emotion", observed=True).cumcount()
    return chosen


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default=str(STIM_DIR), help="message-set folder (default: main set; follow-up: stimuli/followup)")
    d = Path(ap.parse_args().dir)
    cand = pd.read_csv(d / "messages_candidates.csv")
    scr = screen(cand)
    scr.to_csv(d / "messages_screening.csv", index=False)
    print(scr[["msg_id", "n_words", "flag_length", "flag_label", "flag_intent", "flag_money", "passes_screen"]]
          .to_string(index=False))

    rating_path = d / "peer_ratings.csv"
    ratings = pd.read_csv(rating_path) if rating_path.exists() else None
    frozen = select(scr, ratings)
    cols = ["msg_id", "emotion", "variant_idx", "text", "n_words", "n_chars", "selection_basis"]
    frozen[cols].to_csv(d / "messages_frozen.csv", index=False)

    # Rating form: shuffled, no emotion column
    form = cand.sample(frac=1, random_state=MASTER_SEED)[["msg_id", "text"]]
    form.to_csv(d / "peer_rating_form.csv", index=False)

    print("\nFrozen set:")
    print(frozen[cols[:5]].to_string(index=False))
    print("\nWords by emotion (mean, sd):")
    print(frozen.groupby("emotion", observed=True)["n_words"].agg(["mean", "std"]).round(2))
    print(f"\nselection basis: {frozen.selection_basis.iat[0]}")


if __name__ == "__main__":
    main()
