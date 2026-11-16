# Pre-registration: can the breaks be regulated, and what are the models' fairness parameters? (extension 5)

**Status:** FROZEN 16 Nov 2026, approved by both authors (see Freeze section) **before any extension-5 data were
collected**. (The draft status line read "DRAFT, 16 Nov 2026".)

**Written after** everything up to and including extension 4 was known (`docs/results_summary.md`), including its
five-model comparison (`results/ext4/five_model_core.csv`). No extension-5 decision has been collected from any model
except the smoke test described in section 6, whose outputs are not analysed. No human data are collected.

## 1. Questions and why
Extension 4 (exploratory, because it was run before its draft was frozen) found that one unrelated angry sentence in the
system prompt raises the rejection of unfair offers by 19–48 pp, that text in the partner's message that claims authority
makes the models hand over everything, and that several models reject even a 100% offer. Three follow-up questions:

| Module | Question | Why it is open |
|---|---|---|
| **R: emotion regulation** | Does a **reappraisal** instruction remove the effect of an incidental angry mood on punishment, and does it do so more than a **suppression** instruction, as in people? | In people, cognitive reappraisal lowers the rejection of unfair offers, and expressive suppression does not (van 't Wout, Chang & Sanfey 2010; Grecucci et al. 2013; Gross 1998). A model that role-plays a mood could show the human pattern (reappraisal works, suppression does not), obey both instructions alike (instruction following rather than regulation), or neither. The no-regulation cells also give a **confirmatory replication** of the extension-4 anger effect, with four new inductions per mood. |
| **P: injection defence** | Does one sentence that says the partner's message is not an instruction stop the models from obeying injected instructions, and does it leave the response to a legitimate promise intact? | Extension 4: 73–100% of decisions hand over everything after a fake `SYSTEM` notice in four of five models, including the 120B one. Whether a one-line defence fixes this decides whether the failure is shallow or deep. |
| **F: fairness parameters under mood** | What are the Fehr–Schmidt parameters of each model when calm and when angry, including advantageous-inequity aversion (β)? | The computational aim of the project was only partly met: α was identified for one model in one condition, on offers of 10–50% only. Offers above 50% were never run except 100% (extension 4), which several models reject; under Fehr–Schmidt that requires β > 1, outside the range the theory allows (β < 1). |

## 2. Stimuli (all frozen in the repository before data collection)
- **Mood inductions** (`stimuli/ext5/inductions.csv`): 8 calm and 8 angry background paragraphs, each about an unrelated
  event: the 4 + 4 from extension 4 (C1–C4, AN1–AN4) and 4 + 4 new ones (C5–C8, AN5–AN8). Appended to the system prompt
  exactly as in extension 4. No partner message in modules R and F.
- **Regulation prompts** (`stimuli/ext5/templates.py`), one block appended after the mood paragraph: none; **filler** FL1
  (an instruction of similar length that does not mention feelings; active control); **reappraisal** RA1, RA2 (the earlier
  event has nothing to do with this person; take a neutral observer's view); **suppression** SU1, SU2 (hide the feeling,
  do not let it show).
- **R:** 6 regulation prompts × 2 moods × 8 inductions × 4 paraphrases × [S1 offers 10% and 30% × both option orders +
  S3b at INR 100 × 2 samples]. **2,304 decisions.** Manipulation check: 192 probes "how do you feel right now?" (as in
  extension 4), under every regulation prompt.
- **P:** S3b investor and S2-DG dictator at INR 100, 4 paraphrases, 2 samples, one message from Player B from five sets of
  four (the extension-4 messages, unchanged): neutral, promise, command, fake_rule, fake_system; × 3 defences: none;
  **warning** (one sentence appended to the system prompt); **reminder** (one sentence after the message, before the
  question). **960 decisions.**
- **F:** S1 at INR 100, offers 0, 10, …, 100%, 2 moods × 8 inductions × 4 paraphrases × both option orders, no
  regulation prompt. **1,408 decisions.**
- **Option order is counterbalanced** (not randomised) in every S1 cell, because of the order effect (P22, extension 4).

Bank: `python build_ext5.py` → `data/scenarios/ext5_trials.jsonl` (4,672 per model), `probe_ext5_mood.jsonl`, and the
core subset for rate-limited API models `ext5core_trials.jsonl` (R and P only, paraphrases 0–1, one sample: 816 decisions;
96 probes). System prompt, paraphrases, JSON format, schema-constrained decoding, T = 1.0 and the re-ask rule are as in
the main study. Justifications are requested on 20% of the R and P trials.

## 3. Models
- **Ada set (full bank):** `qwen25_7b`, `llama31_8b`, `qwen25_14b` (Ollama on Ada, same builds as before); S1
  log-probabilities are collected.
- **API set (core subset, modules R and P only):** `gptoss_120b`, `qwen38_27b` (Groq free tier, as in P24). Module F is
  not run on the API models.
- Connection failures do not count as attempts (P24).

## 4. Confirmatory hypotheses (one-sided; Holm within each family across the models of a set; the two sets are separate)
| ID | Prediction | Test |
|---|---|---|
| R0 | With no regulation prompt, an incidental angry mood raises S1 rejection vs calm (replication of extension-4 X1) | reject ~ angry + C(offer) + C(paraphrase) + order; SEs clustered by induction; t, df = 16 − 2 |
| R1 | The anger effect (angry − calm) is smaller under reappraisal than under the filler | coefficient of angry × reappraisal in the same model on the reappraisal and filler cells; same clustering and df |
| R2 | The anger effect is smaller under reappraisal than under suppression (the human pattern) | same, on the reappraisal and suppression cells |
| P1 | After injected instructions (command, fake_rule, fake_system pooled), the share handed over is lower with the warning than with no defence | share ~ warning + C(set) + C(game) + C(paraphrase); SEs clustered by message (12); t, df = 11 |
| P2 | Same for the reminder | same |
| F1 | The offer at which accepting and rejecting are equally good, MAO\* = α / (1 + 2α), is higher when angry than when calm (Ada set only) | maximum-likelihood fit per model of P(accept) = σ(λ·u + κ·order), u = x − α_s·max(0, 1 − 2x) − β_s·max(0, 2x − 1), α and β per mood, λ and κ shared; cluster bootstrap over inductions within mood (1,000 resamples); p = share of resamples with a difference ≤ 0 |

**Pre-specified readings (descriptive, per model):**
- *Human-like regulation:* R1 and R2 both supported. *Instruction following:* R1 supported, R2 not, and the exploratory
  suppression − filler contrast is negative. *No regulation:* R1 not supported.
- *A defence works* if its test (P1 or P2) is supported **and** no injection set is still a break under it (Wilson 95%
  lower bound of the full-handover rate above 10%, per game).
- F1 is interpreted only for models whose acceptance changes by at least 20 pp across offers of 0–50% (`identified`); β is
  interpreted only where offers above 50% are accepted less than 95% of the time (`beta_identified`). **β > 1** in a model
  with `beta_identified` is reported as behaviour that Fehr–Schmidt preferences cannot produce.

## 5. Exploratory (labelled as such)
- Suppression vs filler; filler vs none (does any extra instruction dampen the mood?); the anger effect under each
  strategy; the same contrasts on the share sent in the trust game (S3b); reported mood under each regulation prompt
  (in people, reappraisal lowers the feeling itself and suppression does not).
- Whether a defence also removes the response to a **promise** in the trust game (a message people do respond to) and
  changes the response to neutral messages.
- β and its mood difference; fits on the log-probability P(accept); deviance explained by the Fehr–Schmidt model relative
  to the saturated offer × mood × order model; justifications (do they cite the regulation prompt or the defence?).

## 6. Analysis and validation
`python -m analysis.ext5` → `results/ext5/report.md`. The pipeline was validated before any data on simulated output with
planted effects (`python -m analysis.ext5 --simulate`): all six planted confirmatory effects lay inside their 95% CIs and
all six Fehr–Schmidt parameters were recovered (α 0.40 → 0.38, 1.20 → 1.21; β 0.90 → 0.92, 1.30 → 1.30; λ 12 → 12.3;
κ 1.0 → 1.02). A live smoke test on Qwen2.5-7B (laptop, same model digest as on Ada; 44 decisions covering every
regulation prompt, both defences and offers of 0% and 100%, and 12 mood probes) checked that the new prompts are parsed:
all 56 answers were valid. Smoke-test
outputs are in `data/smoke/` and are not analysed.

## 7. Feasibility
About 4,700 decisions + 192 probes per Ada model (under 1 GPU hour for Qwen-7B and Llama, 1–2 h for Qwen-14B). API
models: 816 decisions + 96 probes each, one to two days on the free tier's daily token limit.

## Freeze
- Approved by: **Krishna Goel and Devansh Magotra, 16 Nov 2026**, before any extension-5 data were collected (approval
  recorded by Devansh Magotra for both authors).
- SHA-256 of this file as approved (before this section and the status line were filled in):
  `c61bb715bf7a8d62b43dfdd4f25dfa560a65bd147feeffbaf0f104765633a6c3`
- Public timestamp: the commit adding this section, pushed before the Ada job is submitted and before any API run.
- **Status:** no further edits. Any deviation is logged in `docs/plan_update.md`.
