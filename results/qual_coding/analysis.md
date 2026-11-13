# Qualitative coding: final codes and exploratory analysis

368 justifications coded by both authors (rows either coder left undecided are excluded).
Inter-rater agreement (before any consensus): see `kappa.txt`.
**Final codes (fixed in advance):** a code is present only if *both* coders marked it (primary);
*either* coder marking it is reported as a sensitivity check. Everything below is exploratory.

## Primary: both coders

### Prevalence by model (95% Wilson CI)

| Model | n | emotion | fairness | strategy |
|---|---|---|---|---|
| llama31_8b | 120 | 36% [28%, 45%] | 22% [16%, 31%] | 57% [49%, 66%] |
| mistral | 125 | 13% [8%, 20%] | 26% [19%, 34%] | 75% [67%, 82%] |
| qwen25_7b | 123 | 26% [19%, 34%] | 42% [34%, 51%] | 40% [32%, 49%] |

### Emotion mentions by message condition

| Model | none | neutral | angry | sad | happy |
|---|---|---|---|---|---|
| llama31_8b | 2/23 | 6/23 | 11/26 | 12/24 | 12/24 |
| mistral | 1/23 | 1/26 | 5/26 | 6/25 | 3/25 |
| qwen25_7b | 1/23 | 1/26 | 12/26 | 11/24 | 7/24 |

### Exploratory tests (Fisher's exact, two-sided; Holm across these 6)

| Test | a | b | p | p (Holm) |
|---|---|---|---|---|
| llama31_8b: emotion code, emotional msg (a) vs neutral/none (b) | 35/74 | 8/46 | < .001 | 0.004 |
| mistral: emotion code, emotional msg (a) vs neutral/none (b) | 14/76 | 2/49 | 0.026 | 0.063 |
| qwen25_7b: emotion code, emotional msg (a) vs neutral/none (b) | 30/74 | 2/49 | < .001 | < .001 |
| all models, S2: strategy code, UG (a) vs DG (b) | 12/29 | 17/32 | 0.444 | 0.444 |
| llama31_8b, S1: fairness code, reject (a) vs accept (b) | 13/17 | 5/46 | < .001 | < .001 |
| qwen25_7b, S1: fairness code, reject (a) vs accept (b) | 17/31 | 8/32 | 0.021 | 0.063 |

## Sensitivity: either coder

### Prevalence by model (95% Wilson CI)

| Model | n | emotion | fairness | strategy |
|---|---|---|---|---|
| llama31_8b | 120 | 48% [40%, 57%] | 29% [22%, 38%] | 69% [60%, 77%] |
| mistral | 125 | 16% [11%, 23%] | 33% [25%, 41%] | 84% [77%, 89%] |
| qwen25_7b | 123 | 31% [23%, 40%] | 46% [37%, 54%] | 49% [40%, 58%] |

### Emotion mentions by message condition

| Model | none | neutral | angry | sad | happy |
|---|---|---|---|---|---|
| llama31_8b | 3/23 | 7/23 | 17/26 | 17/24 | 14/24 |
| mistral | 2/23 | 1/26 | 7/26 | 7/25 | 3/25 |
| qwen25_7b | 2/23 | 1/26 | 13/26 | 14/24 | 8/24 |

### Exploratory tests (Fisher's exact, two-sided; Holm across these 6)

| Test | a | b | p | p (Holm) |
|---|---|---|---|---|
| llama31_8b: emotion code, emotional msg (a) vs neutral/none (b) | 48/74 | 10/46 | < .001 | < .001 |
| mistral: emotion code, emotional msg (a) vs neutral/none (b) | 17/76 | 3/49 | 0.023 | 0.068 |
| qwen25_7b: emotion code, emotional msg (a) vs neutral/none (b) | 35/74 | 3/49 | < .001 | < .001 |
| all models, S2: strategy code, UG (a) vs DG (b) | 18/29 | 18/32 | 0.795 | 0.795 |
| llama31_8b, S1: fairness code, reject (a) vs accept (b) | 14/17 | 9/46 | < .001 | < .001 |
| qwen25_7b, S1: fairness code, reject (a) vs accept (b) | 17/31 | 9/32 | 0.042 | 0.084 |

Note: Mistral accepted every S1 offer in this sample, so the fairness-by-decision test is not run for it.
Cells are small (e.g. 11 DG rows per model); treat these results as descriptive.
