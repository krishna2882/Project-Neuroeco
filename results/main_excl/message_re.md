# Emotion effects with message as a random factor (main_excl)

Model: original fixed effects + C(paraphrase) + (1 | message) + (1 | message:paraphrase). p values: t with df = #message groups - #emotion levels (emotion varies between messages); Holm and BH across the whole study, as in `forest.md`. Script: `analysis/message_re.py` (P12).

- Holm-significant study-wide: **5 → 3**
- FDR-significant study-wide: **7 → 6**

## Effects significant (FDR or Holm) in either analysis

| model | test | emotion | original [95% CI] | with message RE [95% CI] | Holm old | Holm new | FDR old | FDR new |
|---|---|---|---|---|---|---|---|---|
| mistral | S2 giving (DG) (pp) | angry | +12.36 [+5.24, +19.48] | +12.99 [+7.72, +18.26] | 0.025 | 0.005 | 0.006 | 0.003 |
| mistral | S2 giving (DG) (pp) | happy | +7.80 [+1.13, +14.46] | +7.67 [+2.77, +12.57] | 0.721 | 0.244 | 0.092 | 0.046 |
| mistral | S2 giving (DG) (pp) | sad | +24.59 [+17.92, +31.26] | +25.75 [+20.82, +30.68] | < .001 | < .001 | < .001 | < .001 |
| mistral | S3a returned (pp) | angry | +11.52 [+5.79, +17.26] | +11.53 [+4.53, +18.53] | 0.003 | 0.177 | < .001 | 0.039 |
| mistral | S3a returned (pp) | happy | +13.70 [+8.28, +19.12] | +13.66 [+7.05, +20.28] | < .001 | 0.030 | < .001 | 0.011 |
| mistral | S3a returned (pp) | sad | +12.00 [+6.58, +17.43] | +11.98 [+5.36, +18.59] | < .001 | 0.089 | < .001 | 0.024 |
| mistral | S3b sent (pp) | happy | +10.85 [+4.01, +17.69] | +10.66 [+2.68, +18.64] | 0.070 | 0.593 | 0.013 | 0.081 |
| qwen25_7b | S1 rejection (log-OR) | sad | -0.95 [-1.64, -0.26] | -0.91 [-1.64, -0.17] | 0.262 | 0.848 | 0.044 | 0.101 |

## Between-message variability (SD of message intercepts; S1 on logit scale, others in pp)

| model | test | sd_msg | sd_msg_para | df |
|---|---|---|---|---|
| llama31_8b | S1 rejection (log-OR) | 0.00 | 0.63 | 18 |
| llama31_8b | S2 giving (DG) (pp) | 5.66 | 6.85 | 18 |
| llama31_8b | S2 giving (UG) (pp) | 5.66 | 6.85 | 18 |
| llama31_8b | S3a returned (pp) | 2.82 | 5.43 | 18 |
| llama31_8b | S3b sent (pp) | 2.40 | 7.30 | 18 |
| mistral | S1 rejection (log-OR) | 0.35 | 0.00 | 18 |
| mistral | S2 giving (DG) (pp) | 1.81 | 2.40 | 18 |
| mistral | S2 giving (UG) (pp) | 1.81 | 2.40 | 18 |
| mistral | S3a returned (pp) | 4.13 | 3.97 | 18 |
| mistral | S3b sent (pp) | 4.60 | 5.52 | 18 |
| qwen25_7b | S1 rejection (log-OR) | 0.44 | 0.68 | 18 |
| qwen25_7b | S2 giving (DG) (pp) | 1.74 | 3.44 | 18 |
| qwen25_7b | S2 giving (UG) (pp) | 1.74 | 3.44 | 18 |
| qwen25_7b | S3a returned (pp) | 2.43 | 4.77 | 18 |
| qwen25_7b | S3b sent (pp) | 3.50 | 1.41 | 18 |

## All tests

| model | test | emotion | est_old | p_old | est_new | se_new | p_z | p_t | p_holm_study | p_bh_study |
|---|---|---|---|---|---|---|---|---|---|---|
| llama31_8b | S1 rejection (log-OR) | angry | -0.111 | 0.761 | -0.051 | 0.246 | 0.834 | 0.837 | 1.000 | 0.879 |
| llama31_8b | S1 rejection (log-OR) | happy | -0.408 | 0.321 | -0.425 | 0.237 | 0.073 | 0.089 | 1.000 | 0.221 |
| llama31_8b | S1 rejection (log-OR) | sad | 0.009 | 0.979 | 0.013 | 0.232 | 0.955 | 0.956 | 1.000 | 0.979 |
| llama31_8b | S2 giving (DG) (pp) | angry | 4.970 | 0.396 | 4.170 | 6.384 | 0.514 | 0.522 | 1.000 | 0.673 |
| llama31_8b | S2 giving (DG) (pp) | happy | 4.176 | 0.444 | 4.845 | 5.956 | 0.416 | 0.427 | 1.000 | 0.640 |
| llama31_8b | S2 giving (DG) (pp) | sad | 5.845 | 0.284 | 6.015 | 5.957 | 0.313 | 0.326 | 1.000 | 0.527 |
| llama31_8b | S2 giving (UG) (pp) | angry | -1.124 | 0.848 | -1.640 | 6.384 | 0.797 | 0.800 | 1.000 | 0.862 |
| llama31_8b | S2 giving (UG) (pp) | happy | 4.814 | 0.377 | 4.386 | 5.956 | 0.461 | 0.471 | 1.000 | 0.659 |
| llama31_8b | S2 giving (UG) (pp) | sad | -0.956 | 0.861 | -1.788 | 5.957 | 0.764 | 0.768 | 1.000 | 0.848 |
| llama31_8b | S3a returned (pp) | angry | 3.041 | 0.503 | 3.086 | 3.723 | 0.407 | 0.418 | 1.000 | 0.640 |
| llama31_8b | S3a returned (pp) | happy | 1.881 | 0.661 | 1.955 | 3.526 | 0.579 | 0.586 | 1.000 | 0.703 |
| llama31_8b | S3a returned (pp) | sad | -5.631 | 0.190 | -5.590 | 3.525 | 0.113 | 0.130 | 1.000 | 0.273 |
| llama31_8b | S3b sent (pp) | angry | -11.666 | 0.066 | -11.870 | 5.853 | 0.043 | 0.058 | 1.000 | 0.186 |
| llama31_8b | S3b sent (pp) | happy | 2.553 | 0.666 | 2.767 | 5.445 | 0.611 | 0.618 | 1.000 | 0.720 |
| llama31_8b | S3b sent (pp) | sad | -14.473 | 0.014 | -14.428 | 5.428 | 0.008 | 0.016 | 0.577 | 0.081 |
| mistral | S1 rejection (log-OR) | angry | 8.392 |  | 8.431 | 56.748 |  |  |  |  |
| mistral | S1 rejection (log-OR) | happy | 8.803 |  | 8.815 | 56.745 |  |  |  |  |
| mistral | S1 rejection (log-OR) | sad | -24.603 |  | -24.649 | 83.437 |  |  |  |  |
| mistral | S2 giving (DG) (pp) | angry | 12.358 | 0.001 | 12.991 | 2.689 | 0.000 | 0.000 | 0.005 | 0.003 |
| mistral | S2 giving (DG) (pp) | happy | 7.798 | 0.022 | 7.669 | 2.498 | 0.002 | 0.007 | 0.244 | 0.046 |
| mistral | S2 giving (DG) (pp) | sad | 24.587 | 0.000 | 25.752 | 2.514 | 0.000 | 0.000 | 0.000 | 0.000 |
| mistral | S2 giving (UG) (pp) | angry | 7.463 | 0.040 | 7.140 | 2.689 | 0.008 | 0.016 | 0.577 | 0.081 |
| mistral | S2 giving (UG) (pp) | happy | 2.866 | 0.399 | 2.929 | 2.498 | 0.241 | 0.256 | 1.000 | 0.449 |
| mistral | S2 giving (UG) (pp) | sad | 6.157 | 0.070 | 5.606 | 2.514 | 0.026 | 0.039 | 1.000 | 0.136 |
| mistral | S3a returned (pp) | angry | 11.524 | 0.000 | 11.529 | 3.570 | 0.001 | 0.005 | 0.177 | 0.039 |
| mistral | S3a returned (pp) | happy | 13.699 | 0.000 | 13.665 | 3.374 | 0.000 | 0.001 | 0.030 | 0.011 |
| mistral | S3a returned (pp) | sad | 12.004 | 0.000 | 11.976 | 3.374 | 0.000 | 0.002 | 0.089 | 0.024 |
| mistral | S3b sent (pp) | angry | 1.492 | 0.689 | 1.613 | 4.344 | 0.710 | 0.715 | 1.000 | 0.811 |
| mistral | S3b sent (pp) | happy | 10.848 | 0.002 | 10.661 | 4.073 | 0.009 | 0.017 | 0.593 | 0.081 |
| mistral | S3b sent (pp) | sad | 6.841 | 0.050 | 6.982 | 4.071 | 0.086 | 0.104 | 1.000 | 0.229 |
| qwen25_7b | S1 rejection (log-OR) | angry | 0.763 | 0.032 | 0.781 | 0.400 | 0.051 | 0.067 | 1.000 | 0.200 |
| qwen25_7b | S1 rejection (log-OR) | happy | -0.459 | 0.200 | -0.469 | 0.382 | 0.219 | 0.234 | 1.000 | 0.428 |
| qwen25_7b | S1 rejection (log-OR) | sad | -0.949 | 0.007 | -0.906 | 0.375 | 0.016 | 0.027 | 0.848 | 0.101 |
| qwen25_7b | S2 giving (DG) (pp) | angry | -2.544 | 0.223 | -2.849 | 1.972 | 0.149 | 0.166 | 1.000 | 0.317 |
| qwen25_7b | S2 giving (DG) (pp) | happy | 3.882 | 0.048 | 3.532 | 1.849 | 0.056 | 0.072 | 1.000 | 0.202 |
| qwen25_7b | S2 giving (DG) (pp) | sad | -2.753 | 0.160 | -2.811 | 1.849 | 0.128 | 0.146 | 1.000 | 0.292 |
| qwen25_7b | S2 giving (UG) (pp) | angry | -2.402 | 0.250 | -2.085 | 1.972 | 0.290 | 0.304 | 1.000 | 0.511 |
| qwen25_7b | S2 giving (UG) (pp) | happy | 0.744 | 0.704 | 1.188 | 1.849 | 0.521 | 0.529 | 1.000 | 0.673 |
| qwen25_7b | S2 giving (UG) (pp) | sad | -3.244 | 0.098 | -3.175 | 1.849 | 0.086 | 0.103 | 1.000 | 0.229 |
| qwen25_7b | S3a returned (pp) | angry | -4.562 | 0.076 | -4.562 | 2.506 | 0.069 | 0.085 | 1.000 | 0.221 |
| qwen25_7b | S3a returned (pp) | happy | 1.826 | 0.451 | 1.826 | 2.367 | 0.440 | 0.450 | 1.000 | 0.652 |
| qwen25_7b | S3a returned (pp) | sad | -1.539 | 0.526 | -1.540 | 2.367 | 0.515 | 0.523 | 1.000 | 0.673 |
| qwen25_7b | S3b sent (pp) | angry | -7.498 | 0.018 | -7.569 | 3.019 | 0.012 | 0.022 | 0.725 | 0.092 |
| qwen25_7b | S3b sent (pp) | happy | -0.039 | 0.990 | -0.024 | 2.818 | 0.993 | 0.993 | 1.000 | 0.993 |
| qwen25_7b | S3b sent (pp) | sad | -1.625 | 0.584 | -1.600 | 2.819 | 0.570 | 0.577 | 1.000 | 0.703 |
