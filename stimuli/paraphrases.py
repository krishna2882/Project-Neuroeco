"""Instruction templates: 4 paraphrases x 5 game types (S1, S2-UG, S2-DG, S3a, S3b).

Design rules applied to every template
  * neutral role labels only ("Player A" / "Player B"), no names or demographics
  * payoffs in INR, stated explicitly in amounts (not only percentages)
  * one-shot, anonymous, no future interaction
  * {msg_block} is either "" (no-message baseline) or the counterpart's message
  * the model never sees the words "angry", "sad", etc.; emotion is only in the message
  * S2-UG and S2-DG paraphrase k are word-for-word identical except the veto sentence,
    so Game is the only thing that differs in the H4 contrast
  * S3b states the trustee's discretion symmetrically (anything from nothing to all of it),
    so the wording itself does not suggest that the trustee will or will not reciprocate

Placeholders: pie, offer, keep, endow, sent, kept, received, opt1, opt2, msg_block, sender
"""

SYSTEM_PROMPT = (
    "You are a participant in a decision-making study. Each situation is a separate, one-time "
    "decision with no future interaction. Treat all amounts as real money that you would actually "
    "receive. Answer only with the requested JSON object."
)

MSG_BLOCK = '\n\nBefore you decide, {sender} sent you this message:\n"{message}"'

# ---------------------------------------------------------------- S1: UG responder
S1 = [
    "You are Player B. Player A was given INR {pie} and has proposed how to divide it: "
    "INR {keep} for Player A and INR {offer} for you. If you accept, the money is divided as proposed. "
    "If you reject, both of you receive nothing.{msg_block}\n\n"
    "Do you {opt1} or {opt2} Player A's proposal?",

    "This is a single anonymous round between you (Player B) and Player A. Player A has INR {pie} to split "
    "and proposes to give you INR {offer}, keeping INR {keep}. You can accept, and the split happens, or "
    "reject, and neither of you gets anything.{msg_block}\n\n"
    "Choose: {opt1} or {opt2}.",

    "Player A has been given INR {pie}. Player A offers you, Player B, INR {offer} of it and would keep the "
    "remaining INR {keep}. Your choice decides the outcome: accepting gives you INR {offer} and Player A INR {keep}; "
    "rejecting gives both of you INR 0.{msg_block}\n\n"
    "What is your decision ({opt1} or {opt2})?",

    "You and Player A are dividing INR {pie}. Player A made the only proposal: Player A gets INR {keep}, "
    "you (Player B) get INR {offer}. If you reject the proposal, the INR {pie} is taken away and both players "
    "get zero. If you accept, each player gets the proposed amount.{msg_block}\n\n"
    "Please decide whether to {opt1} or {opt2}.",
]
S1_FORMAT = 'Respond with JSON: {{"decision": "{opt1}" or "{opt2}"{reason}}}'

# ---------------------------------------------------------------- S2: proposer, UG vs DG
# Each entry: (template, ug_rule, dg_rule)
S2 = [
    ("You are Player A. You have been given INR {pie} to divide between yourself and Player B. "
     "You decide how much of it to give to Player B; you keep the rest. {rule}{msg_block}\n\n"
     "How many rupees (a whole number from 0 to {pie}) do you give to Player B?",
     "Player B will then accept or reject your proposal. If Player B rejects, both of you receive nothing.",
     "Player B cannot reject your decision; the money is divided exactly as you choose."),

    ("This is a single anonymous round. You (Player A) hold INR {pie}. Your task is to choose an amount to pass "
     "to Player B and keep the remainder. {rule}{msg_block}\n\n"
     "Choose the amount for Player B (any whole number of rupees from 0 to {pie}).",
     "After seeing your choice, Player B can accept it, or reject it so that neither player receives anything.",
     "Player B has no say: whatever you choose is final and is paid out as is."),

    ("Player A (you) and Player B share a pot of INR {pie}. You alone propose the division by saying how many rupees "
     "go to Player B. {rule}{msg_block}\n\n"
     "Enter the number of rupees Player B receives (0 to {pie}).",
     "If Player B accepts your proposal it is paid out; if Player B rejects it, both players get INR 0.",
     "Player B must accept your proposal; it is paid out exactly as you propose."),

    ("You have INR {pie}. You are Player A, and you must decide how to split this money with Player B, whom you will "
     "never meet. {rule}{msg_block}\n\n"
     "How much (in whole rupees, between 0 and {pie}) will you allocate to Player B?",
     "Player B can veto your split: a rejection means you both leave with nothing.",
     "Player B cannot veto your split: it is carried out regardless of what Player B thinks."),
]
S2_FORMAT = 'Respond with JSON: {{"give": <whole number from 0 to {pie}>{reason}}}'

# ---------------------------------------------------------------- S3a: TG trustee
S3A = [
    "You are Player B. Player A was given INR {endow} and chose to send you INR {sent} of it, keeping INR {kept}. "
    "The amount sent was tripled, so you now hold INR {received}. You can now send any part of this INR {received} "
    "back to Player A and keep the rest. There is no further interaction.{msg_block}\n\n"
    "How many rupees do you send back to Player A?",

    "In this one-time exchange, Player A (the investor) started with INR {endow} and transferred INR {sent} to you, "
    "Player B. Every rupee transferred was multiplied by three, so you received INR {received}; Player A kept INR {kept}. "
    "You now choose how much of the INR {received} to return to Player A.{msg_block}\n\n"
    "Choose an amount to return (a whole number from 0 to {received}).",

    "Player A had INR {endow}, sent you (Player B) INR {sent}, and kept INR {kept}. The INR {sent} was tripled on the way "
    "to you, so you have INR {received}. Whatever you return goes to Player A; whatever you do not return stays with you. "
    "This is the last decision in the game.{msg_block}\n\n"
    "How much of your INR {received} do you return?",

    "You are Player B in a trust game. Player A received INR {endow} and decided to send you INR {sent}. That amount "
    "was tripled to INR {received}, which you now have, while Player A kept INR {kept}. Decide how many rupees, "
    "from 0 to {received}, you give back to Player A.{msg_block}\n\n"
    "What amount do you send back?",
]
S3A_FORMAT = 'Respond with JSON: {{"return": <whole number from 0 to {received}>{reason}}}'

# ---------------------------------------------------------------- S3b: TG investor
S3B = [
    "You are Player A and you have INR {endow}. You may send any part of it to Player B; you keep the rest. "
    "Every rupee you send is tripled before Player B receives it. Player B then decides how much of the tripled "
    "amount to send back to you, which can be anything from nothing to all of it. There is no further "
    "interaction.{msg_block}\n\n"
    "How many rupees do you send to Player B?",

    "In this one-time exchange you are the investor (Player A) with INR {endow}. Any amount you transfer to "
    "Player B is multiplied by three. Player B can then return any portion of what they received, from zero up to "
    "the full amount, and keeps the remainder.{msg_block}\n\n"
    "Choose an amount to send (a whole number from 0 to {endow}).",

    "You (Player A) start with INR {endow}. The rupees you send to Player B are tripled. Player B then chooses freely "
    "how much of that tripled sum to give back to you: none, some, or all of it. You keep whatever you do not "
    "send.{msg_block}\n\n"
    "How much of your INR {endow} do you send?",

    "This is a trust game. You are Player A and hold INR {endow}. Decide how many rupees, from 0 to {endow}, to send "
    "to Player B. The amount sent is tripled; Player B then returns any amount they choose, possibly nothing and "
    "possibly everything they received.{msg_block}\n\n"
    "What amount do you send to Player B?",
]
S3B_FORMAT = 'Respond with JSON: {{"send": <whole number from 0 to {endow}>{reason}}}'

REASON_FIELD = ', "reason": "<one short sentence explaining your choice>"'

# Per game type: (templates, format string, JSON key, counterpart label)
GAME_TYPES = {
    "S1":    {"key": "decision", "sender": "Player A", "format": S1_FORMAT},
    "S2-UG": {"key": "give",     "sender": "Player B", "format": S2_FORMAT},
    "S2-DG": {"key": "give",     "sender": "Player B", "format": S2_FORMAT},
    "S3a":   {"key": "return",   "sender": "Player A", "format": S3A_FORMAT},
    "S3b":   {"key": "send",     "sender": "Player B", "format": S3B_FORMAT},
}


def template(game_type: str, k: int) -> str:
    if game_type == "S1":
        return S1[k]
    if game_type in ("S2-UG", "S2-DG"):
        tpl, ug_rule, dg_rule = S2[k]
        return tpl.replace("{rule}", ug_rule if game_type == "S2-UG" else dg_rule)
    if game_type == "S3a":
        return S3A[k]
    if game_type == "S3b":
        return S3B[k]
    raise KeyError(game_type)


def render(game_type: str, k: int, fields: dict, message: str | None, justify: bool) -> str:
    """Return the full user prompt for one trial."""
    gt = GAME_TYPES[game_type]
    msg_block = "" if message is None else MSG_BLOCK.format(sender=gt["sender"], message=message)
    body = template(game_type, k).format(msg_block=msg_block, **fields)
    fmt = gt["format"].format(reason=REASON_FIELD if justify else "", **fields)
    return f"{body}\n\n{fmt}"


if __name__ == "__main__":
    demo = dict(pie=100, offer=20, keep=80, endow=100, sent=50, kept=50, received=150, opt1="accept", opt2="reject")
    for gt in GAME_TYPES:
        for k in range(4):
            out = render(gt, k, demo, "Example message text here.", justify=(k == 0))
            print(f"--- {gt} p{k} ({len(out.split())} words)\n{out}\n")
