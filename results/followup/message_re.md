# Emotion effects with message as a random factor (followup)

Model: original fixed effects + C(paraphrase) + (1 | message) + (1 | message:paraphrase). p values: t with df = #message groups - #emotion levels (emotion varies between messages); Holm and BH across the whole study, as in `forest.md`. Script: `analysis/message_re.py` (P12).

- Holm-significant study-wide: **2 → 1**
- FDR-significant study-wide: **3 → 4**

## Effects significant (FDR or Holm) in either analysis

| model | test | emotion | original [95% CI] | with message RE [95% CI] | Holm old | Holm new | FDR old | FDR new |
|---|---|---|---|---|---|---|---|---|
| llama31_8b | S1 rejection (log-OR) | happy | +0.72 [+0.15, +1.30] | +0.71 [+0.43, +1.00] | 0.280 | 0.004 | 0.067 | 0.004 |
| llama31_8b | S3b sent (pp) | happy | +20.88 [+10.68, +31.09] | +20.51 [+8.03, +33.00] | 0.001 | 0.118 | 0.001 | 0.043 |
| qwen25_7b | S2 giving (DG) (pp) | happy | +6.46 [+2.37, +10.55] | +6.41 [+2.34, +10.49] | 0.045 | 0.149 | 0.022 | 0.043 |
| qwen25_7b | S3b sent (pp) | angry | -9.60 [-15.89, -3.31] | -9.57 [-14.98, -4.15] | 0.061 | 0.074 | 0.022 | 0.038 |

## Between-message variability (SD of message intercepts; S1 on logit scale, others in pp)

| model | test | sd_msg | sd_msg_para | df |
|---|---|---|---|---|
| llama31_8b | S1 rejection (log-OR) | 0.12 | 0.12 | 16 |
| llama31_8b | S2 giving (DG) (pp) | 1.57 | 3.02 | 16 |
| llama31_8b | S2 giving (UG) (pp) | 1.57 | 3.02 | 16 |
| llama31_8b | S3b sent (pp) | 6.71 | 7.40 | 16 |
| qwen25_7b | S1 rejection (log-OR) | 0.15 | 0.39 | 16 |
| qwen25_7b | S2 giving (DG) (pp) | 1.74 | 4.75 | 16 |
| qwen25_7b | S2 giving (UG) (pp) | 1.74 | 4.75 | 16 |
| qwen25_7b | S3b sent (pp) | 2.20 | 5.44 | 16 |

## All tests

| model | test | emotion | est_old | p_old | est_new | se_new | p_z | p_t | p_holm_study | p_bh_study |
|---|---|---|---|---|---|---|---|---|---|---|
| llama31_8b | S1 rejection (log-OR) | angry | 0.321 | 0.267 | 0.316 | 0.144 | 0.028 | 0.044 | 0.786 | 0.150 |
| llama31_8b | S1 rejection (log-OR) | happy | 0.723 | 0.014 | 0.714 | 0.147 | 0.000 | 0.000 | 0.004 | 0.004 |
| llama31_8b | S1 rejection (log-OR) | sad | 0.199 | 0.494 | 0.189 | 0.144 | 0.190 | 0.209 | 1.000 | 0.501 |
| llama31_8b | S2 giving (DG) (pp) | angry | -5.437 | 0.355 | -5.018 | 4.922 | 0.308 | 0.323 | 1.000 | 0.554 |
| llama31_8b | S2 giving (DG) (pp) | happy | 4.134 | 0.482 | 3.935 | 4.931 | 0.425 | 0.437 | 1.000 | 0.616 |
| llama31_8b | S2 giving (DG) (pp) | sad | 11.297 | 0.055 | 11.376 | 4.921 | 0.021 | 0.034 | 0.654 | 0.138 |
| llama31_8b | S2 giving (UG) (pp) | angry | -5.191 | 0.377 | -5.383 | 4.922 | 0.274 | 0.290 | 1.000 | 0.554 |
| llama31_8b | S2 giving (UG) (pp) | happy | 6.936 | 0.238 | 6.539 | 4.931 | 0.185 | 0.203 | 1.000 | 0.501 |
| llama31_8b | S2 giving (UG) (pp) | sad | 5.326 | 0.365 | 5.178 | 4.921 | 0.293 | 0.308 | 1.000 | 0.554 |
| llama31_8b | S3b sent (pp) | angry | -9.288 | 0.074 | -9.371 | 6.364 | 0.141 | 0.160 | 1.000 | 0.481 |
| llama31_8b | S3b sent (pp) | happy | 20.884 | 0.000 | 20.513 | 6.371 | 0.001 | 0.005 | 0.118 | 0.043 |
| llama31_8b | S3b sent (pp) | sad | -0.521 | 0.920 | -0.314 | 6.366 | 0.961 | 0.961 | 1.000 | 0.988 |
| qwen25_7b | S1 rejection (log-OR) | angry | 0.240 | 0.256 | 0.241 | 0.194 | 0.213 | 0.231 | 1.000 | 0.503 |
| qwen25_7b | S1 rejection (log-OR) | happy | 0.030 | 0.886 | 0.031 | 0.193 | 0.870 | 0.873 | 1.000 | 0.952 |
| qwen25_7b | S1 rejection (log-OR) | sad | -0.130 | 0.540 | -0.126 | 0.194 | 0.516 | 0.525 | 1.000 | 0.700 |
| qwen25_7b | S2 giving (DG) (pp) | angry | 0.301 | 0.885 | 0.032 | 2.079 | 0.988 | 0.988 | 1.000 | 0.988 |
| qwen25_7b | S2 giving (DG) (pp) | happy | 6.463 | 0.002 | 6.413 | 2.079 | 0.002 | 0.007 | 0.149 | 0.043 |
| qwen25_7b | S2 giving (DG) (pp) | sad | 0.829 | 0.691 | 0.584 | 2.079 | 0.779 | 0.782 | 1.000 | 0.894 |
| qwen25_7b | S2 giving (UG) (pp) | angry | 0.463 | 0.824 | 0.761 | 2.079 | 0.714 | 0.719 | 1.000 | 0.863 |
| qwen25_7b | S2 giving (UG) (pp) | happy | 5.347 | 0.010 | 5.475 | 2.079 | 0.008 | 0.018 | 0.361 | 0.087 |
| qwen25_7b | S2 giving (UG) (pp) | sad | 1.472 | 0.481 | 1.730 | 2.079 | 0.405 | 0.418 | 1.000 | 0.616 |
| qwen25_7b | S3b sent (pp) | angry | -9.602 | 0.003 | -9.569 | 2.763 | 0.001 | 0.003 | 0.074 | 0.038 |
| qwen25_7b | S3b sent (pp) | happy | 1.572 | 0.624 | 1.447 | 2.768 | 0.601 | 0.608 | 1.000 | 0.768 |
| qwen25_7b | S3b sent (pp) | sad | -2.538 | 0.429 | -2.637 | 2.766 | 0.340 | 0.355 | 1.000 | 0.567 |

## Pre-registered confirmatory tests under this model (one-sided, Holm over F1, F2)

| id | estimate | p_one_sided | p_holm |
|---|---|---|---|
| F1 | -0.13 [-0.51, +0.25] | 0.263 | 0.263 |
| F2 | -9.57 [-14.98, -4.15] | 0.002 | 0.003 |
