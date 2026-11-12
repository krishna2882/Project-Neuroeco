# Emotion effects with message as a random factor (ext2)

Model: original fixed effects + C(paraphrase) + (1 | message) + (1 | message:paraphrase). p values: t with df = #message groups - #emotion levels (emotion varies between messages); Holm and BH across the whole study, as in `forest.md`. Script: `analysis/message_re.py` (P12).

- Holm-significant study-wide: **7 → 4**
- FDR-significant study-wide: **19 → 13**

## Effects significant (FDR or Holm) in either analysis

| model | test | emotion | original [95% CI] | with message RE [95% CI] | Holm old | Holm new | FDR old | FDR new |
|---|---|---|---|---|---|---|---|---|
| qwen25_14b | S1 rejection (log-OR) | happy | -1.14 [-1.86, -0.41] | -1.11 [-1.53, -0.69] | 0.081 | 0.003 | 0.009 | 0.001 |
| qwen25_14b | S1 rejection (log-OR) | sad | -3.03 [-3.97, -2.08] | -3.38 [-4.02, -2.74] | < .001 | < .001 | < .001 | < .001 |
| qwen25_14b | S2 giving (DG) (pp) | sad | +6.21 [+2.23, +10.19] | +6.17 [+2.52, +9.83] | 0.087 | 0.161 | 0.009 | 0.023 |
| qwen25_14b | S2 giving (UG) (pp) | sad | +5.75 [+1.77, +9.73] | +5.77 [+2.11, +9.42] | 0.171 | 0.257 | 0.016 | 0.032 |
| qwen25_14b | S3a returned (pp) | sad | +6.46 [+2.15, +10.76] | +6.46 [+2.14, +10.78] | 0.124 | 0.345 | 0.012 | 0.037 |
| qwen25_14b | S3b sent (pp) | angry | -17.18 [-22.41, -11.95] | -16.47 [-25.90, -7.04] | < .001 | 0.131 | < .001 | 0.023 |
| qwen25_14b | S3b sent (pp) | happy | +8.32 [+3.10, +13.53] | +8.27 [-1.16, +17.70] | 0.077 | 1.000 | 0.009 | 0.192 |
| qwen25_14b | S3b sent (pp) | sad | +12.31 [+7.10, +17.53] | +12.28 [+2.85, +21.70] | < .001 | 0.740 | < .001 | 0.068 |
| qwen25_3b | S1 rejection (log-OR) | angry | +2.06 [+0.80, +3.32] | +1.79 [+0.63, +2.94] | 0.058 | 0.280 | 0.008 | 0.032 |
| qwen25_3b | S1 rejection (log-OR) | sad | -1.45 [-2.26, -0.64] | -1.54 [-2.21, -0.88] | 0.020 | 0.011 | 0.003 | 0.004 |
| qwen25_3b | S2 giving (UG) (pp) | angry | -20.57 [-33.56, -7.58] | -20.21 [-34.12, -6.30] | 0.079 | 0.401 | 0.009 | 0.040 |
| qwen25_3b | S3a returned (pp) | angry | -19.29 [-31.44, -7.13] | -19.26 [-30.43, -8.10] | 0.079 | 0.141 | 0.009 | 0.023 |
| qwen25_3b | S3b sent (pp) | angry | -22.51 [-33.16, -11.86] | -22.50 [-33.69, -11.31] | 0.002 | 0.042 | < .001 | 0.011 |
| qwen25_3b | S3b sent (pp) | sad | -14.44 [-25.08, -3.79] | -14.50 [-25.70, -3.31] | 0.276 | 0.740 | 0.024 | 0.068 |
| qwen25_7b | S1 rejection (log-OR) | angry | +0.85 [+0.17, +1.52] | +0.86 [+0.13, +1.59] | 0.464 | 1.000 | 0.039 | 0.092 |
| qwen25_7b | S1 rejection (log-OR) | sad | -0.95 [-1.65, -0.25] | -0.91 [-1.63, -0.18] | 0.272 | 0.873 | 0.024 | 0.077 |
| qwen25_7b | S2 giving (UG) (pp) | angry | -5.69 [-10.41, -0.97] | -5.44 [-10.47, -0.40] | 0.595 | 1.000 | 0.048 | 0.121 |
| qwen25_7b | S3b sent (pp) | angry | -11.22 [-17.39, -5.06] | -11.08 [-18.18, -3.97] | 0.016 | 0.273 | 0.003 | 0.032 |
| qwen25_7b_q8 | S3b sent (pp) | angry | -14.68 [-19.67, -9.70] | -14.27 [-21.65, -6.90] | < .001 | 0.058 | < .001 | 0.013 |

## Between-message variability (SD of message intercepts; S1 on logit scale, others in pp)

| model | test | sd_msg | sd_msg_para | df |
|---|---|---|---|---|
| qwen25_14b | S1 rejection (log-OR) | 0.00 | 1.37 | 19 |
| qwen25_14b | S2 giving (DG) (pp) | 1.23 | 3.88 | 19 |
| qwen25_14b | S2 giving (UG) (pp) | 1.23 | 3.88 | 19 |
| qwen25_14b | S3a returned (pp) | 2.21 | 5.14 | 19 |
| qwen25_14b | S3b sent (pp) | 7.16 | 3.21 | 19 |
| qwen25_3b | S1 rejection (log-OR) | 0.00 | 1.31 | 19 |
| qwen25_3b | S2 giving (DG) (pp) | 7.29 | 13.99 | 19 |
| qwen25_3b | S2 giving (UG) (pp) | 7.29 | 13.99 | 19 |
| qwen25_3b | S3a returned (pp) | 6.93 | 9.48 | 19 |
| qwen25_3b | S3b sent (pp) | 6.07 | 7.85 | 19 |
| qwen25_7b | S1 rejection (log-OR) | 0.43 | 0.68 | 19 |
| qwen25_7b | S2 giving (DG) (pp) | 2.75 | 4.86 | 19 |
| qwen25_7b | S2 giving (UG) (pp) | 2.75 | 4.86 | 19 |
| qwen25_7b | S3a returned (pp) | 2.74 | 4.93 | 19 |
| qwen25_7b | S3b sent (pp) | 4.70 | 3.80 | 19 |
| qwen25_7b_q8 | S1 rejection (log-OR) | 0.41 | 0.61 | 19 |
| qwen25_7b_q8 | S3b sent (pp) | 5.23 | 3.04 | 19 |

## All tests

| model | test | emotion | est_old | p_old | est_new | se_new | p_z | p_t | p_holm_study | p_bh_study |
|---|---|---|---|---|---|---|---|---|---|---|
| qwen25_14b | S1 rejection (log-OR) | angry | 0.710 | 0.088 | 0.150 | 0.211 | 0.476 | 0.484 | 1.000 | 0.588 |
| qwen25_14b | S1 rejection (log-OR) | happy | -1.135 | 0.002 | -1.112 | 0.216 | 0.000 | 0.000 | 0.003 | 0.001 |
| qwen25_14b | S1 rejection (log-OR) | sad | -3.026 | 0.000 | -3.382 | 0.327 | 0.000 | 0.000 | 0.000 | 0.000 |
| qwen25_14b | S2 giving (DG) (pp) | angry | -3.585 | 0.078 | -3.785 | 1.865 | 0.042 | 0.057 | 1.000 | 0.131 |
| qwen25_14b | S2 giving (DG) (pp) | happy | 1.642 | 0.419 | 1.418 | 1.864 | 0.447 | 0.456 | 1.000 | 0.588 |
| qwen25_14b | S2 giving (DG) (pp) | sad | 6.213 | 0.002 | 6.175 | 1.864 | 0.001 | 0.004 | 0.161 | 0.023 |
| qwen25_14b | S2 giving (UG) (pp) | angry | -0.994 | 0.625 | -0.864 | 1.865 | 0.643 | 0.649 | 1.000 | 0.663 |
| qwen25_14b | S2 giving (UG) (pp) | happy | 1.428 | 0.482 | 1.647 | 1.864 | 0.377 | 0.388 | 1.000 | 0.535 |
| qwen25_14b | S2 giving (UG) (pp) | sad | 5.750 | 0.005 | 5.768 | 1.864 | 0.002 | 0.006 | 0.257 | 0.032 |
| qwen25_14b | S3a returned (pp) | angry | -4.720 | 0.032 | -4.721 | 2.204 | 0.032 | 0.045 | 1.000 | 0.121 |
| qwen25_14b | S3a returned (pp) | happy | 2.633 | 0.230 | 2.633 | 2.204 | 0.232 | 0.247 | 1.000 | 0.370 |
| qwen25_14b | S3a returned (pp) | sad | 6.456 | 0.003 | 6.456 | 2.204 | 0.003 | 0.009 | 0.345 | 0.037 |
| qwen25_14b | S3b sent (pp) | angry | -17.183 | 0.000 | -16.467 | 4.812 | 0.001 | 0.003 | 0.131 | 0.023 |
| qwen25_14b | S3b sent (pp) | happy | 8.316 | 0.002 | 8.271 | 4.810 | 0.086 | 0.102 | 1.000 | 0.192 |
| qwen25_14b | S3b sent (pp) | sad | 12.314 | 0.000 | 12.276 | 4.810 | 0.011 | 0.019 | 0.740 | 0.068 |
| qwen25_3b | S1 rejection (log-OR) | angry | 2.063 | 0.001 | 1.785 | 0.589 | 0.002 | 0.007 | 0.280 | 0.032 |
| qwen25_3b | S1 rejection (log-OR) | happy | -0.571 | 0.206 | -0.675 | 0.332 | 0.042 | 0.056 | 1.000 | 0.131 |
| qwen25_3b | S1 rejection (log-OR) | sad | -1.454 | 0.000 | -1.544 | 0.341 | 0.000 | 0.000 | 0.011 | 0.004 |
| qwen25_3b | S2 giving (DG) (pp) | angry | -13.416 | 0.043 | -13.964 | 7.097 | 0.049 | 0.064 | 1.000 | 0.133 |
| qwen25_3b | S2 giving (DG) (pp) | happy | 4.332 | 0.513 | 4.682 | 7.097 | 0.509 | 0.517 | 1.000 | 0.609 |
| qwen25_3b | S2 giving (DG) (pp) | sad | 4.877 | 0.462 | 4.291 | 7.097 | 0.545 | 0.553 | 1.000 | 0.609 |
| qwen25_3b | S2 giving (UG) (pp) | angry | -20.570 | 0.002 | -20.214 | 7.097 | 0.004 | 0.010 | 0.401 | 0.040 |
| qwen25_3b | S2 giving (UG) (pp) | happy | 5.103 | 0.441 | 5.099 | 7.097 | 0.473 | 0.481 | 1.000 | 0.588 |
| qwen25_3b | S2 giving (UG) (pp) | sad | -4.944 | 0.456 | -4.198 | 7.097 | 0.554 | 0.561 | 1.000 | 0.609 |
| qwen25_3b | S3a returned (pp) | angry | -19.286 | 0.002 | -19.264 | 5.695 | 0.001 | 0.003 | 0.141 | 0.023 |
| qwen25_3b | S3a returned (pp) | happy | 3.692 | 0.552 | 3.681 | 5.695 | 0.518 | 0.526 | 1.000 | 0.609 |
| qwen25_3b | S3a returned (pp) | sad | -13.588 | 0.028 | -13.584 | 5.695 | 0.017 | 0.028 | 0.967 | 0.083 |
| qwen25_3b | S3b sent (pp) | angry | -22.510 | 0.000 | -22.499 | 5.707 | 0.000 | 0.001 | 0.042 | 0.011 |
| qwen25_3b | S3b sent (pp) | happy | -7.754 | 0.154 | -7.807 | 5.710 | 0.172 | 0.187 | 1.000 | 0.319 |
| qwen25_3b | S3b sent (pp) | sad | -14.435 | 0.008 | -14.503 | 5.711 | 0.011 | 0.020 | 0.740 | 0.068 |
| qwen25_7b | S1 rejection (log-OR) | angry | 0.847 | 0.014 | 0.858 | 0.372 | 0.021 | 0.033 | 1.000 | 0.092 |
| qwen25_7b | S1 rejection (log-OR) | happy | -0.458 | 0.204 | -0.470 | 0.374 | 0.209 | 0.224 | 1.000 | 0.358 |
| qwen25_7b | S1 rejection (log-OR) | sad | -0.953 | 0.008 | -0.906 | 0.370 | 0.014 | 0.024 | 0.873 | 0.077 |
| qwen25_7b | S2 giving (DG) (pp) | angry | -4.922 | 0.041 | -5.020 | 2.568 | 0.051 | 0.065 | 1.000 | 0.133 |
| qwen25_7b | S2 giving (DG) (pp) | happy | 3.944 | 0.101 | 3.582 | 2.567 | 0.163 | 0.179 | 1.000 | 0.315 |
| qwen25_7b | S2 giving (DG) (pp) | sad | -2.745 | 0.254 | -2.805 | 2.567 | 0.275 | 0.288 | 1.000 | 0.408 |
| qwen25_7b | S2 giving (UG) (pp) | angry | -5.690 | 0.018 | -5.437 | 2.568 | 0.034 | 0.048 | 1.000 | 0.121 |
| qwen25_7b | S2 giving (UG) (pp) | happy | 0.745 | 0.757 | 1.238 | 2.567 | 0.630 | 0.635 | 1.000 | 0.663 |
| qwen25_7b | S2 giving (UG) (pp) | sad | -3.245 | 0.177 | -3.170 | 2.567 | 0.217 | 0.232 | 1.000 | 0.359 |
| qwen25_7b | S3a returned (pp) | angry | -2.832 | 0.272 | -2.833 | 2.560 | 0.269 | 0.282 | 1.000 | 0.408 |
| qwen25_7b | S3a returned (pp) | happy | 1.826 | 0.478 | 1.826 | 2.560 | 0.476 | 0.484 | 1.000 | 0.588 |
| qwen25_7b | S3a returned (pp) | sad | -1.539 | 0.550 | -1.540 | 2.560 | 0.548 | 0.555 | 1.000 | 0.609 |
| qwen25_7b | S3b sent (pp) | angry | -11.225 | 0.000 | -11.077 | 3.625 | 0.002 | 0.007 | 0.273 | 0.032 |
| qwen25_7b | S3b sent (pp) | happy | -0.046 | 0.988 | -0.067 | 3.621 | 0.985 | 0.985 | 1.000 | 0.985 |
| qwen25_7b | S3b sent (pp) | sad | -1.636 | 0.603 | -1.672 | 3.622 | 0.644 | 0.650 | 1.000 | 0.663 |
| qwen25_7b_q8 | S1 rejection (log-OR) | angry | 0.672 | 0.036 | 0.676 | 0.345 | 0.050 | 0.065 | 1.000 | 0.133 |
| qwen25_7b_q8 | S1 rejection (log-OR) | happy | -0.551 | 0.090 | -0.547 | 0.346 | 0.114 | 0.131 | 1.000 | 0.238 |
| qwen25_7b_q8 | S1 rejection (log-OR) | sad | -0.681 | 0.036 | -0.642 | 0.347 | 0.065 | 0.080 | 1.000 | 0.157 |
| qwen25_7b_q8 | S3b sent (pp) | angry | -14.684 | 0.000 | -14.273 | 3.764 | 0.000 | 0.001 | 0.058 | 0.013 |
| qwen25_7b_q8 | S3b sent (pp) | happy | -2.917 | 0.251 | -3.081 | 3.762 | 0.413 | 0.423 | 1.000 | 0.568 |
| qwen25_7b_q8 | S3b sent (pp) | sad | -4.459 | 0.079 | -4.730 | 3.763 | 0.209 | 0.224 | 1.000 | 0.358 |
