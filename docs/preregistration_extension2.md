# Pre-registration: model scale, game comprehension and quantisation (extension 2)

**Status:** DRAFT, 12 Nov 2026. **Both** Krishna Goel and Devansh Magotra must approve it **before any extension-2 data are
collected**. On approval: record both names and the date in the Freeze section, compute the SHA-256 of this file as approved,
commit and push to github.com/krishna2882/Project-Neuroeco, and only then submit the Ada jobs.

**Written after** the main study, the pre-registered follow-up (`docs/preregistration_followup.md`) and the post-hoc
analyses P12 (message as a random factor) and P14 (equivalence tests, pooled estimates) were known. It adds new data to
answer three questions those results left open. The existing data and conclusions are not changed.

## 1. Questions and why
| Part | Question | Why it is open |
|---|---|---|
| **E1: scale** | Does emotion sensitivity change with model size **within one family**? | H5 (model differences) mixes family, size and reasoning: the only large model (Mistral Large 4) is also the only reasoning model and a different family. |
| **E2: comprehension** | Do Llama and Qwen understand the games' payoff rules? | Llama's acceptance barely depends on the offer (H1 fails). That is either a preference (ignores fairness) or a misunderstanding of the game; the data cannot tell these apart. |
| **E3: quantisation** | Are the Qwen effects artefacts of 4-bit compression? | All open models ran at Q4_K_M. |

The single effect that holds in both open models and in both message styles is **anger lowering trust** (Qwen S3b: main
−11.1 pp, follow-up −9.6 pp, pooled −10.1 pp [−14.4, −5.8]; Llama pooled −12.3 pp; `results/main/equivalence.md`). The
confirmatory hypotheses therefore target that effect.

## 2. Models (Ollama on Ada, GTX 1080 Ti, identical runtime and settings to the main study)
| Key | Ollama tag | Part | Size on disk (approx.) |
|---|---|---|---|
| `qwen25_3b` | `qwen2.5:3b-instruct-q4_K_M` | E1, E2 | 2 GB |
| `qwen25_14b` | `qwen2.5:14b-instruct-q4_K_M` | E1, E2 | 9 GB |
| `qwen25_7b_q8` | `qwen2.5:7b-instruct-q8_0` | E3 | 8 GB |
| `llama31_8b`, `qwen25_7b` (existing) | as in the main study | E2 only | already on Ada |

If a tag cannot be pulled, the nearest Q4_K_M/Q8_0 build of the same model is used and logged; no other substitution.

## 3. Design
**E1 (scale).** Qwen2.5-3B and Qwen2.5-14B run the **complete frozen main bank** (`data/scenarios/trials.jsonl`, 6,240
decisions incl. the 5%/45% cells) and the main manipulation checks (`checks.jsonl`, 468), with the same messages,
paraphrases, seeds, 3 samples and T = 1.0. S1 log-probabilities are collected as in the main study. Together with the
existing Qwen2.5-7B this gives a 3-point size ladder (3B, 7B, 14B) within one family.

**E3 (quantisation).** Qwen2.5-7B at Q8_0 runs the main-bank **S1 and S3b** trials (3,360 + 480 = 3,840 decisions) with the
same seeds; results are compared with the existing Q4_K_M run.

**E2 (comprehension).** A new bank `comprehension.jsonl`, with no messages, for `llama31_8b`, `qwen25_7b`, `qwen25_3b` and
`qwen25_14b`. Each item shows a game exactly as in the main study (the same 4 paraphrases, the same system prompt, the
no-message version) but replaces the final decision question with one comprehension question. The answer format is JSON
`{"answer": <whole number>}` or `{"answer": "yes" | "no"}`.

| Item | Game (template) | Question appended instead of the decision | Correct answer |
|---|---|---|---|
| C1 | S1 responder, offer 10% and 40% | "If you reject the proposal, how many rupees do you receive?" | 0 |
| C2 | S1 responder, offer 10% and 40% | "If you accept the proposal, how many rupees do you receive?" | the offer |
| C3 | S1 responder, offer 10% and 40% | "If you accept the proposal, how many rupees does Player A receive?" | pie − offer |
| C4 | S2-UG proposer | "If Player B rejects your proposal, how many rupees do you receive?" | 0 |
| C5 | S2-DG proposer | "Can Player B change how the money is divided? Answer yes or no." | no |
| C6 | S3b investor | "If you send INR {half of the endowment}, how many rupees does Player B receive?" | 3 × that amount |
| C7 | S3b investor | "Does Player B have to send any money back to you? Answer yes or no." | no |

Each item × 2 stakes (INR 100, 10,000) × 4 paraphrases × 3 samples (C1–C3 also × 2 offers): C1–C3 144, C4–C7 96, so
**240 items per model**. Scoring is automatic: a numeric answer must match exactly; yes/no is matched case-insensitively.

## 4. Confirmatory hypotheses
| ID | Model | Prediction | Test |
|---|---|---|---|
| X1 | Qwen2.5-14B | S3b: angry trustee **lowers** share sent vs neutral | one-sided |
| X2 | Qwen2.5-3B | S3b: angry trustee **lowers** share sent vs neutral | one-sided |
| X3 | Qwen2.5-7B Q8_0 | S3b: angry trustee **lowers** share sent vs neutral | one-sided |

**Decision rule:** each one-sided test at α = .05, **Holm-corrected across X1–X3**. Primary model = the stricter model of
P12 (`analysis/message_re.py`: original fixed effects + C(paraphrase) + (1 | message) + (1 | message:paraphrase), t with
df = #messages − #emotions); the original model (random intercept per variant) is reported alongside it.
- Significant: **replicated** at that size / precision.
- Not significant: we report the estimate with its 95% CI and whether it is **equivalent to zero** (90% CI inside ±5 pp),
  **inconclusive**, or reliably smaller than the Qwen-7B Q4 estimate (CI excludes −11.1 pp).

**E3 additionally (fixed in advance, not part of the Holm family):** Q8 − Q4 difference in the S3b anger effect with a 95% CI,
and a TOST against ±10 pp. If the 90% CI of the difference is within ±10 pp, we say the anger effect is "not a 4-bit artefact".
Expected precision is limited (each estimate has SE ≈ 3.6 pp), so a narrower bound is not claimed.

**E2 interpretation (fixed in advance):** accuracy per item and model, with Wilson 95% CIs.
- Llama's flat acceptance curve is attributed to **misunderstanding** if its accuracy on C1–C3 is < 80%, and to a
  **preference** (the rules are understood but fairness is not used) if ≥ 90%. Between 80% and 90%: inconclusive.
- The same thresholds are applied to every model and item; any model below 80% on an item is flagged as "game not reliably
  understood" next to its results for that game.

## 5. Exploratory (labelled as such in the write-up)
- All other emotion × sub-experiment effects for 3B and 14B; H1–H4 for each size; MAO and Fehr–Schmidt α where identified.
- **Size trend:** emotion effects and manipulation-check recognition across 3B → 7B → 14B (three points, so descriptive only).
- Equivalence classes (P14 bounds: ±5 pp / OR 1.5 and ±10 pp / OR 2) for the new models.
- Q8 vs Q4: decision agreement on identical prompts and seeds (% identical decisions) for S1 and S3b.
- Whether comprehension accuracy differs by paraphrase.

## 6. Data handling and stopping
Exactly as in the main study (`docs/protocol_decisions.md`): every attempt logged; off-format outputs re-asked up to 3 times;
the first valid attempt is analysed; failure rates are reported. Each run collects the full bank once; a crashed job is
resumed (completed trials are skipped) but **no data are added beyond the banks above**, and nothing is re-run because of
its results. No messages, prompts or banks are changed after approval.

## 7. Feasibility
GPU time on Ada (from earlier jobs: about 30 min per 4,000 decisions for a 7B model): E1 3B ≈ 0.5 h, E1 14B ≈ 2 h, E3 ≈ 0.5 h,
E2 ≈ 10 min per model. Storage: about 19 GB of new model files, with 26 GB free in the 50 GB home quota.

## Freeze
- Approved by: _(both names and date)_
- SHA-256 of this file as approved (before this section is filled in): _(to be recorded)_
- Public timestamp: the commit adding this section, pushed **before** any extension-2 data are collected.
