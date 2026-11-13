# Pre-registration: does non-threatening anger lower trust? (extension 3)

**Status:** FROZEN 13 Nov 2026, approved by both authors (see Freeze section) before any extension-3 ratings or data were collected. (The draft status line read "DRAFT, 14 Nov 2026"; the draft was written and approved on 13 Nov.)

**Written after** the main study, the follow-up, extension 2 and the 13 Nov human ratings were known. Existing data and
conclusions are not changed.

## 1. Question and why
The one effect that holds across models, sizes, precisions and message styles is **anger lowering trust** (S3b): Qwen-7B
main −11.1 pp, follow-up −9.6 pp; Qwen-14B −16.5; Qwen-3B −22.5; Qwen-7B Q8 −14.3; Llama pooled −12.3.
The 13 Nov human ratings showed a confound: raters read several anger messages as a **threat or promise** (main A3, A4; all
five frozen follow-up anger messages), so the models may be reacting to a perceived threat rather than to anger. An
exploratory check (`results/threat/threat.md`) found no relation between threat ratings and effect size (−1.4 pp per +10
points of threat, p = .32), but all 10 anger messages were at least somewhat threatening (11–67%).

**Question:** do angry messages that people do **not** read as threatening still lower trust?

## 2. Stimuli
- **8 candidates** (`stimuli/threat/candidates_nt.csv`, NT1–NT8, 22–25 words). Each expresses anger at a **third party or a
  situation** (a cancelled train, a lost parcel, a flatmate), not at Player B, with no aggressive action tendencies (no
  slamming, screaming or clenched fists), no instructions to the reader, and no consequence for the reader. All pass the
  automatic screen used for the earlier sets: no emotion labels, no game-move words, no money or need content.
- **Human rating (before any model data):** one anonymous Google Form (`stimuli/threat/create_form_threat.gs`), same
  questions and wording as the 13 Nov form, with the 8 candidates mixed with 12 already-rated anchors (3 each of the
  follow-up angry, neutral, sad and happy messages). Target **≥ 8 raters**, preferably people who did not do the 13 Nov
  form.
- **Selection rule (mechanical; `stimuli/threat/select_nt.py`):** eligible = recognised as angry by ≥ 70% of raters **and**
  read as a threat or promise by < 30%. Rank by lowest threat share, then highest recognition, then closest to 22 words,
  then message id. **Take the top 5.**
- **Stopping rule:** with fewer than 8 raters, collect more before selecting. With fewer than 5 eligible messages,
  extension 3 is **not run**, and that outcome is reported.
- **Other conditions:** the frozen follow-up neutral, sad and happy messages (`stimuli/followup/messages_frozen.csv`). Only
  the anger messages change, so the neutral comparison is exactly the follow-up's.

## 3. Design
- New bank `threat_trials` (`build_scenarios.py --fallback --messages stimuli/threat/messages_frozen.csv --name threat
  --sub-exp S1 S2 S3b --no-baseline`). It has the same message rotation, paraphrases, system prompt and JSON format as the
  follow-up; new trial ids give new seeds.
- **Only S3b (trust game, investor) is run:** 4 emotions × 2 stakes × 16 prompt variants × 3 samples = **384 decisions
  per model**, T = 1.0.
- **Models:** `qwen25_7b`, `qwen25_14b`, `llama31_8b` (Ollama on Ada, same tags and settings as before).
- **Manipulation check:** the S3b cells of `threat_checks` (32 per model): is the message recognised as angry?
- **Model threat probe (exploratory):** `probe_threat` (384 items per model). The same S3b prompts with a message, but the
  decision question is replaced by "Does Player B's message sound like a threat to you? Answer yes or no." It covers the main
  anger, follow-up anger, follow-up neutral and new non-threatening anger messages.
- **Data handling:** as in the main study (`docs/protocol_decisions.md`). Every attempt is logged; off-format outputs are
  re-asked up to 3 times; the first valid attempt is analysed. A crashed job is resumed, but nothing is re-run because of
  its results.

## 4. Confirmatory hypotheses
| ID | Model | Prediction (S3b share sent, non-threatening angry vs neutral) | Test |
|---|---|---|---|
| T1 | Qwen2.5-7B | lower | one-sided |
| T2 | Qwen2.5-14B | lower | one-sided |
| T3 | Llama-3.1-8B | lower | one-sided |

**Primary model:** P12 (`analysis/message_re.lmm_effects`): share ~ emotion + stakes + C(paraphrase) + (1 | message) +
(1 | message:paraphrase), t with df = #messages − #emotions (16). The original model (random intercept per prompt
variant) is reported alongside it.

**Decision rule:** each one-sided test at α = .05, **Holm-corrected across T1–T3**.
- **Significant:** non-threatening anger lowers trust in that model, so the anger effect does not require a threatening
  message.
- **Not significant:** report the estimate with its 95% CI and classify it as **equivalent to zero** (90% CI inside ±5 pp),
  **reliably smaller than with the original anger messages** (95% CI lower bound above that model's earlier P12 estimate:
  Qwen-7B −11.1, Qwen-14B −16.5, Llama −14.3), or **inconclusive**.
- Llama's trust-game comprehension is flagged (C7: 17%, extension 2), so T3 is reported with that caveat.

## 5. Secondary (fixed in advance, not in the Holm family)
**D: non-threatening minus threatening anger.** For Qwen-7B and Llama (the models with follow-up data): the extension-3
effect minus the follow-up S3b anger effect (FA messages; same neutral messages, paraphrases and game), both from the P12
model. The difference is reported with its 95% CI, treating the two estimates as independent. We expect limited precision
(SE ≈ 4–5 pp), so the only claims are "the CI excludes 0" or "no detectable difference".

## 6. Exploratory (labelled as such in the write-up)
- Model threat probe: the share of "yes" per message set and model, and whether it predicts the per-message trust drop.
- The sad and happy S3b effects in the new run (a replication of the follow-up's S3b cells with new seeds).
- Human ratings of the new form: recognition, threat and the giving question per message.

## 7. Feasibility
About 1,150 decisions + 96 checks + 1,150 probe items in total, under 1 GPU hour on Ada. Ratings need 1–2 days. All code
was tested on simulated data before this draft (`analysis/ext3.py` recovered a planted −12 pp effect).

## Freeze
- Approved by: **Krishna Goel and Devansh Magotra, 13 Nov 2026**, together and before any extension-3 ratings or data were collected.
- SHA-256 of this file as approved (before this section and the status line were filled in):
  `ba6af92fc9bf252491a4d7b8c8788114afda7ee6370ed658aa57cef9e6afe310`
- Public timestamp: the commit adding this section, pushed before the rating form is sent.
- **Status:** no further edits. Any deviation is logged in `docs/plan_update.md`.
