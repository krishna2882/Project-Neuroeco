# Pre-registration: event-free emotion messages (follow-up study)

**Status:** FROZEN 12 Nov 2026 (see Freeze section). Krishna and Devansh must approve it **before any follow-up data are collected**. On approval, record
the date and the SHA-256 of this file in the "Freeze" section and email it to both authors (and the instructor, if possible)
as a timestamp.

**Relation to the main study:** written *after* the main results (`docs/results_summary.md`) were known. It is a
confirmatory test of one specific threat to validity, not a re-analysis. The main study's messages and results are
not changed.

## 1. Motivation
In the main study each emotion message describes a **life event**: sad = bereavement or loss, happy = engagement or birth,
angry = a provocation. A model may therefore respond to the *event* (e.g. sympathy for someone whose dog died) rather than
to the *expressed emotion*. Mistral's reasoning text shows "empathy" mentioned in 75–96% of sad-condition trials,
consistent with either reading.

**Question:** do the main study's emotion effects persist when the same four emotions are expressed **without any life
event**, only through present-tense bodily and behavioural cues ("my jaw is clenched…", "my eyes are puffy from crying…")?

## 2. Stimuli
- 32 candidates (`stimuli/followup/messages_candidates.csv`), 8 per emotion, 18–25 words. They pass the same automatic
  screen as the main set: no emotion labels, no accept/reject/retaliation or game-move words, no money or need content.
  Neutral candidates describe a flat present moment (no personal events).
- **Selection (frozen before data collection; same rule as the main study):** 5 per emotion that pass the automatic
  screen, chosen for length matching (mean 22.0–22.4 words per emotion). The frozen set is
  `stimuli/followup/messages_frozen.csv`:
  - neutral: FN2, FN5, FN6, FN7, FN8
  - angry: FA2, FA3, FA4, FA6, FA7
  - sad: FS1, FS3, FS4, FS5, FS7
  - happy: FH1, FH2, FH5, FH6, FH7
- **Human peer ratings** (target ≥ 8 raters; `stimuli/PEER_RATING_INSTRUCTIONS.md`) are collected in parallel and used
  **only for a pre-specified sensitivity analysis**. A message is excluded there if it is recognised as the intended emotion
  by < 70% of raters, or read as a threat or promise by ≥ 30%. Confirmatory conclusions come from the full frozen set;
  if a conclusion flips when flagged messages are excluded, that is reported.

## 3. Design
Identical to the main study except for the messages: same 4 paraphrases, same message-rotation scheme, 3 samples, T = 1.0,
same system prompt, same JSON output and parsing. Cells: **S1** (4 emotions × 7 offers incl. 5%/45% × 2 stakes = 56),
**S2** (4 emotions × UG/DG × 2 stakes = 16), **S3b** (4 emotions × 2 stakes = 8). That is 80 cells × 48 = **3,840 decisions per
model**, plus 320 manipulation checks. No-message baselines are not re-run (they don't depend on the messages).
S3a is omitted: no confirmatory effect there in the open models; Mistral's S3a effects were not emotion-specific.

**Models:** Llama-3.1-8B and Qwen2.5-7B (identical runtime and version strings to the main study, on Ada). Mistral
Large 4 only if its free API budget allows; otherwise it is reported as not run.

## 4. Confirmatory hypotheses
Chosen because these effects survived study-wide FDR correction in the main study (`results/main/forest.md`):

| ID | Model | Prediction with event-free messages | Main-study estimate |
|---|---|---|---|
| F1 | Qwen | S1: sad proposer **lowers** rejection vs neutral (log-OR < 0) | −0.95 |
| F2 | Qwen | S3b: angry trustee **lowers** share sent vs neutral | −11.2 pp |
| F3 | Mistral (if run) | S2-DG: sad recipient **raises** giving vs neutral | +24.6 pp |
| F4 | Mistral (if run) | S2-DG: angry recipient raises giving vs neutral | +9.6 pp |

**Exploratory:** Qwen S1 angry raises rejection (main: +0.85, p = .014, not significant study-wide); all other emotion ×
sub-experiment cells; Llama throughout (no main-study effect survived correction); Emotion × Game (H4).

## 5. Analysis (same code as the main study)
`python -m analysis.run_all --bank-prefix followup --tag followup --checks-tag followup_checks --out followup`, then
`python -m analysis.forest --out followup`. Same models: GLMM for S1 (reference = neutral), LMM for S2/S3b with
variant random intercepts, fractional-logit robustness.

**Decision rule for F1–F4:** one-sided test in the predicted direction, Holm-corrected across the confirmatory hypotheses
that were actually run (α = .05). For each, we report:
- **Replicated:** significant in the predicted direction.
- **Not replicated:** not significant. We also report the event-free estimate with its 95% CI and whether that CI excludes
  the main-study estimate (i.e., whether the effect is reliably *smaller*).

**Interpretation, fixed in advance:**
- Effects that replicate → driven by the expressed emotion, not only by the life event.
- Effects that disappear, with a CI excluding the main estimate → at least partly event-driven (e.g. sympathy for a
  bereavement rather than for sadness).
- Inconclusive (wide CI overlapping both) → reported as inconclusive.

**Manipulation check:** recognition ≥ 80% per emotion is required for an emotion's effects to be interpreted. Below
that, the effect is reported but marked "manipulation failed".

## 6. Data handling
Exactly as in the main study (`docs/protocol_decisions.md`): every attempt logged; off-format outputs re-asked up to 3
times; the first valid attempt is analysed; failure rates reported. No data are excluded beyond this.

## Freeze
- Approved by: **Krishna Goel, 12 Nov 2026**. **Devansh Magotra, 12 Nov 2026**, signed off in person after the follow-up data
  had been collected. Data collection went ahead on Krishna's approval alone, a deviation from the "both authors before any
  data" rule above (logged as P13 in `docs/plan_update.md`). The document was not changed between the freeze and his sign-off.
- SHA-256 of this file as approved, i.e. before this Freeze section was filled in:
  `6c276f85cdf52414aa1b3faa47cf1dbb2d867d1616cb82fdc207327bc1a2a45f`
- Public timestamp: the git commit that adds this section, pushed to github.com/krishna2882/Project-Neuroeco **before** any
  follow-up data were collected.
- **Status:** status changed from DRAFT to frozen. No further edits except Devansh's sign-off line.
