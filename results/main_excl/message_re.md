# Emotion effects with message as a random factor (main_excl)

Model: original fixed effects + C(paraphrase) + (1 | message) + (1 | message:paraphrase). p values: t with df = #message groups - #emotion levels (emotion varies between messages); Holm and BH across the whole study, as in `forest.md`. Script: `analysis/message_re.py` (P12).

- Holm-significant study-wide: **5 → 5**
- FDR-significant study-wide: **7 → 5**

## Effects significant (FDR or Holm) in either analysis

| model | test | emotion | original [95% CI] | with message RE [95% CI] | Holm old | Holm new | FDR old | FDR new |
|---|---|---|---|---|---|---|---|---|
| mistral | S2 giving (DG) (pp) | angry | +13.63 [+5.64, +21.62] | +14.64 [+8.62, +20.65] | 0.031 | 0.007 | 0.007 | 0.002 |
| mistral | S2 giving (DG) (pp) | sad | +24.56 [+17.78, +31.35] | +25.72 [+20.70, +30.74] | < .001 | < .001 | < .001 | < .001 |
| mistral | S3a returned (pp) | angry | +12.91 [+6.62, +19.20] | +12.91 [+7.20, +18.61] | 0.002 | 0.014 | < .001 | 0.003 |
| mistral | S3a returned (pp) | happy | +13.71 [+8.25, +19.18] | +13.73 [+8.77, +18.69] | < .001 | 0.002 | < .001 | < .001 |
| mistral | S3a returned (pp) | sad | +12.03 [+6.57, +17.50] | +12.05 [+7.09, +17.01] | < .001 | 0.007 | < .001 | 0.002 |
| mistral | S3b sent (pp) | happy | +10.83 [+3.89, +17.76] | +10.63 [+2.45, +18.82] | 0.082 | 0.710 | 0.016 | 0.097 |
| qwen25_7b | S1 rejection (log-OR) | sad | -0.91 [-1.54, -0.28] | -0.88 [-1.54, -0.22] | 0.159 | 0.626 | 0.027 | 0.094 |

## Between-message variability (SD of message intercepts; S1 on logit scale, others in pp)

| model | test | sd_msg | sd_msg_para | df |
|---|---|---|---|---|
| llama31_8b | S1 rejection (log-OR) | 0.00 | 0.62 | 17 |
| llama31_8b | S2 giving (DG) (pp) | 6.02 | 7.02 | 17 |
| llama31_8b | S2 giving (UG) (pp) | 6.02 | 7.02 | 17 |
| llama31_8b | S3a returned (pp) | 3.30 | 4.43 | 17 |
| llama31_8b | S3b sent (pp) | 3.50 | 3.75 | 17 |
| mistral | S1 rejection (log-OR) | 0.00 | 0.00 | 17 |
| mistral | S2 giving (DG) (pp) | 1.90 | 2.51 | 17 |
| mistral | S2 giving (UG) (pp) | 1.90 | 2.51 | 17 |
| mistral | S3a returned (pp) | 2.90 | 0.00 | 17 |
| mistral | S3b sent (pp) | 4.76 | 5.73 | 17 |
| qwen25_7b | S1 rejection (log-OR) | 0.36 | 0.65 | 17 |
| qwen25_7b | S2 giving (DG) (pp) | 0.97 | 3.32 | 17 |
| qwen25_7b | S2 giving (UG) (pp) | 0.97 | 3.32 | 17 |
| qwen25_7b | S3a returned (pp) | 2.51 | 4.47 | 17 |
| qwen25_7b | S3b sent (pp) | 2.87 | 3.22 | 17 |

## All tests

| model | test | emotion | est_old | p_old | est_new | se_new | p_z | p_t | p_holm_study | p_bh_study |
|---|---|---|---|---|---|---|---|---|---|---|
| llama31_8b | S1 rejection (log-OR) | angry | -0.179 | 0.662 | -0.130 | 0.268 | 0.626 | 0.632 | 1.000 | 0.759 |
| llama31_8b | S1 rejection (log-OR) | happy | -0.400 | 0.332 | -0.428 | 0.234 | 0.067 | 0.085 | 1.000 | 0.222 |
| llama31_8b | S1 rejection (log-OR) | sad | 0.010 | 0.977 | 0.013 | 0.230 | 0.954 | 0.955 | 1.000 | 0.978 |
| llama31_8b | S2 giving (DG) (pp) | angry | 5.677 | 0.391 | 4.687 | 7.223 | 0.516 | 0.525 | 1.000 | 0.735 |
| llama31_8b | S2 giving (DG) (pp) | happy | 4.134 | 0.455 | 4.859 | 6.072 | 0.424 | 0.435 | 1.000 | 0.722 |
| llama31_8b | S2 giving (DG) (pp) | sad | 5.748 | 0.299 | 5.976 | 6.074 | 0.325 | 0.339 | 1.000 | 0.593 |
| llama31_8b | S2 giving (UG) (pp) | angry | -3.205 | 0.628 | -3.823 | 7.223 | 0.597 | 0.603 | 1.000 | 0.747 |
| llama31_8b | S2 giving (UG) (pp) | happy | 4.889 | 0.377 | 4.400 | 6.072 | 0.469 | 0.479 | 1.000 | 0.722 |
| llama31_8b | S2 giving (UG) (pp) | sad | -0.947 | 0.864 | -1.826 | 6.074 | 0.764 | 0.767 | 1.000 | 0.839 |
| llama31_8b | S3a returned (pp) | angry | 1.680 | 0.729 | 1.715 | 4.074 | 0.674 | 0.679 | 1.000 | 0.792 |
| llama31_8b | S3a returned (pp) | happy | 1.838 | 0.663 | 1.904 | 3.544 | 0.591 | 0.598 | 1.000 | 0.747 |
| llama31_8b | S3a returned (pp) | sad | -5.675 | 0.178 | -5.638 | 3.543 | 0.112 | 0.130 | 1.000 | 0.287 |
| llama31_8b | S3b sent (pp) | angry | -13.542 | 0.049 | -13.804 | 6.217 | 0.026 | 0.040 | 1.000 | 0.145 |
| llama31_8b | S3b sent (pp) | happy | 2.550 | 0.668 | 2.841 | 5.381 | 0.598 | 0.604 | 1.000 | 0.747 |
| llama31_8b | S3b sent (pp) | sad | -14.474 | 0.015 | -14.413 | 5.364 | 0.007 | 0.016 | 0.561 | 0.094 |
| mistral | S1 rejection (log-OR) | angry | 8.748 |  | 8.733 | 54.426 |  |  |  |  |
| mistral | S1 rejection (log-OR) | happy | 8.737 |  | 8.723 | 54.424 |  |  |  |  |
| mistral | S1 rejection (log-OR) | sad | -24.564 |  | -24.668 | 81.940 |  |  |  |  |
| mistral | S2 giving (DG) (pp) | angry | 13.627 | 0.001 | 14.637 | 3.069 | 0.000 | 0.000 | 0.007 | 0.002 |
| mistral | S2 giving (DG) (pp) | happy | 7.800 | 0.024 | 7.672 | 2.546 | 0.003 | 0.008 | 0.290 | 0.055 |
| mistral | S2 giving (DG) (pp) | sad | 24.563 | 0.000 | 25.723 | 2.562 | 0.000 | 0.000 | 0.000 | 0.000 |
| mistral | S2 giving (UG) (pp) | angry | 7.166 | 0.079 | 6.563 | 3.069 | 0.032 | 0.047 | 1.000 | 0.145 |
| mistral | S2 giving (UG) (pp) | happy | 2.866 | 0.407 | 2.932 | 2.546 | 0.249 | 0.265 | 1.000 | 0.507 |
| mistral | S2 giving (UG) (pp) | sad | 6.156 | 0.075 | 5.577 | 2.562 | 0.029 | 0.044 | 1.000 | 0.145 |
| mistral | S3a returned (pp) | angry | 12.909 | 0.000 | 12.905 | 2.909 | 0.000 | 0.000 | 0.014 | 0.003 |
| mistral | S3a returned (pp) | happy | 13.712 | 0.000 | 13.733 | 2.530 | 0.000 | 0.000 | 0.002 | 0.001 |
| mistral | S3a returned (pp) | sad | 12.032 | 0.000 | 12.049 | 2.530 | 0.000 | 0.000 | 0.007 | 0.002 |
| mistral | S3b sent (pp) | angry | 1.525 | 0.710 | 1.744 | 4.839 | 0.719 | 0.723 | 1.000 | 0.821 |
| mistral | S3b sent (pp) | happy | 10.825 | 0.002 | 10.632 | 4.176 | 0.011 | 0.021 | 0.710 | 0.097 |
| mistral | S3b sent (pp) | sad | 6.858 | 0.053 | 7.003 | 4.174 | 0.093 | 0.112 | 1.000 | 0.261 |
| qwen25_7b | S1 rejection (log-OR) | angry | 0.421 | 0.237 | 0.419 | 0.382 | 0.272 | 0.288 | 1.000 | 0.525 |
| qwen25_7b | S1 rejection (log-OR) | happy | -0.457 | 0.154 | -0.459 | 0.332 | 0.167 | 0.185 | 1.000 | 0.388 |
| qwen25_7b | S1 rejection (log-OR) | sad | -0.912 | 0.004 | -0.881 | 0.336 | 0.009 | 0.018 | 0.626 | 0.094 |
| qwen25_7b | S2 giving (DG) (pp) | angry | 0.067 | 0.976 | -0.219 | 1.868 | 0.907 | 0.908 | 1.000 | 0.953 |
| qwen25_7b | S2 giving (DG) (pp) | happy | 3.870 | 0.042 | 3.481 | 1.578 | 0.027 | 0.041 | 1.000 | 0.145 |
| qwen25_7b | S2 giving (DG) (pp) | sad | -2.755 | 0.148 | -2.817 | 1.577 | 0.074 | 0.092 | 1.000 | 0.227 |
| qwen25_7b | S2 giving (UG) (pp) | angry | -0.813 | 0.716 | -0.532 | 1.868 | 0.776 | 0.779 | 1.000 | 0.839 |
| qwen25_7b | S2 giving (UG) (pp) | happy | 0.744 | 0.696 | 1.137 | 1.578 | 0.471 | 0.481 | 1.000 | 0.722 |
| qwen25_7b | S2 giving (UG) (pp) | sad | -3.244 | 0.089 | -3.181 | 1.577 | 0.044 | 0.060 | 1.000 | 0.167 |
| qwen25_7b | S3a returned (pp) | angry | -3.421 | 0.227 | -3.424 | 2.708 | 0.206 | 0.223 | 1.000 | 0.446 |
| qwen25_7b | S3a returned (pp) | happy | 1.823 | 0.458 | 1.823 | 2.349 | 0.438 | 0.448 | 1.000 | 0.722 |
| qwen25_7b | S3a returned (pp) | sad | -1.539 | 0.531 | -1.541 | 2.349 | 0.512 | 0.521 | 1.000 | 0.735 |
| qwen25_7b | S3b sent (pp) | angry | -6.368 | 0.069 | -6.644 | 3.124 | 0.033 | 0.048 | 1.000 | 0.145 |
| qwen25_7b | S3b sent (pp) | happy | -0.040 | 0.989 | -0.015 | 2.664 | 0.995 | 0.996 | 1.000 | 0.996 |
| qwen25_7b | S3b sent (pp) | sad | -1.627 | 0.590 | -1.585 | 2.665 | 0.552 | 0.560 | 1.000 | 0.747 |
