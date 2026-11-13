# Emotion effects with message as a random factor (followup_excl)

Model: original fixed effects + C(paraphrase) + (1 | message) + (1 | message:paraphrase). p values: t with df = #message groups - #emotion levels (emotion varies between messages); Holm and BH across the whole study, as in `forest.md`. Script: `analysis/message_re.py` (P12).

- Holm-significant study-wide: **1 → 1**
- FDR-significant study-wide: **2 → 1**

## Effects significant (FDR or Holm) in either analysis

| model | test | emotion | original [95% CI] | with message RE [95% CI] | Holm old | Holm new | FDR old | FDR new |
|---|---|---|---|---|---|---|---|---|
| llama31_8b | S1 rejection (log-OR) | happy | +0.73 [+0.12, +1.33] | +0.72 [+0.43, +1.01] | 0.243 | 0.006 | 0.075 | 0.006 |
| llama31_8b | S3b sent (pp) | happy | +20.83 [+9.35, +32.31] | +20.46 [+6.24, +34.67] | 0.006 | 0.216 | 0.006 | 0.082 |
| qwen25_7b | S2 giving (DG) (pp) | happy | +6.48 [+2.09, +10.86] | +6.42 [+2.19, +10.64] | 0.057 | 0.173 | 0.030 | 0.082 |

## Between-message variability (SD of message intercepts; S1 on logit scale, others in pp)

| model | test | sd_msg | sd_msg_para | df |
|---|---|---|---|---|
| llama31_8b | S1 rejection (log-OR) | 0.12 | 0.12 | 12 |
| llama31_8b | S2 giving (DG) (pp) | 3.28 | 4.89 | 12 |
| llama31_8b | S2 giving (UG) (pp) | 3.28 | 4.89 | 12 |
| llama31_8b | S3b sent (pp) | 8.11 | 7.48 | 12 |
| qwen25_7b | S1 rejection (log-OR) | 0.12 | 0.44 | 12 |
| qwen25_7b | S2 giving (DG) (pp) | 1.49 | 5.37 | 12 |
| qwen25_7b | S2 giving (UG) (pp) | 1.49 | 5.37 | 12 |
| qwen25_7b | S3b sent (pp) | 0.00 | 5.66 | 12 |

## All tests

| model | test | emotion | est_old | p_old | est_new | se_new | p_z | p_t | p_holm_study | p_bh_study |
|---|---|---|---|---|---|---|---|---|---|---|
| llama31_8b | S1 rejection (log-OR) | happy | 0.726 | 0.019 | 0.725 | 0.148 | 0.000 | 0.000 | 0.006 | 0.006 |
| llama31_8b | S1 rejection (log-OR) | sad | 0.200 | 0.509 | 0.192 | 0.145 | 0.185 | 0.210 | 1.000 | 0.549 |
| llama31_8b | S2 giving (DG) (pp) | happy | 4.087 | 0.488 | 4.237 | 5.537 | 0.444 | 0.459 | 1.000 | 0.667 |
| llama31_8b | S2 giving (DG) (pp) | sad | 11.304 | 0.055 | 11.411 | 5.521 | 0.039 | 0.061 | 0.733 | 0.195 |
| llama31_8b | S2 giving (UG) (pp) | happy | 6.866 | 0.244 | 6.842 | 5.537 | 0.217 | 0.240 | 1.000 | 0.549 |
| llama31_8b | S2 giving (UG) (pp) | sad | 5.305 | 0.368 | 5.213 | 5.521 | 0.345 | 0.364 | 1.000 | 0.647 |
| llama31_8b | S3b sent (pp) | happy | 20.831 | 0.000 | 20.457 | 7.251 | 0.005 | 0.015 | 0.216 | 0.082 |
| llama31_8b | S3b sent (pp) | sad | -0.491 | 0.933 | -0.283 | 7.246 | 0.969 | 0.969 | 1.000 | 0.969 |
| qwen25_7b | S1 rejection (log-OR) | happy | 0.031 | 0.888 | 0.032 | 0.194 | 0.870 | 0.873 | 1.000 | 0.931 |
| qwen25_7b | S1 rejection (log-OR) | sad | -0.131 | 0.548 | -0.127 | 0.195 | 0.516 | 0.528 | 1.000 | 0.704 |
| qwen25_7b | S2 giving (DG) (pp) | happy | 6.476 | 0.004 | 6.416 | 2.155 | 0.003 | 0.012 | 0.173 | 0.082 |
| qwen25_7b | S2 giving (DG) (pp) | sad | 0.838 | 0.708 | 0.585 | 2.155 | 0.786 | 0.791 | 1.000 | 0.904 |
| qwen25_7b | S2 giving (UG) (pp) | happy | 5.354 | 0.017 | 5.478 | 2.155 | 0.011 | 0.026 | 0.336 | 0.103 |
| qwen25_7b | S2 giving (UG) (pp) | sad | 1.466 | 0.512 | 1.731 | 2.155 | 0.422 | 0.438 | 1.000 | 0.667 |
| qwen25_7b | S3b sent (pp) | happy | 1.599 | 0.639 | 1.300 | 2.473 | 0.599 | 0.609 | 1.000 | 0.749 |
| qwen25_7b | S3b sent (pp) | sad | -2.517 | 0.460 | -2.754 | 2.467 | 0.264 | 0.286 | 1.000 | 0.572 |

## Pre-registered confirmatory tests under this model (one-sided, Holm over F1, F2)

| id | estimate | p_one_sided | p_holm |
|---|---|---|---|
| F1 | -0.13 [-0.51, +0.26] | 0.264 | 0.528 |
| F2 | not estimable (no messages left) |  | 0.528 |
