# Emotion effects with message as a random factor (main)

Model: original fixed effects + C(paraphrase) + (1 | message) + (1 | message:paraphrase). p values: t with df = #message groups - #emotion levels (emotion varies between messages); Holm and BH across the whole study, as in `forest.md`. Script: `analysis/message_re.py` (P12).

- Holm-significant study-wide: **5 → 4**
- FDR-significant study-wide: **8 → 10**

## Effects significant (FDR or Holm) in either analysis

| model | test | emotion | original [95% CI] | with message RE [95% CI] | Holm old | Holm new | FDR old | FDR new |
|---|---|---|---|---|---|---|---|---|
| llama31_8b | S3b sent (pp) | angry | -13.90 [-25.30, -2.49] | -14.26 [-24.29, -4.23] | 0.542 | 0.388 | 0.063 | 0.049 |
| llama31_8b | S3b sent (pp) | sad | -14.47 [-25.87, -3.07] | -14.39 [-24.40, -4.39] | 0.437 | 0.372 | 0.057 | 0.049 |
| mistral | S2 giving (DG) (pp) | angry | +9.62 [+3.00, +16.24] | +9.91 [+4.80, +15.01] | 0.158 | 0.047 | 0.026 | 0.013 |
| mistral | S2 giving (DG) (pp) | happy | +7.80 [+1.18, +14.42] | +7.68 [+2.58, +12.78] | 0.627 | 0.296 | 0.067 | 0.049 |
| mistral | S2 giving (DG) (pp) | sad | +24.57 [+17.94, +31.19] | +25.64 [+20.51, +30.76] | < .001 | < .001 | < .001 | < .001 |
| mistral | S2 giving (UG) (pp) | angry | +7.63 [+1.01, +14.25] | +7.46 [+2.35, +12.56] | 0.691 | 0.348 | 0.071 | 0.049 |
| mistral | S3a returned (pp) | angry | +9.71 [+4.27, +15.15] | +9.71 [+4.21, +15.20] | 0.018 | 0.099 | 0.004 | 0.022 |
| mistral | S3a returned (pp) | happy | +13.70 [+8.26, +19.14] | +13.70 [+8.20, +19.19] | < .001 | 0.004 | < .001 | 0.002 |
| mistral | S3a returned (pp) | sad | +12.01 [+6.57, +17.45] | +12.01 [+6.51, +17.50] | < .001 | 0.016 | < .001 | 0.006 |
| mistral | S3b sent (pp) | happy | +10.84 [+4.12, +17.55] | +10.64 [+2.74, +18.54] | 0.058 | 0.516 | 0.011 | 0.062 |
| qwen25_7b | S1 rejection (log-OR) | sad | -0.95 [-1.65, -0.25] | -0.91 [-1.63, -0.18] | 0.265 | 0.752 | 0.040 | 0.085 |
| qwen25_7b | S3b sent (pp) | angry | -11.22 [-17.39, -5.06] | -11.08 [-18.18, -3.97] | 0.014 | 0.241 | 0.004 | 0.046 |

## Between-message variability (SD of message intercepts; S1 on logit scale, others in pp)

| model | test | sd_msg | sd_msg_para | df |
|---|---|---|---|---|
| llama31_8b | S1 rejection (log-OR) | 0.00 | 0.63 | 19 |
| llama31_8b | S2 giving (DG) (pp) | 4.91 | 8.14 | 19 |
| llama31_8b | S2 giving (UG) (pp) | 4.91 | 8.14 | 19 |
| llama31_8b | S3a returned (pp) | 3.00 | 5.45 | 19 |
| llama31_8b | S3b sent (pp) | 2.82 | 3.19 | 19 |
| mistral | S1 rejection (log-OR) | 0.00 | 0.00 | 19 |
| mistral | S2 giving (DG) (pp) | 2.17 | 2.54 | 19 |
| mistral | S2 giving (UG) (pp) | 2.17 | 2.54 | 19 |
| mistral | S3a returned (pp) | 2.76 | 4.26 | 19 |
| mistral | S3b sent (pp) | 4.57 | 5.56 | 19 |
| qwen25_7b | S1 rejection (log-OR) | 0.43 | 0.68 | 19 |
| qwen25_7b | S2 giving (DG) (pp) | 2.75 | 4.86 | 19 |
| qwen25_7b | S2 giving (UG) (pp) | 2.75 | 4.86 | 19 |
| qwen25_7b | S3a returned (pp) | 2.74 | 4.93 | 19 |
| qwen25_7b | S3b sent (pp) | 4.70 | 3.80 | 19 |

## All tests

| model | test | emotion | est_old | p_old | est_new | se_new | p_z | p_t | p_holm_study | p_bh_study |
|---|---|---|---|---|---|---|---|---|---|---|
| llama31_8b | S1 rejection (log-OR) | angry | -0.068 | 0.849 | -0.000 | 0.233 | 0.999 | 0.999 | 1.000 | 0.999 |
| llama31_8b | S1 rejection (log-OR) | happy | -0.403 | 0.327 | -0.425 | 0.238 | 0.074 | 0.089 | 1.000 | 0.221 |
| llama31_8b | S1 rejection (log-OR) | sad | 0.010 | 0.978 | 0.014 | 0.233 | 0.953 | 0.954 | 1.000 | 0.999 |
| llama31_8b | S2 giving (DG) (pp) | angry | 7.538 | 0.189 | 7.217 | 5.883 | 0.220 | 0.235 | 1.000 | 0.429 |
| llama31_8b | S2 giving (DG) (pp) | happy | 4.125 | 0.472 | 4.835 | 5.878 | 0.411 | 0.421 | 1.000 | 0.631 |
| llama31_8b | S2 giving (DG) (pp) | sad | 5.727 | 0.318 | 6.041 | 5.879 | 0.304 | 0.317 | 1.000 | 0.493 |
| llama31_8b | S2 giving (UG) (pp) | angry | -2.141 | 0.709 | -2.700 | 5.883 | 0.646 | 0.651 | 1.000 | 0.760 |
| llama31_8b | S2 giving (UG) (pp) | happy | 4.904 | 0.392 | 4.377 | 5.878 | 0.456 | 0.466 | 1.000 | 0.674 |
| llama31_8b | S2 giving (UG) (pp) | sad | -0.945 | 0.869 | -1.761 | 5.879 | 0.765 | 0.768 | 1.000 | 0.849 |
| llama31_8b | S3a returned (pp) | angry | 1.313 | 0.760 | 1.407 | 3.605 | 0.696 | 0.701 | 1.000 | 0.795 |
| llama31_8b | S3a returned (pp) | happy | 1.876 | 0.662 | 1.942 | 3.604 | 0.590 | 0.596 | 1.000 | 0.759 |
| llama31_8b | S3a returned (pp) | sad | -5.638 | 0.189 | -5.601 | 3.604 | 0.120 | 0.137 | 1.000 | 0.302 |
| llama31_8b | S3b sent (pp) | angry | -13.897 | 0.017 | -14.263 | 5.118 | 0.005 | 0.012 | 0.388 | 0.049 |
| llama31_8b | S3b sent (pp) | happy | 2.555 | 0.661 | 2.945 | 5.120 | 0.565 | 0.572 | 1.000 | 0.751 |
| llama31_8b | S3b sent (pp) | sad | -14.472 | 0.013 | -14.391 | 5.104 | 0.005 | 0.011 | 0.372 | 0.049 |
| mistral | S1 rejection (log-OR) | angry | 8.332 |  | 8.298 | 55.845 |  |  |  |  |
| mistral | S1 rejection (log-OR) | happy | 8.785 |  | 8.676 | 55.846 |  |  |  |  |
| mistral | S1 rejection (log-OR) | sad | -24.738 |  | -24.734 | 82.742 |  |  |  |  |
| mistral | S2 giving (DG) (pp) | angry | 9.621 | 0.004 | 9.906 | 2.604 | 0.000 | 0.001 | 0.047 | 0.013 |
| mistral | S2 giving (DG) (pp) | happy | 7.800 | 0.021 | 7.681 | 2.604 | 0.003 | 0.008 | 0.296 | 0.049 |
| mistral | S2 giving (DG) (pp) | sad | 24.566 | 0.000 | 25.636 | 2.614 | 0.000 | 0.000 | 0.000 | 0.000 |
| mistral | S2 giving (UG) (pp) | angry | 7.631 | 0.024 | 7.458 | 2.604 | 0.004 | 0.010 | 0.348 | 0.049 |
| mistral | S2 giving (UG) (pp) | happy | 2.866 | 0.396 | 2.942 | 2.604 | 0.259 | 0.273 | 1.000 | 0.466 |
| mistral | S2 giving (UG) (pp) | sad | 6.156 | 0.068 | 5.490 | 2.614 | 0.036 | 0.049 | 1.000 | 0.138 |
| mistral | S3a returned (pp) | angry | 9.712 | 0.000 | 9.708 | 2.804 | 0.001 | 0.003 | 0.099 | 0.022 |
| mistral | S3a returned (pp) | happy | 13.702 | 0.000 | 13.698 | 2.804 | 0.000 | 0.000 | 0.004 | 0.002 |
| mistral | S3a returned (pp) | sad | 12.009 | 0.000 | 12.006 | 2.804 | 0.000 | 0.000 | 0.016 | 0.006 |
| mistral | S3b sent (pp) | angry | 0.136 | 0.968 | 0.272 | 4.029 | 0.946 | 0.947 | 1.000 | 0.999 |
| mistral | S3b sent (pp) | happy | 10.837 | 0.002 | 10.644 | 4.031 | 0.008 | 0.016 | 0.516 | 0.062 |
| mistral | S3b sent (pp) | sad | 6.849 | 0.046 | 6.995 | 4.029 | 0.083 | 0.099 | 1.000 | 0.230 |
| qwen25_7b | S1 rejection (log-OR) | angry | 0.847 | 0.014 | 0.858 | 0.372 | 0.021 | 0.033 | 0.977 | 0.105 |
| qwen25_7b | S1 rejection (log-OR) | happy | -0.458 | 0.204 | -0.470 | 0.374 | 0.209 | 0.224 | 1.000 | 0.429 |
| qwen25_7b | S1 rejection (log-OR) | sad | -0.953 | 0.008 | -0.906 | 0.370 | 0.014 | 0.024 | 0.752 | 0.085 |
| qwen25_7b | S2 giving (DG) (pp) | angry | -4.922 | 0.041 | -5.020 | 2.568 | 0.051 | 0.065 | 1.000 | 0.172 |
| qwen25_7b | S2 giving (DG) (pp) | happy | 3.944 | 0.101 | 3.582 | 2.567 | 0.163 | 0.179 | 1.000 | 0.376 |
| qwen25_7b | S2 giving (DG) (pp) | sad | -2.745 | 0.254 | -2.805 | 2.567 | 0.275 | 0.288 | 1.000 | 0.466 |
| qwen25_7b | S2 giving (UG) (pp) | angry | -5.690 | 0.018 | -5.437 | 2.568 | 0.034 | 0.048 | 1.000 | 0.138 |
| qwen25_7b | S2 giving (UG) (pp) | happy | 0.745 | 0.757 | 1.238 | 2.567 | 0.630 | 0.635 | 1.000 | 0.760 |
| qwen25_7b | S2 giving (UG) (pp) | sad | -3.245 | 0.177 | -3.170 | 2.567 | 0.217 | 0.232 | 1.000 | 0.429 |
| qwen25_7b | S3a returned (pp) | angry | -2.832 | 0.272 | -2.833 | 2.560 | 0.269 | 0.282 | 1.000 | 0.466 |
| qwen25_7b | S3a returned (pp) | happy | 1.826 | 0.478 | 1.826 | 2.560 | 0.476 | 0.484 | 1.000 | 0.678 |
| qwen25_7b | S3a returned (pp) | sad | -1.539 | 0.550 | -1.540 | 2.560 | 0.548 | 0.555 | 1.000 | 0.751 |
| qwen25_7b | S3b sent (pp) | angry | -11.225 | 0.000 | -11.077 | 3.625 | 0.002 | 0.007 | 0.241 | 0.046 |
| qwen25_7b | S3b sent (pp) | happy | -0.046 | 0.988 | -0.067 | 3.621 | 0.985 | 0.985 | 1.000 | 0.999 |
| qwen25_7b | S3b sent (pp) | sad | -1.636 | 0.603 | -1.672 | 3.622 | 0.644 | 0.650 | 1.000 | 0.760 |
