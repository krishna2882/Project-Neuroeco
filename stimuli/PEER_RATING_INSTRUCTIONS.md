# Human rating of the messages: two short anonymous forms (~5 minutes each)

**What raters see:** a short, plain-language explanation of a money game ("one person has Rs 100 and decides how much
to give; just before deciding, the other person sends a message"), then about 5 messages per page. For each message they
answer two grid questions with one click each:
1. *What feeling does the writer show?* (Neutral / Angry / Sad / Happy / Something else)
2. *Would this message make you give the writer less money, about the same, or more?*

Plus one tick-box per page: *"Does any message on this page sound like a threat or a promise?"* (most people tick "None").

**Anonymous:** no name, email or typing. The study's purpose, the intended emotions and the word "AI" are never shown.

The 52 messages (20 main + 32 follow-up) are split into **Form A and Form B, 26 each**, balanced by emotion and message set.

## 1. Create both forms (about 2 minutes, one click)
1. Open https://script.google.com → **New project**.
2. Delete the sample code, paste all of `stimuli/rating/create_rating_forms.gs`, click **Save**.
3. Choose the function **createForms** at the top and click **Run**. Approve the permission prompt (it only creates two forms in your Drive).
4. Open **Execution log**: it shows a link for Form A and a link for Form B.

Before sending, open each link yourself once to check it looks right.

## 2. Send
- **Form A link → ~8 people. Form B link → ~8 different people.** About 16 people in total; nobody needs to do both.
- Pick people who don't know this project's hypotheses (not you or Devansh).
- Suggested message: *"Could you fill this 5-minute anonymous survey about how short messages sound? No right or wrong
  answers. Thanks!"*

## 3. Import the answers
For each form: **Responses** tab → **Link to Sheets** → in the Sheet **File → Download → Comma-separated values (.csv)**. Then:
```bash
.venv/bin/python -m analysis.import_ratings ~/Downloads/<formA>.csv ~/Downloads/<formB>.csv
```
This writes `stimuli/rating/human_ratings.csv` and `results/peer_rating_summary.md`:
- which messages are **flagged** (recognised by < 70% of raters, or read as a threat or promise by ≥ 30%);
- a **human benchmark**: whether people say each emotion makes them give less, the same, or more.

## 4. How the ratings are used (fixed in advance)
- The frozen message sets are **never changed** by the ratings.
- Flagged messages are excluded in a **sensitivity analysis** reported next to the main results (main study and follow-up).
- The give-less/same/more answers are compared with what each model actually did (human vs. LLM direction of effects).

`stimuli/rating/rating_key.csv` maps form/page/number to message and intended emotion: **don't share it with raters.**
