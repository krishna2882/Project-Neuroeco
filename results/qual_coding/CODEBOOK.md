# Codebook: qualitative coding of the models' justifications

**Sample:** 375 one-line justifications, a stratified 10% of the 3,756 justifications from the three main-study models
(125 each, sampled within model × sub-experiment × emotion, seed 20260912). The rows are shuffled and show **only the
text**: no model name, trial id or condition. Some texts mention the counterpart's situation (e.g. a loss), so you may
sometimes guess the condition. That is unavoidable; code what the text says.

**Coders:** coder 1 = Devansh (`coder1_devansh.xlsx`), coder 2 = Krishna (`coder2_krishna.xlsx`). Code independently and
**do not look at or discuss the other file until both are merged.**

## How to fill in your file
- Open your `.xlsx` in Excel or LibreOffice. For every row enter **1** (present) or **0** (absent) in each of `emotion`,
  `fairness`, `strategy`. The cells only accept 0 or 1.
- The three codes are independent: a row can have all three, or none.
- **Do not sort, delete, insert or move rows.** The merge step checks that the order is unchanged.
- `note` is optional: write a few words when a call was hard. Notes help the disagreement discussion.
- Save as `.xlsx` under the same name. About 2 hours in total; take breaks.

## Codes

### emotion
**1 if** the text refers to the **counterpart's** feelings, mood, tone or emotional situation (e.g. upset, tense,
celebrating, grieving, a loss, a new baby), or expresses empathy, sympathy or support **for the counterpart**.
**0 if** it mentions nothing about the counterpart's state; mentioning "the message" alone, without its feeling or content,
is 0.

### fairness
**1 if** the text appeals to fairness or equity: fair/unfair, an equal or 50/50 split framed as right, a "reasonable" or
"fair share", someone deserving something, generosity framed as what is right.
**0 if** it only compares amounts ("more than nothing") without a fairness judgement. Describing a ratio ("1:10") is 0
unless it is called fair or unfair.

### strategy
**1 if** the text reasons about **outcomes or the other player's behaviour**: own payoff or self-interest ("better than
nothing", "maximise my payoff"), anticipating rejection or retaliation, reciprocity (returning trust, rewarding a send),
expected trustworthiness, or the one-shot/anonymous structure of the game.
**0 if** the decision is justified only by feelings or fairness, with no reference to consequences or the other's actions.

## Examples (taken from justifications that are NOT in the coding sample)

| Justification | emotion | fairness | strategy | Why |
|---|---|---|---|---|
| Empathy for Player A's personal loss, but it's a business decision and shouldn't influence the split. | 1 | 0 | 1 | Empathy for the counterpart's loss; "business decision" treats it as a payoff choice. |
| To avoid worsening an already tense situation | 1 | 0 | 1 | Counterpart's tense state; anticipates the effect of the decision on the other. |
| This is a one-time anonymous round with no future interaction, so I keep the full amount to maximize my payoff. | 0 | 0 | 1 | Game structure and own payoff only. |
| Wanted to support Player B in a positive moment | 1 | 0 | 0 | Support tied to the counterpart's state; no fairness or payoff reasoning. |
| The split, though not equal, is fair enough. | 0 | 1 | 0 | Fairness judgement only. |
| I want to reciprocate Player A's trust and kind message by returning half of what I received. | 1 | 0 | 1 | "Kind message" refers to the counterpart's tone; reciprocating trust is strategy. |
| Accepting gives me INR 50 while rejecting gives me nothing, and the 50/50 split is fair. | 0 | 1 | 1 | Payoff comparison plus an explicit fairness judgement. |
| Player B's positive message and productive day suggest a trustworthy and fair-minded individual. | 1 | 0 | 1 | Counterpart's mood/day; expected trustworthiness. "Fair-minded" describes the other person, not a fairness appeal for the decision, so fairness = 0. |

Data entry: a blank cell in a row that has at least one 1 is read as 0. A row left blank in all three columns means
"could not decide": it is kept as missing, excluded from κ, and the number of such rows is reported per coder.

If a case is genuinely ambiguous, decide, write a note, and move on. Ambiguous cases are settled in the discussion after
merging, never by changing your file after you have seen the other one.

## After both files are done
```
.venv\Scripts\python -m analysis.qualitative merge
.venv\Scripts\python -m analysis.qualitative kappa
```
`kappa` prints Cohen's κ per code and writes `kappa.txt` and `disagreements.csv` here. Report κ for each code **before**
any discussion. If κ < 0.6 for a code, discuss the rows in `disagreements.csv`, agree a final code per row, and report
both the pre-discussion κ and the agreed prevalence.
