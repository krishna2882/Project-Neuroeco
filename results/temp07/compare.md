# Temperature robustness: T = 0.7 vs T = 1.0 (exploratory, P20)

Same prompts and seeds; message as a random factor (P12 model) at both temperatures; FDR study-wide within each run. S1 in log-odds of rejection, S2/S3 in percentage points.

- Effects with the same sign at both temperatures: **27 of 30**; correlation of the estimates r = 0.84; median |difference| 0.76.
- Anger → trust (S3b): Llama-3.1-8B -14.3 pp at 1.0 vs -9.2 pp [-20.6, +2.2] at 0.7; Qwen2.5-7B -11.1 pp at 1.0 vs -11.5 pp [-19.4, -3.6] at 0.7

| model | test | emotion | T = 1.0 | T = 0.7 | p_bh_study_t10 | p_bh_study_t07 | same_sign |
|---|---|---|---|---|---|---|---|
| Llama-3.1-8B | S1 rejection (log-OR) | angry | -0.00 [-0.46, +0.46] | -0.10 [-0.59, +0.39] | 0.999 | 0.878 | True |
| Llama-3.1-8B | S1 rejection (log-OR) | happy | -0.43 [-0.89, +0.04] | -0.51 [-1.04, +0.02] | 0.221 | 0.330 | True |
| Llama-3.1-8B | S1 rejection (log-OR) | sad | +0.01 [-0.44, +0.47] | +0.04 [-0.46, +0.53] | 0.999 | 0.951 | True |
| Llama-3.1-8B | S2 giving (DG) (pp) | angry | +7.22 [-4.31, +18.75] | +6.43 [-4.37, +17.23] | 0.429 | 0.409 | True |
| Llama-3.1-8B | S2 giving (DG) (pp) | happy | +4.84 [-6.69, +16.36] | +7.02 [-3.78, +17.81] | 0.631 | 0.409 | True |
| Llama-3.1-8B | S2 giving (DG) (pp) | sad | +6.04 [-5.48, +17.56] | +10.31 [-0.49, +21.10] | 0.493 | 0.330 | True |
| Llama-3.1-8B | S2 giving (UG) (pp) | angry | -2.70 [-14.23, +8.83] | -6.01 [-16.81, +4.79] | 0.760 | 0.434 | True |
| Llama-3.1-8B | S2 giving (UG) (pp) | happy | +4.38 [-7.14, +15.90] | -0.43 [-11.23, +10.36] | 0.674 | 0.971 | False |
| Llama-3.1-8B | S2 giving (UG) (pp) | sad | -1.76 [-13.28, +9.76] | -10.53 [-21.32, +0.27] | 0.849 | 0.330 | True |
| Llama-3.1-8B | S3a returned (pp) | angry | +1.41 [-5.66, +8.47] | -1.07 [-7.22, +5.09] | 0.795 | 0.885 | False |
| Llama-3.1-8B | S3a returned (pp) | happy | +1.94 [-5.12, +9.01] | +4.47 [-1.69, +10.62] | 0.759 | 0.409 | True |
| Llama-3.1-8B | S3a returned (pp) | sad | -5.60 [-12.67, +1.46] | -4.15 [-10.31, +2.00] | 0.302 | 0.409 | True |
| Llama-3.1-8B | S3b sent (pp) | angry | -14.26 [-24.29, -4.23] | -9.19 [-20.63, +2.24] | 0.049 | 0.409 | True |
| Llama-3.1-8B | S3b sent (pp) | happy | +2.94 [-7.09, +12.98] | +7.57 [-3.88, +19.02] | 0.751 | 0.409 | True |
| Llama-3.1-8B | S3b sent (pp) | sad | -14.39 [-24.40, -4.39] | -7.06 [-18.49, +4.36] | 0.049 | 0.409 | True |
| Qwen2.5-7B | S1 rejection (log-OR) | angry | +0.86 [+0.13, +1.59] | +0.82 [+0.07, +1.56] | 0.105 | 0.330 | True |
| Qwen2.5-7B | S1 rejection (log-OR) | happy | -0.47 [-1.20, +0.26] | -0.51 [-1.26, +0.24] | 0.429 | 0.409 | True |
| Qwen2.5-7B | S1 rejection (log-OR) | sad | -0.91 [-1.63, -0.18] | -0.94 [-1.68, -0.21] | 0.085 | 0.321 | True |
| Qwen2.5-7B | S2 giving (DG) (pp) | angry | -5.02 [-10.05, +0.01] | -3.39 [-8.55, +1.77] | 0.172 | 0.409 | True |
| Qwen2.5-7B | S2 giving (DG) (pp) | happy | +3.58 [-1.45, +8.61] | +4.72 [-0.44, +9.89] | 0.376 | 0.334 | True |
| Qwen2.5-7B | S2 giving (DG) (pp) | sad | -2.80 [-7.84, +2.23] | -2.07 [-7.24, +3.09] | 0.466 | 0.630 | True |
| Qwen2.5-7B | S2 giving (UG) (pp) | angry | -5.44 [-10.47, -0.40] | -5.73 [-10.90, -0.57] | 0.138 | 0.330 | True |
| Qwen2.5-7B | S2 giving (UG) (pp) | happy | +1.24 [-3.79, +6.27] | +0.40 [-4.76, +5.56] | 0.760 | 0.951 | True |
| Qwen2.5-7B | S2 giving (UG) (pp) | sad | -3.17 [-8.20, +1.86] | -3.06 [-8.23, +2.10] | 0.429 | 0.409 | True |
| Qwen2.5-7B | S3a returned (pp) | angry | -2.83 [-7.85, +2.19] | -3.20 [-8.31, +1.92] | 0.466 | 0.409 | True |
| Qwen2.5-7B | S3a returned (pp) | happy | +1.83 [-3.19, +6.84] | +1.50 [-3.62, +6.61] | 0.678 | 0.747 | True |
| Qwen2.5-7B | S3a returned (pp) | sad | -1.54 [-6.56, +3.48] | -1.72 [-6.84, +3.39] | 0.751 | 0.705 | True |
| Qwen2.5-7B | S3b sent (pp) | angry | -11.08 [-18.18, -3.97] | -11.50 [-19.45, -3.56] | 0.046 | 0.315 | True |
| Qwen2.5-7B | S3b sent (pp) | happy | -0.07 [-7.17, +7.03] | +0.11 [-7.83, +8.05] | 0.999 | 0.979 | False |
| Qwen2.5-7B | S3b sent (pp) | sad | -1.67 [-8.77, +5.43] | -1.03 [-8.97, +6.91] | 0.760 | 0.925 | True |
