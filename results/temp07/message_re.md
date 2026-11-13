# Emotion effects with message as a random factor (temp07)

Model: original fixed effects + C(paraphrase) + (1 | message) + (1 | message:paraphrase). p values: t with df = #message groups - #emotion levels (emotion varies between messages); Holm and BH across the whole study, as in `forest.md`. Script: `analysis/message_re.py` (P12).

- Holm-significant study-wide: **1 → 0**
- FDR-significant study-wide: **1 → 0**

## Effects significant (FDR or Holm) in either analysis

| model | test | emotion | original [95% CI] | with message RE [95% CI] | Holm old | Holm new | FDR old | FDR new |
|---|---|---|---|---|---|---|---|---|
| qwen25_7b | S3b sent (pp) | angry | -11.73 [-18.02, -5.43] | -11.50 [-19.45, -3.56] | 0.008 | 0.315 | 0.008 | 0.315 |

## Between-message variability (SD of message intercepts; S1 on logit scale, others in pp)

| model | test | sd_msg | sd_msg_para | df |
|---|---|---|---|---|
| llama31_8b | S1 rejection (log-OR) | 0.00 | 0.72 | 19 |
| llama31_8b | S2 giving (DG) (pp) | 4.38 | 9.48 | 19 |
| llama31_8b | S2 giving (UG) (pp) | 4.38 | 9.48 | 19 |
| llama31_8b | S3a returned (pp) | 0.01 | 6.46 | 19 |
| llama31_8b | S3b sent (pp) | 4.76 | 8.98 | 19 |
| qwen25_7b | S1 rejection (log-OR) | 0.44 | 0.68 | 19 |
| qwen25_7b | S2 giving (DG) (pp) | 2.75 | 5.26 | 19 |
| qwen25_7b | S2 giving (UG) (pp) | 2.75 | 5.26 | 19 |
| qwen25_7b | S3a returned (pp) | 2.77 | 5.21 | 19 |
| qwen25_7b | S3b sent (pp) | 5.56 | 3.70 | 19 |

## All tests

| model | test | emotion | est_old | p_old | est_new | se_new | p_z | p_t | p_holm_study | p_bh_study |
|---|---|---|---|---|---|---|---|---|---|---|
| llama31_8b | S1 rejection (log-OR) | angry | 0.167 | 0.711 | -0.097 | 0.250 | 0.698 | 0.702 | 1.000 | 0.878 |
| llama31_8b | S1 rejection (log-OR) | happy | 0.167 | 0.709 | -0.506 | 0.271 | 0.062 | 0.077 | 1.000 | 0.330 |
| llama31_8b | S1 rejection (log-OR) | sad | 0.390 | 0.302 | 0.036 | 0.252 | 0.886 | 0.887 | 1.000 | 0.951 |
| llama31_8b | S2 giving (DG) (pp) | angry | 6.556 | 0.245 | 6.429 | 5.510 | 0.243 | 0.258 | 1.000 | 0.409 |
| llama31_8b | S2 giving (DG) (pp) | happy | 6.829 | 0.226 | 7.016 | 5.508 | 0.203 | 0.218 | 1.000 | 0.409 |
| llama31_8b | S2 giving (DG) (pp) | sad | 9.749 | 0.084 | 10.307 | 5.508 | 0.061 | 0.077 | 1.000 | 0.330 |
| llama31_8b | S2 giving (UG) (pp) | angry | -5.670 | 0.315 | -6.008 | 5.510 | 0.276 | 0.289 | 1.000 | 0.434 |
| llama31_8b | S2 giving (UG) (pp) | happy | -0.453 | 0.936 | -0.432 | 5.508 | 0.937 | 0.938 | 1.000 | 0.971 |
| llama31_8b | S2 giving (UG) (pp) | sad | -9.824 | 0.082 | -10.527 | 5.508 | 0.056 | 0.071 | 1.000 | 0.330 |
| llama31_8b | S3a returned (pp) | angry | -1.208 | 0.794 | -1.067 | 3.141 | 0.734 | 0.738 | 1.000 | 0.885 |
| llama31_8b | S3a returned (pp) | happy | 4.446 | 0.336 | 4.468 | 3.140 | 0.155 | 0.171 | 1.000 | 0.409 |
| llama31_8b | S3a returned (pp) | sad | -4.219 | 0.361 | -4.154 | 3.140 | 0.186 | 0.202 | 1.000 | 0.409 |
| llama31_8b | S3b sent (pp) | angry | -9.201 | 0.112 | -9.193 | 5.835 | 0.115 | 0.132 | 1.000 | 0.409 |
| llama31_8b | S3b sent (pp) | happy | 7.585 | 0.190 | 7.573 | 5.842 | 0.195 | 0.210 | 1.000 | 0.409 |
| llama31_8b | S3b sent (pp) | sad | -7.064 | 0.222 | -7.065 | 5.827 | 0.225 | 0.240 | 1.000 | 0.409 |
| qwen25_7b | S1 rejection (log-OR) | angry | 0.817 | 0.021 | 0.817 | 0.381 | 0.032 | 0.045 | 1.000 | 0.330 |
| qwen25_7b | S1 rejection (log-OR) | happy | -0.499 | 0.176 | -0.512 | 0.383 | 0.180 | 0.196 | 1.000 | 0.409 |
| qwen25_7b | S1 rejection (log-OR) | sad | -0.967 | 0.009 | -0.943 | 0.376 | 0.012 | 0.021 | 0.621 | 0.321 |
| qwen25_7b | S2 giving (DG) (pp) | angry | -3.376 | 0.182 | -3.390 | 2.635 | 0.198 | 0.214 | 1.000 | 0.409 |
| qwen25_7b | S2 giving (DG) (pp) | happy | 4.978 | 0.049 | 4.723 | 2.635 | 0.073 | 0.089 | 1.000 | 0.334 |
| qwen25_7b | S2 giving (DG) (pp) | sad | -1.992 | 0.431 | -2.075 | 2.635 | 0.431 | 0.441 | 1.000 | 0.630 |
| qwen25_7b | S2 giving (UG) (pp) | angry | -5.846 | 0.021 | -5.733 | 2.635 | 0.030 | 0.042 | 1.000 | 0.330 |
| qwen25_7b | S2 giving (UG) (pp) | happy | 0.007 | 0.998 | 0.400 | 2.635 | 0.879 | 0.881 | 1.000 | 0.951 |
| qwen25_7b | S2 giving (UG) (pp) | sad | -3.159 | 0.212 | -3.064 | 2.635 | 0.245 | 0.259 | 1.000 | 0.409 |
| qwen25_7b | S3a returned (pp) | angry | -3.198 | 0.213 | -3.197 | 2.609 | 0.221 | 0.236 | 1.000 | 0.409 |
| qwen25_7b | S3a returned (pp) | happy | 1.497 | 0.560 | 1.497 | 2.609 | 0.566 | 0.573 | 1.000 | 0.747 |
| qwen25_7b | S3a returned (pp) | sad | -1.723 | 0.503 | -1.722 | 2.609 | 0.509 | 0.517 | 1.000 | 0.705 |
| qwen25_7b | S3b sent (pp) | angry | -11.729 | 0.000 | -11.503 | 4.053 | 0.005 | 0.011 | 0.315 | 0.315 |
| qwen25_7b | S3b sent (pp) | happy | 0.167 | 0.958 | 0.110 | 4.051 | 0.978 | 0.979 | 1.000 | 0.979 |
| qwen25_7b | S3b sent (pp) | sad | -0.998 | 0.756 | -1.031 | 4.051 | 0.799 | 0.802 | 1.000 | 0.925 |
