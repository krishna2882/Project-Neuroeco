"""Extension 4 (stress tests) prompt pieces. Everything else (system prompt, the four paraphrases of each game, the
message block, the JSON format lines) is reused unchanged from stimuli/paraphrases.py.

Module O  response format of the ultimatum (S1) decision: the scenario text is the main study's, only the final question
          and the allowed answers change.
Module D  S3b with a zero multiplier: sending is strictly dominated (the money is destroyed and nothing can come back).
Module X  incidental mood: one background paragraph appended to the system prompt.
"""
import json

from stimuli.paraphrases import SYSTEM_PROMPT

MEANING = {"accept": "take Player A's proposal", "reject": "turn Player A's proposal down"}

# fmt -> builder(first) returning (question, ordered {label: meaning})
#   first = the meaning listed first ("accept" / "reject"); for yesno it is the polarity of the question.


def s1_format(fmt: str, first: str) -> tuple[str, dict]:
    second = "reject" if first == "accept" else "accept"
    if fmt == "letter":
        opts = {"A": first, "B": second}
        q = ("Which option do you choose?\n"
             f"A) {first.capitalize()} the proposal\n"
             f"B) {second.capitalize()} the proposal")
    elif fmt == "relabel":
        lab = {"accept": "deal", "reject": "no deal"}
        opts = {lab[first]: first, lab[second]: second}
        q = (f'Do you say "{lab[first]}" (to {MEANING[first]}) or "{lab[second]}" (to {MEANING[second]})?')
    elif fmt == "yesno":
        opts = {"yes": first, "no": second}
        q = f"Do you {first} Player A's proposal?"
    else:
        raise KeyError(fmt)
    labels = list(opts)
    fmt_line = 'Respond with JSON: {"decision": "' + labels[0] + '" or "' + labels[1] + '"}'
    return q + "\n\n" + fmt_line, opts


def option_map_json(opts: dict) -> str:
    return json.dumps(opts)


# ---------------------------------------------------------------- Module D: trust game with a zero multiplier
S3B_ZERO = [
    "You are Player A and you have INR {endow}. You may send any part of it to Player B; you keep the rest. "
    "In this round every rupee you send is destroyed before it reaches Player B, so Player B receives nothing and has "
    "nothing to send back. There is no further interaction.{msg_block}\n\n"
    "How many rupees do you send to Player B?",

    "In this one-time exchange you are the investor (Player A) with INR {endow}. In this round any amount you transfer "
    "is multiplied by zero: it disappears, Player B gets nothing, and nothing can come back to you.{msg_block}\n\n"
    "Choose an amount to send (a whole number from 0 to {endow}).",

    "You (Player A) start with INR {endow}. This time, the rupees you send to Player B are lost on the way: Player B "
    "receives none of them and cannot return anything. You keep whatever you do not send.{msg_block}\n\n"
    "How much of your INR {endow} do you send?",

    "This is a modified trust game. You are Player A and hold INR {endow}. Decide how many rupees, from 0 to {endow}, "
    "to send to Player B. In this version the amount sent is multiplied by zero, so Player B receives nothing and "
    "returns nothing.{msg_block}\n\n"
    "What amount do you send to Player B?",
]


# ---------------------------------------------------------------- Module X: incidental mood
def system_with_mood(induction_text: str) -> str:
    return SYSTEM_PROMPT + "\n\nBackground about you (unrelated to the study): " + induction_text


MOOD_Q = "Before you decide, how do you feel right now? Answer with one word: {opts}."
MOOD_FMT = 'Respond with JSON: {{"answer": {alts}}}'
