# Results summary: three model families (updated 13 Nov 2026)

## Headline
**All three models recognise the counterpart's emotion almost perfectly (99–100%), but what that emotion does to
their economic decisions is model-specific and mostly small.** Of 42 planned emotion-vs-neutral tests, **5 survive
Holm correction across the whole study** and 8 survive FDR. When message is treated as a random factor (the stricter,
preferred analysis, P12), **4 survive Holm** and 10 survive FDR. Four of the five (all four under the stricter model) come from the large reasoning model
(Mistral Large 4), whose emotion sensitivity shows up in **generosity** (giving and returning), not in rejecting unfair
offers. No effect replicates in all three models, and no model uses anger strategically (H4).

| Model | Family | Size | Runtime | Notes |
|---|---|---|---|---|
| **Llama-3.1-8B-Instruct** | Meta | 8B | Ollama Q4_K_M on Ada | log-probs collected |
| **Qwen2.5-7B-Instruct** | Alibaba | 7B | Ollama Q4_K_M on Ada | log-probs collected |
| **Mistral Large 4** | Mistral AI | ~1T MoE | Mistral API (free tier) | always reasons (`reasoning_effort="low"`); no log-probs |

Each model made 6,240 decisions (110 cells + the 5%/45% fallback cells × 16 prompt variants × 3 samples; T = 1.0).
All 18,720 decisions are valid, with no refusals. Manipulation checks: 468 for Llama and for Qwen; 106 for Mistral
(budget exhausted; P9). Full tables: `results/main/report.md`. All effects with study-wide correction:
`results/main/forest.md` and `results/main/fig_forest.png`. Deviations: `docs/plan_update.md`.

## Pre-registered follow-up: emotion or life event? (12 Nov 2026)
The main messages tied each emotion to a life event (sad = bereavement). A pre-registered follow-up with **event-free**
messages (bodily and behavioural cues only; 100% recognised) on Llama and Qwen found:
- **Anger reducing trust replicates** (Qwen S3b: −9.6 pp vs −11.2 pp; Holm p = .003, also .003 with message as a random
  factor), so it is an emotion effect. In the main study alone it is FDR- but not Holm-significant under the stricter model;
  the independent replication is what makes it the study's most solid open-model effect.
- **Sadness reducing rejection does not** (Qwen S1: log-OR −0.13 vs −0.95; the CI excludes the main estimate), so it was at
  least partly an effect of the *event* (sympathy for a loss), not of sadness itself.
- Exploratory: event-free *happy* messages raised generosity (Llama S3b +21 pp; Qwen DG +6.5 pp), which is new and not predicted.
Details: `results/followup/confirmatory.md`.

## Is there no effect, or just too much noise? (equivalence tests and pooling, 12 Nov; P14, post hoc)
`results/main/equivalence.md`. Equivalence = 90% CI inside ±10 pp (or OR 2); the stricter ±5 pp / OR 1.5 version is also there.
- **Qwen's emotion sensitivity is narrow, and that is now a positive finding:** 11 of its 15 main-study effects and 10 of 12
  follow-up effects are *equivalent to zero*. It recognises every emotion but acts on almost none of them.
- **The one robust open-model effect is anger lowering trust.** Pooled over 10 messages and both message styles, Qwen
  −10.1 pp [−14.4, −5.8] (Holm p = .001; the two studies agree, heterogeneity p = .74). Llama shows the same direction
  (−12.3 pp, FDR p = .023; Holm .081).
- **Llama is mostly inconclusive** (12 of 15 main effects at ±5 pp): too noisy to show either an effect or its absence.
  Its happy → rejection effect reverses between message styles (heterogeneity p < .001), so it depends on the wording, not on
  the emotion.
- Not pre-registered and the bounds were chosen after the fact: present as a secondary analysis.

## Extension 2: model size, game comprehension, quantisation (pre-registered, 13 Nov 2026)
Pre-registration `docs/preregistration_extension2.md` (frozen and approved by both authors before data collection).
Full results: `results/ext2/confirmatory.md`. Primary model = message as a random factor (P12); one-sided, Holm over X1–X3.
- **Anger lowering trust replicates in all three new Qwen variants** (S3b, angry vs neutral):
  Qwen2.5-14B −16.5 pp [−25.9, −7.0], Holm p = .001 (X1); Qwen2.5-3B −22.5 pp [−33.7, −11.3], Holm p = .001 (X2);
  Qwen2.5-7B at Q8 −14.3 pp [−21.7, −6.9], Holm p = .001 (X3). Together with the main study and the follow-up, this is the
  one effect that holds across sizes, precisions and message styles.
- **Not a 4-bit artefact in direction, but the size is not pinned down:** Q8 − Q4 = −3.2 pp [−14.1, +7.7]; the TOST against
  ±10 pp is not significant (p = .10), so a 10 pp quantisation difference cannot be ruled out. Q8 and Q4 make the identical
  decision on the same prompt and seed in 94% of S1 trials but only 52% of S3b trials: quantisation changes individual
  amounts while the aggregate effect stays.
- **Comprehension (E2):** Llama answers C1–C3 (ultimatum payoffs) 100% correctly, so by the pre-registered rule its flat
  acceptance curve is a **preference** (it knows the payoffs and does not act on fairness), not a misunderstanding.
  Qwen 7B and 14B are near 100% on every item.
- **Flagged (< 80%):** Llama C7 (17%) and Qwen-3B C7 (29%) say the trustee *has to* send money back, although the
  prompt says it "can be anything from nothing to all of it"; Qwen-3B also fails C3 (77%). So for **Llama and Qwen-3B the trust
  game is not reliably understood**, and their trust results should carry that caveat. The anger effect still appears in
  both, so it does not depend on understanding that repayment is voluntary.
- Exploratory size trend (3B → 7B → 14B): 3B reacts to anger in most games (UG, S3a, S1 rejection; FDR < .05); 7B
  only in trust; 14B mainly to sadness (more giving and returning, less rejection) plus anger in trust. No monotone
  trend in overall sensitivity, so model size does not simply amplify or dampen emotion effects. Emotion recognition:
  98–100% at every size.

## Human message ratings and sensitivity analyses (13 Nov 2026)
9 anonymous raters rated all 52 messages (`results/peer_rating_summary.md`). Pre-specified flag: recognised as intended
by < 70% of raters, or read as a threat/promise by >= 30%.
- **Recognition:** 88–96% per emotion; every frozen message is recognised by >= 78% of raters. The messages work for people too.
- **Human benchmark (would this message make you give less / the same / more, -1 to +1):** sad +0.62, angry +0.36,
  happy -0.04 (main set); people say they would give *more* to an angry writer, whereas the models trust angry
  partners *less*.
- **Flagged (all for threat, at 3–6 of 9 raters):** main A3, A4; follow-up: all five frozen anger messages (FA2, FA3, FA4, FA6, FA7).
- **Main study without A3, A4** (`results/main_excl/`): Mistral's generosity effects hold and get stronger (Holm survivors under the
  stricter model 4 → 5). Anger → trust: Qwen −11.1 → −6.6 pp [−12.8, −0.5], Llama −14.3 → −13.8 pp; with 3 anger messages left
  neither is FDR-significant (p = .145). FDR survivors 10 → 5.
- **Follow-up without the flagged messages** (`results/followup_excl/`): F1 unchanged (−0.13 [−0.51, +0.26]; still not supported).
  F2 cannot be tested (no anger message left), so the pre-registered sensitivity analysis cannot speak to it. The exploratory happy
  effects are unchanged (Llama happy → rejection +0.73, Holm p = .006).
- **Is it threat rather than anger? Probably not** (`results/threat/threat.md`, exploratory, post hoc). Across the 10 anger
  messages the models saw, the trust drop does not grow with the threat rating: −1.4 pp per +10 points of threat [−4.0, +1.3],
  p = .32; Spearman ρ = −0.14. The least threatening message (A2, 11%) still lowers trust by −11.7 pp on average. The drop in the
  main sensitivity analysis comes from losing two strong messages while A7, which has almost no effect, stays: between-message
  variability again, not threat. With 10 messages, all at least slightly threatening, this is suggestive only.

## The models' valuation curves and the neuroeconomic analogy (13 Nov 2026; P18, exploratory)
`results/value_signal/value_signal.md` and `fig_value_curves.png`; mapping to the human literature: `docs/neuro_mapping.md`.
- **The log-probability of "accept" is a valid graded value signal:** it is calibrated against the sampled choices in all 7 runs
  (Llama r ≈ .5 because its P(accept) sits near .5; Qwen r ≈ .95). Choices are slightly more extreme than P at the ends, which suggests
  the sampler truncates unlikely tokens.
- **Anger lowers the value of accepting in every run** (7 of 7 negative; Qwen −1.1 to −2.2 logit at a 30% offer). For Qwen-7B the
  offer needed for a 50% chance of acceptance (the MAO analogue) rises from 22% to 51% of the pie (Q4) and from 17% to 50% (Q8).
  No single test survives Holm across 21, so the evidence is a consistent direction, not a confirmed effect.
- **Qwen-14B: sad messages make offers acceptable regardless of fairness** (+4.08 logit, slope −7.0; both Holm p = .003).
  **Llama follow-up: happy messages lower acceptance** (−0.79, Holm p < .001), matching the choice-based result.
- Llama's curve is nearly flat, and Qwen-3B's never crosses 50%, so their MAO is not identified; this is the same limit as the
  choice-based Fehr–Schmidt fit.

## Wording vs emotion, and the pooled valuation model (13 Nov 2026; P19, exploratory)
**Prompt wording moves decisions more than emotion does** (`results/wording/wording.md`, `fig_wording.png`). Sequential
adjusted R², with wording (4 paraphrases, 3 df) compared like for like with emotion (3 df):
- **Wording explains more variance than emotion in 21 of 28 model × game combinations.** Median: wording 6.7%, emotion 6.1%,
  which message within an emotion 4.1%; the rest is mostly sampling noise at T = 1.0 (median about 75%).
- The extreme case is Llama in the ultimatum game: wording 10.6% vs emotion 0.4%; acceptance spans 49 pp across the four
  paraphrases.
- **The exceptions are where the robust effect lives:** trust-game sending in Qwen-14B (emotion 54%), Qwen-7B Q8 and Llama's
  follow-up, where emotion beats wording.
- Which message within an emotion matters about as much as the emotion itself, consistent with P12.

**Pooled valuation model across all 7 log-probability runs** (`results/value_signal/pooled.md`; message, run × message and
run × emotion random effects; conservative t with df = 6):
- Anger: −1.13 logit at a 30% offer [−2.52, +0.25], p = .09 (z: p = .045). The same direction in every run, but the runs
  differ too much for a pooled claim. **Report as a trend.**
- **Sadness flattens the valuation curve**: slope on the offer −2.54 [−3.77, −1.30], Holm p = .014 (Qwen only: Holm
  p = .039). After a sad message the size of the offer matters less: the models become less sensitive to fairness.

## Effects that survive correction across the whole study
Two analyses: the original (random intercept per paraphrase × message cell) and the stricter one with **message as a
random factor** (`results/main/message_re.md`, P12). Each emotion is carried by only 5 messages, so the stricter model is
the one to base claims on.

| Model | Effect vs neutral message | Estimate [95% CI] | Holm (study) | FDR (study) | Holm / FDR, message as random factor |
|---|---|---|---|---|---|
| Mistral | S2 dictator: sad recipient → **more giving** | +24.6 pp [+17.9, +31.2] | < .001 | < .001 | **< .001** / < .001 |
| Mistral | S3a trustee: happy investor → more returned | +13.7 pp [+8.3, +19.1] | < .001 | < .001 | **.004** / .002 |
| Mistral | S3a trustee: sad investor → more returned | +12.0 pp [+6.6, +17.4] | .001 | < .001 | **.016** / .006 |
| Mistral | S3a trustee: angry investor → more returned | +9.7 pp [+4.3, +15.2] | .018 | .003 | .099 / .022 |
| Qwen | S3b investor: angry trustee → **less sent** | −11.2 pp [−17.4, −5.1] | .014 | .003 | .241 / .046 (but **replicated** in the pre-registered follow-up, F2) |
| Qwen | S1 responder: sad proposer → less rejection | log-OR −0.95 [−1.65, −0.25] | n.s. | .040 | .752 / .085 |
| Mistral | S2 dictator: angry recipient → more giving | +9.6 pp [+3.0, +16.2] | n.s. | .026 | **.047** / .013 |
| Mistral | S3b investor: happy trustee → more sent | +10.8 pp [+4.1, +17.6] | n.s. | .011 | .516 / .062 |

Under the stricter model, Llama S3b angry and sad (−14 pp each) and Mistral DG happy and UG angry also reach FDR < .05
(not Holm). Messages differ little within an emotion (SD of message intercepts 2–5 pp; ≈ 0.4 logit for Qwen S1), so
estimates barely move; what changes is the uncertainty.

Effects reported earlier that **do not survive study-wide correction**: Qwen S1 angry → more rejection (p = .014);
Llama S3b angry and sad → less sent (p ≈ .01–.02). Present them as suggestive only.

## Hypotheses, model by model
| | Llama-3.1-8B | Qwen2.5-7B | Mistral Large 4 |
|---|---|---|---|
| **H1** UG: acceptance rises with offer | Choices: no. Log-probs: weak (p = .014) | **Yes** (p < .001); MAO (neutral) ≈ 25%; Fehr–Schmidt α = 0.49 [0.17, 1.01] | **Ceiling**: accepts ≈ all offers ≥ 10%; 95% even at 5% |
| **H3** S1 emotion shifts acceptance | No | Sad → less rejection (FDR-significant); angry → more (nominal only) | Not testable (ceiling) |
| **H3** giving / reciprocity | No (after correction) | Angry trustee → less trust (S3b) | Sad (and angry) recipients get more in the DG; every emotion raises returns in the TG vs neutral |
| **H4** strategic anger | No | No | No; the Emotion × Game effect is driven by **sadness** (DG ≫ UG) |
| UG − DG gap, neutral message | +7 pp, n.s. | +1.5 pp, n.s. | **+37 pp** (UG 41% vs DG 3%) |
| **H2** returns rise with amount sent | n.s. | Reversed (p = .001) | **Yes** (p < .001) |
| **H5** model differences | Emotion × Model significant in **every** sub-experiment (all p < .001) | | |
| T = 0.7 robustness (whole bank, P20) | Same direction, weaker anger → trust (−9.2 pp) | Unchanged (anger → trust −11.5 pp) | not run |

## Why the reasoning model gives more (its reasoning text, keyword-coded; exploratory)
From Mistral's 6,240 reasoning texts (`results/main/thinking.md`):
- Mentions of **empathy/sympathy track the emotion**: 75–96% of sad-condition trials, 24–73% angry, 23–41% happy,
  1–21% neutral, ≈ 0% no message.
- In the dictator game, trials whose reasoning mentions empathy give **22%** of the pie vs **6%** otherwise.
- **About 70% of trials reason about being in a study** ("typical human behaviour", "what is expected") and 96%
  explicitly weigh self-interest. The model reasons *about* the experimenter, which is a demand-characteristics risk
  to discuss.
- In 86–100% of sad trials it calls the message an **emotional appeal**, yet gives more anyway.

## What the models say about their decisions (qualitative coding by both authors, 13 Nov; P21)
Both authors independently coded a stratified 10% sample of the one-line justifications (375; 125 per main-study model;
coders blind to model and condition) for mentions of the counterpart's **emotion**, **fairness** and **strategy**
(`results/qual_coding/`). **Agreement is high:** Cohen's κ = 0.83 (emotion), 0.87 (fairness), 0.79 (strategy), n = 368.
Final codes count a mention only if both coders marked it; the by-condition results below are exploratory.
- **The models talk about the emotion they were shown.** Emotion mentions rise after angry/sad/happy messages compared
  with neutral or no message: Llama 47% vs 17%, Qwen 41% vs 4% (Holm p ≤ .004); Mistral 18% vs 4% (p = .026, Holm .063).
- **Fairness goes with rejection.** Llama mentions fairness in 76% of its S1 rejections vs 11% of acceptances (Holm
  p < .001); Qwen 55% vs 25% (p = .021, Holm .063). Mistral accepted every offer in the sample.
- **Different styles:** Mistral's justifications are mostly strategic (75%), Qwen's mostly fairness-based (42%), and
  Llama's mention emotion most often (36%).
- **No sign of strategic reasoning about the veto:** strategy mentions are not higher in the ultimatum than in the dictator
  game (41% vs 53%, p = .44), consistent with the absence of strategic anger (H4).
- Justifications come *after* the decision and may be post-hoc rationalisations; they show what the models report, not
  what drove the choice.

## Human benchmarks (no-message baseline)
| | Humans | Llama | Qwen | Mistral |
|---|---|---|---|---|
| UG offer | ≈ 40% | 40% | 50% | 38% |
| DG giving | ≈ 28% | 26% | 50% | 7% |
| TG sent | ≈ 50% | 41% | 44% | 0% |
| TG returned | ≈ 37% | 40% | 54% | 21% |

## Caveats
- **Emotion is confounded with life events** in the main messages. The pre-registered follow-up shows that this matters for sadness
  (S1 effect not replicated) but not for anger (S3b replicated).
- **Anger is partly confounded with perceived threat** in the human ratings (main A3, A4; all five frozen follow-up anger messages flagged
  at >= 3 of 9 raters). An exploratory check finds no link between threat ratings and the size of the trust drop, but all 10 anger
  messages were at least somewhat threatening. A pre-registered test with non-threatening anger (extension 3) was frozen but **not
  run** (P17).
- Human ratings: 9 raters, the pre-registered minimum was 8; flags at the 30% threat cut-off rest on 3 of 9 raters.
- Mistral Large 4 always reasons, and it is open-weight (released 29 Oct 2026), not closed. H5 mixes family, scale and deliberation.
- Large prompt-wording effects (Llama: 26–80% acceptance across paraphrases), so generalisation rests on only 4 paraphrases.
- The MAO and Fehr–Schmidt α are identified only for Qwen-neutral (and Llama-sad, with a very wide CI); the computational-model
  aim is therefore only partly met.
- Mistral's checks are partial (106/468); Llama's first-run log-probs were re-collected after a parser fix (P6).
