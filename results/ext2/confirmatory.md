# Extension 2: pre-registered results (scale, comprehension, quantisation)

Pre-registration: `docs/preregistration_extension2.md` (frozen 12 Nov 2026, approved by both authors before data collection, SHA-256 dcf5acc4…). Primary model: message as a random factor (P12); one-sided t, Holm over X1-X3.

## Confirmatory: does anger lower trust (S3b) in each new model?

| id | model | estimate [95% CI] | original model [95% CI] | p_one_sided | p_holm | outcome |
|---|---|---|---|---|---|---|
| X1 | Qwen2.5-14B | -16.5 [-25.9, -7.0] | -17.2 [-22.4, -12.0] | 0.0014 | 0.0014 | **Replicated** |
| X2 | Qwen2.5-3B | -22.5 [-33.7, -11.3] | -22.5 [-33.2, -11.9] | 0.0004 | 0.0013 | **Replicated** |
| X3 | Qwen2.5-7B (Q8) | -14.3 [-21.7, -6.9] | -14.7 [-19.7, -9.7] | 0.0006 | 0.0013 | **Replicated** |

## E3: is the anger effect a 4-bit artefact? (fixed in advance; not in the Holm family)

Q8 -14.3 pp vs Q4 -11.1 pp; difference -3.2 pp [95% CI -14.1, +7.7; 90% CI -12.2, +5.8], TOST vs ±10 pp p = 0.104 → **cannot rule out** a quantisation difference of 10 pp

Exploratory: identical decisions on identical prompts and seeds (Q8 vs Q4):

| sub_exp | n | identical | mean_abs_diff |
|---|---|---|---|
| S1 | 3360 | 0.939 |  |
| S3b | 480 | 0.523 | 272.821 |

## E2: do the models understand the games?

Llama C1-C3 accuracy 100.0% [97.4%, 100.0%] → **preference**: Llama understands the payoff rules, so its flat acceptance curve reflects not using fairness, not a misunderstanding (rule fixed in the pre-registration).

| item | Llama-3.1-8B | Qwen2.5-14B | Qwen2.5-3B | Qwen2.5-7B (Q4) |
|---|---|---|---|---|
| C1 | 1.000 | 1.000 | 1.000 | 1.000 |
| C2 | 1.000 | 1.000 | 1.000 | 1.000 |
| C3 | 1.000 | 1.000 | 0.771 | 1.000 |
| C4 | 0.833 | 1.000 | 0.917 | 1.000 |
| C5 | 0.958 | 1.000 | 1.000 | 1.000 |
| C6 | 1.000 | 1.000 | 1.000 | 1.000 |
| C7 | 0.167 | 1.000 | 0.292 | 0.958 |

Wilson 95% CIs and flags (< 80% = game not reliably understood):

| model | item | n | accuracy | ci_lo | ci_hi | flag |
|---|---|---|---|---|---|---|
| Llama-3.1-8B | C1 | 48 | 1.000 | 0.926 | 1.000 |  |
| Llama-3.1-8B | C2 | 48 | 1.000 | 0.926 | 1.000 |  |
| Llama-3.1-8B | C3 | 48 | 1.000 | 0.926 | 1.000 |  |
| Llama-3.1-8B | C4 | 24 | 0.833 | 0.641 | 0.933 |  |
| Llama-3.1-8B | C5 | 24 | 0.958 | 0.798 | 0.993 |  |
| Llama-3.1-8B | C6 | 24 | 1.000 | 0.862 | 1.000 |  |
| Llama-3.1-8B | C7 | 24 | 0.167 | 0.067 | 0.359 | game not reliably understood |
| Qwen2.5-14B | C1 | 48 | 1.000 | 0.926 | 1.000 |  |
| Qwen2.5-14B | C2 | 48 | 1.000 | 0.926 | 1.000 |  |
| Qwen2.5-14B | C3 | 48 | 1.000 | 0.926 | 1.000 |  |
| Qwen2.5-14B | C4 | 24 | 1.000 | 0.862 | 1.000 |  |
| Qwen2.5-14B | C5 | 24 | 1.000 | 0.862 | 1.000 |  |
| Qwen2.5-14B | C6 | 24 | 1.000 | 0.862 | 1.000 |  |
| Qwen2.5-14B | C7 | 24 | 1.000 | 0.862 | 1.000 |  |
| Qwen2.5-3B | C1 | 48 | 1.000 | 0.926 | 1.000 |  |
| Qwen2.5-3B | C2 | 48 | 1.000 | 0.926 | 1.000 |  |
| Qwen2.5-3B | C3 | 48 | 0.771 | 0.635 | 0.867 | game not reliably understood |
| Qwen2.5-3B | C4 | 24 | 0.917 | 0.742 | 0.977 |  |
| Qwen2.5-3B | C5 | 24 | 1.000 | 0.862 | 1.000 |  |
| Qwen2.5-3B | C6 | 24 | 1.000 | 0.862 | 1.000 |  |
| Qwen2.5-3B | C7 | 24 | 0.292 | 0.149 | 0.492 | game not reliably understood |
| Qwen2.5-7B (Q4) | C1 | 48 | 1.000 | 0.926 | 1.000 |  |
| Qwen2.5-7B (Q4) | C2 | 48 | 1.000 | 0.926 | 1.000 |  |
| Qwen2.5-7B (Q4) | C3 | 48 | 1.000 | 0.926 | 1.000 |  |
| Qwen2.5-7B (Q4) | C4 | 24 | 1.000 | 0.862 | 1.000 |  |
| Qwen2.5-7B (Q4) | C5 | 24 | 1.000 | 0.862 | 1.000 |  |
| Qwen2.5-7B (Q4) | C6 | 24 | 1.000 | 0.862 | 1.000 |  |
| Qwen2.5-7B (Q4) | C7 | 24 | 0.958 | 0.798 | 0.993 |  |

First-attempt valid-output rate: Llama-3.1-8B 100.0%, Qwen2.5-14B 100.0%, Qwen2.5-3B 100.0%, Qwen2.5-7B (Q4) 100.0%

Exploratory: accuracy by paraphrase

| model_key | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| llama31_8b | 0.900 | 0.867 | 0.917 | 0.900 |
| qwen25_14b | 1.000 | 1.000 | 1.000 | 1.000 |
| qwen25_3b | 0.917 | 0.733 | 0.950 | 0.900 |
| qwen25_7b | 0.983 | 1.000 | 1.000 | 1.000 |

## Exploratory: size trend within Qwen (3B → 7B → 14B), stricter model; * = study-wide FDR < .05 in this analysis

| test | emotion | Qwen2.5-3B | Qwen2.5-7B (Q4) | Qwen2.5-14B |
|---|---|---|---|---|
| S1 rejection (log-OR) | angry | +1.79* | +0.86 | +0.15 |
| S1 rejection (log-OR) | happy | -0.67 | -0.47 | -1.11* |
| S1 rejection (log-OR) | sad | -1.54* | -0.91 | -3.38* |
| S2 giving (DG) (pp) | angry | -13.96 | -5.02 | -3.79 |
| S2 giving (DG) (pp) | happy | +4.68 | +3.58 | +1.42 |
| S2 giving (DG) (pp) | sad | +4.29 | -2.80 | +6.17* |
| S2 giving (UG) (pp) | angry | -20.21* | -5.44 | -0.86 |
| S2 giving (UG) (pp) | happy | +5.10 | +1.24 | +1.65 |
| S2 giving (UG) (pp) | sad | -4.20 | -3.17 | +5.77* |
| S3a returned (pp) | angry | -19.26* | -2.83 | -4.72 |
| S3a returned (pp) | happy | +3.68 | +1.83 | +2.63 |
| S3a returned (pp) | sad | -13.58 | -1.54 | +6.46* |
| S3b sent (pp) | angry | -22.50* | -11.08* | -16.47* |
| S3b sent (pp) | happy | -7.81 | -0.07 | +8.27 |
| S3b sent (pp) | sad | -14.50 | -1.67 | +12.28 |

## Exploratory: emotion recognition in the manipulation checks

| model | recognition | n |
|---|---|---|
| Qwen2.5-3B | 0.983 | 416 |
| Qwen2.5-7B (Q4) | 1.000 | 416 |
| Qwen2.5-14B | 1.000 | 416 |

## Exploratory: equivalence classes (lenient bounds ±10 pp / OR 2)

| model | equivalent to zero | inconclusive | real | small but real |
|---|---|---|---|---|
| qwen25_14b | 7 | 2 | 4 | 2 |
| qwen25_3b | 0 | 10 | 5 | 0 |
| qwen25_7b | 11 | 3 | 1 | 0 |
| qwen25_7b_q8 | 1 | 4 | 1 | 0 |

Full tables: `report.md`, `forest.md`, `message_re.md` in this folder.