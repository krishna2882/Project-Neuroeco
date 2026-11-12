# Equivalence tests and pooled estimates (P14; Llama, Qwen, Mistral)

Built on the stricter model with message as a random factor (`message_re.md`). Smallest effect of interest (SESOI), chosen **after** seeing the results, so two are shown: primary ±5 pp / OR 1.5, lenient ±10 pp / OR 2. Classes: *equivalent to zero* (90% CI inside ±SESOI, not significant), *small but real* (significant, inside ±SESOI), *real* (significant, not equivalent), *inconclusive*. Significant = study-wide FDR (BH) < .05. Script: `analysis/equivalence.py`.

## How many emotion effects fall in each class (primary SESOI: ±5 pp / OR 1.5)

| study | model | equivalent to zero | small but real | real | inconclusive |
|---|---|---|---|---|---|
| followup | llama31_8b | 0 | 0 | 2 | 10 |
| followup | qwen25_7b | 4 | 0 | 2 | 6 |
| main | llama31_8b | 1 | 0 | 2 | 12 |
| main | mistral | 0 | 0 | 7 | 5 |
| main | qwen25_7b | 0 | 0 | 1 | 14 |

## Same with the lenient SESOI (±10 pp / OR 2)

| study | model | equivalent to zero | small but real | real | inconclusive |
|---|---|---|---|---|---|
| followup | llama31_8b | 2 | 0 | 2 | 8 |
| followup | qwen25_7b | 10 | 0 | 2 | 0 |
| main | llama31_8b | 4 | 0 | 2 | 9 |
| main | mistral | 2 | 0 | 7 | 3 |
| main | qwen25_7b | 11 | 0 | 1 | 3 |

## Pooled main + follow-up (10 messages per emotion; secondary, not pre-registered)

Fixed-effect inverse-variance pooling; `p_het` tests whether the two studies disagree (life-event vs event-free messages); a small `p_het` means pooling hides a real difference. Holm over the pooled tests.

| model | test | emotion | main | follow-up | pooled [95% CI] | p_t | p_holm | p_bh_study | p_het | class_primary |
|---|---|---|---|---|---|---|---|---|---|---|
| llama31_8b | S1 rejection (log-OR) | angry | -0.000 | 0.320 | +0.23 [-0.01, +0.47] | 0.071 | 1.000 | 0.171 | 0.248 | inconclusive |
| llama31_8b | S1 rejection (log-OR) | happy | -0.430 | 0.710 | +0.40 [+0.15, +0.64] | 0.003 | 0.067 | 0.023 | 0.000 | real |
| llama31_8b | S1 rejection (log-OR) | sad | 0.010 | 0.190 | +0.14 [-0.10, +0.38] | 0.260 | 1.000 | 0.397 | 0.522 | equivalent to zero |
| llama31_8b | S2 giving (DG) (pp) | angry | 7.220 | -5.020 | +0.0 [-7.4, +7.4] | 0.996 | 1.000 | 0.996 | 0.111 | inconclusive |
| llama31_8b | S2 giving (DG) (pp) | happy | 4.840 | 3.940 | +4.3 [-3.1, +11.7] | 0.262 | 1.000 | 0.397 | 0.907 | inconclusive |
| llama31_8b | S2 giving (DG) (pp) | sad | 6.040 | 11.380 | +9.2 [+1.8, +16.6] | 0.020 | 0.385 | 0.081 | 0.487 | inconclusive |
| llama31_8b | S2 giving (UG) (pp) | angry | -2.700 | -5.380 | -4.3 [-11.7, +3.1] | 0.265 | 1.000 | 0.397 | 0.727 | inconclusive |
| llama31_8b | S2 giving (UG) (pp) | happy | 4.380 | 6.540 | +5.6 [-1.8, +13.1] | 0.144 | 1.000 | 0.288 | 0.778 | inconclusive |
| llama31_8b | S2 giving (UG) (pp) | sad | -1.760 | 5.180 | +2.3 [-5.1, +9.7] | 0.543 | 1.000 | 0.686 | 0.365 | inconclusive |
| llama31_8b | S3b sent (pp) | angry | -14.260 | -9.370 | -12.3 [-20.2, -4.5] | 0.004 | 0.081 | 0.023 | 0.549 | real |
| llama31_8b | S3b sent (pp) | happy | 2.940 | 20.510 | +9.8 [+2.0, +17.7] | 0.019 | 0.375 | 0.081 | 0.032 | inconclusive |
| llama31_8b | S3b sent (pp) | sad | -14.390 | -0.310 | -8.9 [-16.7, -1.1] | 0.032 | 0.548 | 0.097 | 0.085 | inconclusive |
| qwen25_7b | S1 rejection (log-OR) | angry | 0.860 | 0.240 | +0.37 [+0.04, +0.71] | 0.037 | 0.590 | 0.098 | 0.142 | inconclusive |
| qwen25_7b | S1 rejection (log-OR) | happy | -0.470 | 0.030 | -0.07 [-0.41, +0.26] | 0.670 | 1.000 | 0.751 | 0.234 | equivalent to zero |
| qwen25_7b | S1 rejection (log-OR) | sad | -0.910 | -0.130 | -0.29 [-0.63, +0.04] | 0.096 | 1.000 | 0.209 | 0.062 | inconclusive |
| qwen25_7b | S2 giving (DG) (pp) | angry | -5.020 | 0.030 | -2.0 [-5.1, +1.2] | 0.231 | 1.000 | 0.397 | 0.126 | equivalent to zero |
| qwen25_7b | S2 giving (DG) (pp) | happy | 3.580 | 6.410 | +5.3 [+2.1, +8.5] | 0.002 | 0.055 | 0.023 | 0.392 | real |
| qwen25_7b | S2 giving (DG) (pp) | sad | -2.800 | 0.580 | -0.8 [-3.9, +2.4] | 0.642 | 1.000 | 0.751 | 0.305 | equivalent to zero |
| qwen25_7b | S2 giving (UG) (pp) | angry | -5.440 | 0.760 | -1.7 [-4.9, +1.5] | 0.302 | 1.000 | 0.409 | 0.061 | equivalent to zero |
| qwen25_7b | S2 giving (UG) (pp) | happy | 1.240 | 5.480 | +3.8 [+0.6, +7.0] | 0.025 | 0.442 | 0.084 | 0.200 | inconclusive |
| qwen25_7b | S2 giving (UG) (pp) | sad | -3.170 | 1.730 | -0.2 [-3.4, +3.0] | 0.897 | 1.000 | 0.936 | 0.138 | equivalent to zero |
| qwen25_7b | S3b sent (pp) | angry | -11.080 | -9.570 | -10.1 [-14.4, -5.8] | 0.000 | 0.001 | 0.001 | 0.741 | real |
| qwen25_7b | S3b sent (pp) | happy | -0.070 | 1.450 | +0.9 [-3.4, +5.2] | 0.689 | 1.000 | 0.751 | 0.740 | equivalent to zero |
| qwen25_7b | S3b sent (pp) | sad | -1.670 | -2.640 | -2.3 [-6.6, +2.0] | 0.306 | 1.000 | 0.409 | 0.832 | inconclusive |

## Every test

| study | model | test | emotion | estimate [90% CI] | p_t | p_tost_primary | class_primary | class_lenient |
|---|---|---|---|---|---|---|---|---|
| main | llama31_8b | S1 rejection (log-OR) | angry | -0.00 [-0.40, +0.40] | 0.999 | 0.049 | equivalent to zero | equivalent to zero |
| main | llama31_8b | S1 rejection (log-OR) | happy | -0.43 [-0.84, -0.01] | 0.089 | 0.533 | inconclusive | inconclusive |
| main | llama31_8b | S1 rejection (log-OR) | sad | +0.01 [-0.39, +0.42] | 0.954 | 0.055 | inconclusive | equivalent to zero |
| main | llama31_8b | S2 giving (DG) (pp) | angry | +7.2 [-3.0, +17.4] | 0.235 | 0.645 | inconclusive | inconclusive |
| main | llama31_8b | S2 giving (DG) (pp) | happy | +4.8 [-5.3, +15.0] | 0.421 | 0.489 | inconclusive | inconclusive |
| main | llama31_8b | S2 giving (DG) (pp) | sad | +6.0 [-4.1, +16.2] | 0.317 | 0.569 | inconclusive | inconclusive |
| main | llama31_8b | S2 giving (UG) (pp) | angry | -2.7 [-12.9, +7.5] | 0.651 | 0.350 | inconclusive | inconclusive |
| main | llama31_8b | S2 giving (UG) (pp) | happy | +4.4 [-5.8, +14.5] | 0.466 | 0.458 | inconclusive | inconclusive |
| main | llama31_8b | S2 giving (UG) (pp) | sad | -1.8 [-11.9, +8.4] | 0.768 | 0.294 | inconclusive | inconclusive |
| main | llama31_8b | S3a returned (pp) | angry | +1.4 [-4.8, +7.6] | 0.701 | 0.166 | inconclusive | equivalent to zero |
| main | llama31_8b | S3a returned (pp) | happy | +1.9 [-4.3, +8.2] | 0.596 | 0.203 | inconclusive | equivalent to zero |
| main | llama31_8b | S3a returned (pp) | sad | -5.6 [-11.8, +0.6] | 0.137 | 0.565 | inconclusive | inconclusive |
| main | llama31_8b | S3b sent (pp) | angry | -14.3 [-23.1, -5.4] | 0.012 | 0.957 | real | real |
| main | llama31_8b | S3b sent (pp) | happy | +2.9 [-5.9, +11.8] | 0.572 | 0.346 | inconclusive | inconclusive |
| main | llama31_8b | S3b sent (pp) | sad | -14.4 [-23.2, -5.6] | 0.011 | 0.959 | real | real |
| main | mistral | S2 giving (DG) (pp) | angry | +9.9 [+5.4, +14.4] | 0.001 | 0.962 | real | real |
| main | mistral | S2 giving (DG) (pp) | happy | +7.7 [+3.2, +12.2] | 0.008 | 0.842 | real | real |
| main | mistral | S2 giving (DG) (pp) | sad | +25.6 [+21.1, +30.2] | 0.000 | 1.000 | real | real |
| main | mistral | S2 giving (UG) (pp) | angry | +7.5 [+3.0, +12.0] | 0.010 | 0.821 | real | real |
| main | mistral | S2 giving (UG) (pp) | happy | +2.9 [-1.6, +7.4] | 0.273 | 0.219 | inconclusive | equivalent to zero |
| main | mistral | S2 giving (UG) (pp) | sad | +5.5 [+1.0, +10.0] | 0.049 | 0.573 | inconclusive | inconclusive |
| main | mistral | S3a returned (pp) | angry | +9.7 [+4.9, +14.6] | 0.003 | 0.945 | real | real |
| main | mistral | S3a returned (pp) | happy | +13.7 [+8.8, +18.5] | 0.000 | 0.997 | real | real |
| main | mistral | S3a returned (pp) | sad | +12.0 [+7.2, +16.9] | 0.000 | 0.989 | real | real |
| main | mistral | S3b sent (pp) | angry | +0.3 [-6.7, +7.2] | 0.947 | 0.128 | inconclusive | equivalent to zero |
| main | mistral | S3b sent (pp) | happy | +10.6 [+3.7, +17.6] | 0.016 | 0.911 | inconclusive | inconclusive |
| main | mistral | S3b sent (pp) | sad | +7.0 [+0.0, +14.0] | 0.099 | 0.687 | inconclusive | inconclusive |
| main | qwen25_7b | S1 rejection (log-OR) | angry | +0.86 [+0.21, +1.50] | 0.033 | 0.881 | inconclusive | inconclusive |
| main | qwen25_7b | S1 rejection (log-OR) | happy | -0.47 [-1.12, +0.18] | 0.224 | 0.568 | inconclusive | inconclusive |
| main | qwen25_7b | S1 rejection (log-OR) | sad | -0.91 [-1.55, -0.27] | 0.024 | 0.904 | inconclusive | inconclusive |
| main | qwen25_7b | S2 giving (DG) (pp) | angry | -5.0 [-9.5, -0.6] | 0.065 | 0.503 | inconclusive | equivalent to zero |
| main | qwen25_7b | S2 giving (DG) (pp) | happy | +3.6 [-0.9, +8.0] | 0.179 | 0.294 | inconclusive | equivalent to zero |
| main | qwen25_7b | S2 giving (DG) (pp) | sad | -2.8 [-7.2, +1.6] | 0.288 | 0.202 | inconclusive | equivalent to zero |
| main | qwen25_7b | S2 giving (UG) (pp) | angry | -5.4 [-9.9, -1.0] | 0.048 | 0.567 | inconclusive | equivalent to zero |
| main | qwen25_7b | S2 giving (UG) (pp) | happy | +1.2 [-3.2, +5.7] | 0.635 | 0.080 | inconclusive | equivalent to zero |
| main | qwen25_7b | S2 giving (UG) (pp) | sad | -3.2 [-7.6, +1.3] | 0.232 | 0.242 | inconclusive | equivalent to zero |
| main | qwen25_7b | S3a returned (pp) | angry | -2.8 [-7.3, +1.6] | 0.282 | 0.204 | inconclusive | equivalent to zero |
| main | qwen25_7b | S3a returned (pp) | happy | +1.8 [-2.6, +6.3] | 0.484 | 0.115 | inconclusive | equivalent to zero |
| main | qwen25_7b | S3a returned (pp) | sad | -1.5 [-6.0, +2.9] | 0.555 | 0.096 | inconclusive | equivalent to zero |
| main | qwen25_7b | S3b sent (pp) | angry | -11.1 [-17.3, -4.8] | 0.007 | 0.945 | real | real |
| main | qwen25_7b | S3b sent (pp) | happy | -0.1 [-6.3, +6.2] | 0.985 | 0.095 | inconclusive | equivalent to zero |
| main | qwen25_7b | S3b sent (pp) | sad | -1.7 [-7.9, +4.6] | 0.650 | 0.185 | inconclusive | equivalent to zero |
| followup | llama31_8b | S1 rejection (log-OR) | angry | +0.32 [+0.06, +0.57] | 0.044 | 0.273 | inconclusive | equivalent to zero |
| followup | llama31_8b | S1 rejection (log-OR) | happy | +0.71 [+0.46, +0.97] | 0.000 | 0.974 | real | real |
| followup | llama31_8b | S1 rejection (log-OR) | sad | +0.19 [-0.06, +0.44] | 0.209 | 0.077 | inconclusive | equivalent to zero |
| followup | llama31_8b | S2 giving (DG) (pp) | angry | -5.0 [-13.6, +3.6] | 0.323 | 0.501 | inconclusive | inconclusive |
| followup | llama31_8b | S2 giving (DG) (pp) | happy | +3.9 [-4.7, +12.5] | 0.437 | 0.416 | inconclusive | inconclusive |
| followup | llama31_8b | S2 giving (DG) (pp) | sad | +11.4 [+2.8, +20.0] | 0.034 | 0.893 | inconclusive | inconclusive |
| followup | llama31_8b | S2 giving (UG) (pp) | angry | -5.4 [-14.0, +3.2] | 0.290 | 0.531 | inconclusive | inconclusive |
| followup | llama31_8b | S2 giving (UG) (pp) | happy | +6.5 [-2.1, +15.1] | 0.203 | 0.621 | inconclusive | inconclusive |
| followup | llama31_8b | S2 giving (UG) (pp) | sad | +5.2 [-3.4, +13.8] | 0.308 | 0.514 | inconclusive | inconclusive |
| followup | llama31_8b | S3b sent (pp) | angry | -9.4 [-20.5, +1.7] | 0.160 | 0.749 | inconclusive | inconclusive |
| followup | llama31_8b | S3b sent (pp) | happy | +20.5 [+9.4, +31.6] | 0.005 | 0.987 | real | real |
| followup | llama31_8b | S3b sent (pp) | sad | -0.3 [-11.4, +10.8] | 0.961 | 0.236 | inconclusive | inconclusive |
| followup | qwen25_7b | S1 rejection (log-OR) | angry | +0.24 [-0.10, +0.58] | 0.231 | 0.204 | inconclusive | equivalent to zero |
| followup | qwen25_7b | S1 rejection (log-OR) | happy | +0.03 [-0.31, +0.37] | 0.873 | 0.035 | equivalent to zero | equivalent to zero |
| followup | qwen25_7b | S1 rejection (log-OR) | sad | -0.13 [-0.47, +0.21] | 0.525 | 0.085 | inconclusive | equivalent to zero |
| followup | qwen25_7b | S2 giving (DG) (pp) | angry | +0.0 [-3.6, +3.7] | 0.988 | 0.015 | equivalent to zero | equivalent to zero |
| followup | qwen25_7b | S2 giving (DG) (pp) | happy | +6.4 [+2.8, +10.0] | 0.007 | 0.747 | real | real |
| followup | qwen25_7b | S2 giving (DG) (pp) | sad | +0.6 [-3.0, +4.2] | 0.782 | 0.025 | equivalent to zero | equivalent to zero |
| followup | qwen25_7b | S2 giving (UG) (pp) | angry | +0.8 [-2.9, +4.4] | 0.719 | 0.029 | equivalent to zero | equivalent to zero |
| followup | qwen25_7b | S2 giving (UG) (pp) | happy | +5.5 [+1.8, +9.1] | 0.018 | 0.589 | inconclusive | equivalent to zero |
| followup | qwen25_7b | S2 giving (UG) (pp) | sad | +1.7 [-1.9, +5.4] | 0.418 | 0.068 | inconclusive | equivalent to zero |
| followup | qwen25_7b | S3b sent (pp) | angry | -9.6 [-14.4, -4.7] | 0.003 | 0.941 | real | real |
| followup | qwen25_7b | S3b sent (pp) | happy | +1.4 [-3.4, +6.3] | 0.608 | 0.109 | inconclusive | equivalent to zero |
| followup | qwen25_7b | S3b sent (pp) | sad | -2.6 [-7.5, +2.2] | 0.355 | 0.203 | inconclusive | equivalent to zero |
