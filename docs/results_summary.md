# Results summary: three model families (updated 4 Nov 2026)

## Headline
**All three models recognise the counterpart's emotion almost perfectly (99–100%), but what that emotion does to
their economic decisions is model-specific and mostly small.** Of 42 planned emotion-vs-neutral tests, **5 survive
Holm correction across the whole study** and 8 survive FDR. Four of the five come from the large reasoning model
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

## Effects that survive correction across the whole study
| Model | Effect vs neutral message | Estimate [95% CI] | Holm (study) | FDR (study) |
|---|---|---|---|---|
| Mistral | S2 dictator: sad recipient → **more giving** | +24.6 pp [+17.9, +31.2] | < .001 | < .001 |
| Mistral | S3a trustee: happy investor → more returned | +13.7 pp [+8.3, +19.1] | < .001 | < .001 |
| Mistral | S3a trustee: sad investor → more returned | +12.0 pp [+6.6, +17.4] | .001 | < .001 |
| Mistral | S3a trustee: angry investor → more returned | +9.7 pp [+4.3, +15.2] | .018 | .003 |
| Qwen | S3b investor: angry trustee → **less sent** | −11.2 pp [−17.4, −5.1] | .014 | .003 |
| Qwen | S1 responder: sad proposer → less rejection | log-OR −0.95 [−1.65, −0.25] | n.s. | .040 |
| Mistral | S2 dictator: angry recipient → more giving | +9.6 pp [+3.0, +16.2] | n.s. | .026 |
| Mistral | S3b investor: happy trustee → more sent | +10.8 pp [+4.1, +17.6] | n.s. | .011 |

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
| T = 0.7 robustness (S1) | No change | No change | not run |

## Why the reasoning model gives more (its reasoning text, keyword-coded; exploratory)
From Mistral's 6,240 reasoning texts (`results/main/thinking.md`):
- Mentions of **empathy/sympathy track the emotion**: 75–96% of sad-condition trials, 24–73% angry, 23–41% happy,
  1–21% neutral, ≈ 0% no message.
- In the dictator game, trials whose reasoning mentions empathy give **22%** of the pie vs **6%** otherwise.
- **About 70% of trials reason about being in a study** ("typical human behaviour", "what is expected") and 96%
  explicitly weigh self-interest. The model reasons *about* the experimenter, which is a demand-characteristics risk
  to discuss.
- In 86–100% of sad trials it calls the message an **emotional appeal**, yet gives more anyway.

## Human benchmarks (no-message baseline)
| | Humans | Llama | Qwen | Mistral |
|---|---|---|---|---|
| UG offer | ≈ 40% | 40% | 50% | 38% |
| DG giving | ≈ 28% | 26% | 50% | 7% |
| TG sent | ≈ 50% | 41% | 44% | 0% |
| TG returned | ≈ 37% | 40% | 54% | 21% |

## Caveats
- **Emotion is confounded with life events** in the messages (sad = bereavement, happy = engagement). This is tested by the
  pre-registered follow-up with event-free messages (`docs/preregistration_followup.md`).
- The message set is a provisional freeze until the human peer rating is done; flagged messages get a sensitivity analysis.
- Mistral Large 4 always reasons, and it is open-weight (released 29 Oct 2026), not closed. H5 mixes family, scale and deliberation.
- Large prompt-wording effects (Llama: 26–80% acceptance across paraphrases), so generalisation rests on only 4 paraphrases.
- The MAO and Fehr–Schmidt α are identified only for Qwen-neutral (and Llama-sad, with a very wide CI); the computational-model
  aim is therefore only partly met.
- Mistral's checks are partial (106/468); Llama's first-run log-probs were re-collected after a parser fix (P6).
