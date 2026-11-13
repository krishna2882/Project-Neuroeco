# Emotion effects with message as a random factor (followup_excl)

Model: original fixed effects + C(paraphrase) + (1 | message) + (1 | message:paraphrase). p values: t with df = #message groups - #emotion levels (emotion varies between messages); Holm and BH across the whole study, as in `forest.md`. Script: `analysis/message_re.py` (P12).

- Holm-significant study-wide: **1 → 1**
- FDR-significant study-wide: **2 → 1**

## Effects significant (FDR or Holm) in either analysis

| model | test | emotion | original [95% CI] | with message RE [95% CI] | Holm old | Holm new | FDR old | FDR new |
|---|---|---|---|---|---|---|---|---|
| llama31_8b | S1 rejection (log-OR) | happy | +0.73 [+0.12, +1.33] | +0.72 [+0.45, +1.00] | 0.368 | 0.005 | 0.088 | 0.005 |
| llama31_8b | S3b sent (pp) | happy | +20.84 [+9.79, +31.89] | +20.46 [+6.72, +34.19] | 0.005 | 0.275 | 0.005 | 0.115 |
| qwen25_7b | S2 giving (DG) (pp) | happy | +6.47 [+2.06, +10.87] | +6.42 [+1.96, +10.87] | 0.092 | 0.317 | 0.048 | 0.115 |

## Between-message variability (SD of message intercepts; S1 on logit scale, others in pp)

| model | test | sd_msg | sd_msg_para | df |
|---|---|---|---|---|
| llama31_8b | S1 rejection (log-OR) | 0.08 | 0.17 | 13 |
| llama31_8b | S2 giving (DG) (pp) | 3.34 | 4.64 | 13 |
| llama31_8b | S2 giving (UG) (pp) | 3.34 | 4.64 | 13 |
| llama31_8b | S3b sent (pp) | 7.63 | 8.10 | 13 |
| qwen25_7b | S1 rejection (log-OR) | 0.12 | 0.40 | 13 |
| qwen25_7b | S2 giving (DG) (pp) | 2.04 | 5.05 | 13 |
| qwen25_7b | S2 giving (UG) (pp) | 2.04 | 5.05 | 13 |
| qwen25_7b | S3b sent (pp) | 3.06 | 5.84 | 13 |

## All tests

| model | test | emotion | est_old | p_old | est_new | se_new | p_z | p_t | p_holm_study | p_bh_study |
|---|---|---|---|---|---|---|---|---|---|---|
| llama31_8b | S1 rejection (log-OR) | angry | 0.410 | 0.295 | 0.395 | 0.186 | 0.033 | 0.053 | 1.000 | 0.190 |
| llama31_8b | S1 rejection (log-OR) | happy | 0.726 | 0.018 | 0.724 | 0.142 | 0.000 | 0.000 | 0.005 | 0.005 |
| llama31_8b | S1 rejection (log-OR) | sad | 0.200 | 0.508 | 0.192 | 0.139 | 0.168 | 0.191 | 1.000 | 0.573 |
| llama31_8b | S2 giving (DG) (pp) | angry | -7.851 | 0.343 | -7.648 | 7.643 | 0.317 | 0.335 | 1.000 | 0.728 |
| llama31_8b | S2 giving (DG) (pp) | happy | 4.122 | 0.485 | 4.247 | 5.440 | 0.435 | 0.449 | 1.000 | 0.728 |
| llama31_8b | S2 giving (DG) (pp) | sad | 11.298 | 0.056 | 11.412 | 5.425 | 0.035 | 0.055 | 1.000 | 0.190 |
| llama31_8b | S2 giving (UG) (pp) | angry | -3.257 | 0.694 | -3.377 | 7.643 | 0.659 | 0.666 | 1.000 | 0.841 |
| llama31_8b | S2 giving (UG) (pp) | happy | 6.918 | 0.242 | 6.851 | 5.440 | 0.208 | 0.230 | 1.000 | 0.613 |
| llama31_8b | S2 giving (UG) (pp) | sad | 5.320 | 0.368 | 5.214 | 5.425 | 0.337 | 0.354 | 1.000 | 0.728 |
| llama31_8b | S3b sent (pp) | angry | -6.776 | 0.389 | -6.820 | 9.660 | 0.480 | 0.493 | 1.000 | 0.728 |
| llama31_8b | S3b sent (pp) | happy | 20.839 | 0.000 | 20.456 | 7.008 | 0.004 | 0.012 | 0.275 | 0.115 |
| llama31_8b | S3b sent (pp) | sad | -0.496 | 0.930 | -0.282 | 7.003 | 0.968 | 0.968 | 1.000 | 0.968 |
| qwen25_7b | S1 rejection (log-OR) | angry | 0.203 | 0.463 | 0.206 | 0.249 | 0.407 | 0.422 | 1.000 | 0.728 |
| qwen25_7b | S1 rejection (log-OR) | happy | 0.030 | 0.885 | 0.031 | 0.187 | 0.867 | 0.870 | 1.000 | 0.908 |
| qwen25_7b | S1 rejection (log-OR) | sad | -0.130 | 0.536 | -0.126 | 0.189 | 0.504 | 0.516 | 1.000 | 0.728 |
| qwen25_7b | S2 giving (DG) (pp) | angry | 1.034 | 0.734 | 0.666 | 3.070 | 0.828 | 0.832 | 1.000 | 0.908 |
| qwen25_7b | S2 giving (DG) (pp) | happy | 6.468 | 0.004 | 6.417 | 2.274 | 0.005 | 0.014 | 0.317 | 0.115 |
| qwen25_7b | S2 giving (DG) (pp) | sad | 0.832 | 0.711 | 0.585 | 2.274 | 0.797 | 0.801 | 1.000 | 0.908 |
| qwen25_7b | S2 giving (UG) (pp) | angry | -0.184 | 0.952 | 0.562 | 3.070 | 0.855 | 0.858 | 1.000 | 0.908 |
| qwen25_7b | S2 giving (UG) (pp) | happy | 5.350 | 0.017 | 5.480 | 2.274 | 0.016 | 0.032 | 0.631 | 0.151 |
| qwen25_7b | S2 giving (UG) (pp) | sad | 1.470 | 0.513 | 1.731 | 2.274 | 0.447 | 0.460 | 1.000 | 0.728 |
| qwen25_7b | S3b sent (pp) | angry | -11.653 | 0.014 | -11.443 | 4.348 | 0.008 | 0.021 | 0.435 | 0.124 |
| qwen25_7b | S3b sent (pp) | happy | 1.618 | 0.640 | 1.552 | 3.160 | 0.623 | 0.632 | 1.000 | 0.841 |
| qwen25_7b | S3b sent (pp) | sad | -2.501 | 0.470 | -2.554 | 3.159 | 0.419 | 0.433 | 1.000 | 0.728 |

## Pre-registered confirmatory tests under this model (one-sided, Holm over F1, F2)

| id | estimate | p_one_sided | p_holm |
|---|---|---|---|
| F1 | -0.13 [-0.50, +0.24] | 0.258 | 0.258 |
| F2 | -11.44 [-19.97, -2.92] | 0.010 | 0.021 |
