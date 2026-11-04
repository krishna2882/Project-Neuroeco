# Project Status — for Devansh (handoff, 15 Sep 2026)

Everything below is context so you're caught up without needing to ask Krishna to re-explain. Organized as: the locked design → what's done → what's NOT done → who does what next.

---

## 1. The project, in one paragraph

**"Evaluating Reciprocity Norms and Emotional Comprehension in LLM Decision-Making."** We're testing whether an LLM's economic decisions (accept/reject an offer, how much to give/return/send in Ultimatum/Dictator/Trust games) shift when the *counterpart* sends an emotionally-framed message (Neutral/Angry/Sad/Happy) before the decision — payoffs held identical across conditions. We compare the direction of any shift against known human neuroeconomic findings (Sanfey et al., Fehr-Schmidt inequity aversion, etc.).

**The locked design is `Team_10.pdf`** in this folder — that's the approach paper we submitted, and it is the source of truth for every number below. If anything here conflicts with it, the PDF wins (tell Krishna, there's an older `approach_paper.tex`/`Project_approach_paper.pdf` floating around with different numbers — ignore those, they're superseded drafts).

---

## 2. The locked design, summarized

**5 hypotheses:**
- H1 (negative reciprocity, UG), H2 (positive reciprocity, TG), H3 (emotion shifts decisions at fixed payoff — the core hypothesis), H4 (emotion's effect depends on whether the recipient can veto — UG vs DG), H5 (effects vary across model families — exploratory)

**4 sub-experiments:**
| | What it tests | Model's role |
|---|---|---|
| S1 | UG-responder | Accept/reject an offer |
| S2 | UG vs DG-proposer | Decide how much to give (H4 test) |
| S3a | TG-trustee | Decide how much to return |
| S3b | TG-investor | Decide how much to send |

**Scale:** 110 cells/model (88 factorial + 22 no-message baselines). Each cell gets 16 prompt variants (4 instruction paraphrases × 4 of the 5 frozen emotion messages) × 3 samples = 48 decisions/cell → **5,280 decisions/model, 10,560 total across both models**, plus ~800–1,000 sampled manipulation/belief checks.

**Emotion messages needed: 20 total** (5 per emotion × 4 emotions: Neutral/Angry/Sad/Happy) — length-matched, emotion conveyed through content not a label, no stated intent to accept/reject/retaliate.

**Models:** one local open-weight model (free, unlimited) + one closed API model (different family, for H5).

**Analysis:** mixed-effects logistic regression for S1 (MAO estimation via bootstrap), Fehr-Schmidt inequity-aversion fit, linear mixed models for S2/S3, Holm-corrected contrasts, 10% qualitative coding of justifications.

**Timeline:**
- **Phase 1 (now → Oct 3, mid-sem checkpoint):** lit review, frozen stimuli, frozen scenario bank, working pipeline, pilot run, analysis scripts validated on fake data
- **Phase 2 (Oct 4 → Nov 10):** full data collection (Oct 4–17) → cleaning (Oct 18–24) → modeling (Oct 25–31) → write-up/figures (Nov 1–7) → **presentation Nov 10**

---

## 3. What's DONE so far (all since 12 Sep, mostly today 15 Sep)

### Infrastructure (Krishna's side) — working end-to-end
- **Local model:** Llama-3.1-8B-Instruct (4-bit quantized) running via `llama.cpp` on Krishna's laptop GPU. Confirmed: returns proper JSON decisions, returns token log-probabilities (needed for the paper's pre-registered ceiling/floor fallback).
- **Closed API model:** ~~Gemini~~ → **switched to Groq**, hosting `openai/gpt-oss-120b`. Gemini's free tier turned out to cap at **20 requests/day** (discovered by actually hitting it) — completely unworkable for ~5,700 planned calls. Groq's free tier (1,000/day, 30/min, no payment method needed) is confirmed working and comfortably covers our needs in about 6 days of running.
- Fixed one real bug along the way: the `openai` Python library's new HTTP client couldn't decompress Groq's responses (unrelated to our code — a version-mismatch bug in their dependency). Worked around it; documented in the script.
- **`run/smoke_test.py`** — a small test harness (not the real data collector) that hits both models with placeholder prompts. Used to verify the plumbing works and to get an early read on model behavior.

### Draft stimuli (need your review — see Section 4)
- **`stimuli/messages_candidates.csv`** — 32 candidate emotion messages (8 per emotion), all 18–25 words, emotion conveyed through content not a label, no stated intent to accept/reject. This is a **draft pool** — Week 2 needs peer ratings (~10 people) to cut this down to the frozen 5/emotion = 20 total.
- **`stimuli/paraphrases.py`** — 20 instruction-prompt templates (4 paraphrases × 5 game types: S1, S2-UG, S2-DG, S3a, S3b). Rendered and syntax-checked, but **you haven't reviewed these yet** — Krishna wrote first drafts and flagged at least one judgment call worth a second opinion (S3b's framing of the trustee's discretion, whether it biases the investor's expectation).
- **`Phase1_Plan.md`** — the week-by-week plan with a table of 11 "protocol decisions" (things the approach paper left ambiguous — e.g., how baseline cells hit their decision quota, which message-rotation scheme to use, output JSON field names). These have Krishna's proposed defaults but **aren't formally frozen** — need your sign-off too.

### Early smoke-test findings (tiny sample, NOT real data — just plumbing checks)
- At low stakes (INR 100), all 3 models tested (local, Gemini, Groq) accepted 100% of offers at both 10% and 50% — looked like a hard ceiling.
- At high stakes (INR 10,000), first rejections appeared (small n, partial run). So behavior does seem to shift with stakes — not a hopeless ceiling, but **the real Week 2 pilot will likely need the paper's pre-registered fallback** (extend the offer grid to 5%/45%, score log-probabilities instead of just the discrete choice).

---

## 4. What's NOT done yet — this is where you come in

Nothing below has been started or needs your input before it can be finalized:

1. **Literature review** — NOT STARTED. This is squarely your part per the original plan (4 streams: behavioural economics of reciprocity, neuroeconomics, LLMs-as-economic-agents, emotion-in-LLMs — ending in a gap statement). ~1,500–2,500 words, due as part of the Oct 3 checkpoint.
2. **Review the 32 draft messages** (`stimuli/messages_candidates.csv`) — read through them, flag any that feel off, suggest edits before they go out for peer rating.
3. **Review the 20 paraphrase templates** (`stimuli/paraphrases.py`) — especially the S2/S3 framings, which involved judgment calls about wording that could subtly bias decisions.
4. **Sign off on the 11 protocol decisions** in `Phase1_Plan.md` (table A) — these are locked-in defaults right now, not yet a joint decision.
5. **Set up the peer-rating form** (Google Form, ~10 raters) for the message bank, and run it.
6. **`build_scenarios.py`** — not built yet. Generates the actual 110×16 scenario bank from the frozen stimuli.
7. **`runner.py`** — not built yet. This is the real data-collection script; `smoke_test.py` is just a throwaway test harness, not reusable for the actual run.
8. **The official pilot** (~300 calls, Week 2) — not run. This is what makes the real ceiling/floor call, not the smoke tests.
9. **Analysis scripts validated on simulated data** — not built. Needed before Oct 3 per the plan (mixed-effects models, MAO bootstrap, Fehr-Schmidt fit).

---

## 5. Suggested split (from Phase1_Plan.md, adjust as you like)

- **Krishna:** models + pipeline (mostly done — infra, smoke test; still needs `build_scenarios.py`, `runner.py`, analysis scripts)
- **Devansh:** literature review + stimuli review (messages/paraphrases exist as drafts but need your read-through; lit review is fully open)

---

## 6. Key files, for reference

| File | What it is |
|---|---|
| `Team_10.pdf` | **The locked design** — source of truth |
| `Phase1_Plan.md` | Week-by-week plan + open protocol decisions |
| `stimuli/messages_candidates.csv` | 32 draft emotion messages, awaiting peer rating |
| `stimuli/paraphrases.py` | 20 draft instruction templates, awaiting your review |
| `run/smoke_test.py` | Working test harness (not the real data collector) |
| `llama.cpp/` | Local model setup (Krishna's laptop) |
| `data/raw/*.jsonl` | Smoke test logs — not real experimental data |
