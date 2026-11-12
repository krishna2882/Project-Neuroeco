# All planned emotion effects, corrected across the whole study

51 estimable planned emotion-vs-neutral tests (3 emotions x sub-experiments x models). 7 survive Holm (family-wise, whole study); 19 survive Benjamini-Hochberg FDR 5%.

## Survive Holm across the whole study

| index | model | test | emotion | est | lo | hi | p | p_holm_study |
|---|---|---|---|---|---|---|---|---|
| 12 | qwen25_7b | S3b sent (pp) | angry | -11.225 | -17.389 | -5.061 | 0.000 | 0.017 |
| 16 | qwen25_14b | S1 rejection (log-OR) | sad | -3.026 | -3.970 | -2.083 | 0.000 | 0.000 |
| 27 | qwen25_14b | S3b sent (pp) | angry | -17.183 | -22.413 | -11.953 | 0.000 | 0.000 |
| 28 | qwen25_14b | S3b sent (pp) | sad | 12.314 | 7.095 | 17.533 | 0.000 | 0.000 |
| 31 | qwen25_3b | S1 rejection (log-OR) | sad | -1.454 | -2.265 | -0.643 | 0.000 | 0.020 |
| 42 | qwen25_3b | S3b sent (pp) | angry | -22.510 | -33.157 | -11.863 | 0.000 | 0.002 |
| 48 | qwen25_7b_q8 | S3b sent (pp) | angry | -14.684 | -19.671 | -9.698 | 0.000 | 0.000 |

## Additionally survive FDR (not Holm)

| index | model | test | emotion | est | lo | hi | p | p_bh_study |
|---|---|---|---|---|---|---|---|---|
| 0 | qwen25_7b | S1 rejection (log-OR) | angry | 0.847 | 0.174 | 1.520 | 0.014 | 0.039 |
| 1 | qwen25_7b | S1 rejection (log-OR) | sad | -0.953 | -1.652 | -0.254 | 0.008 | 0.024 |
| 6 | qwen25_7b | S2 giving (UG) (pp) | angry | -5.690 | -10.406 | -0.974 | 0.018 | 0.048 |
| 17 | qwen25_14b | S1 rejection (log-OR) | happy | -1.135 | -1.857 | -0.414 | 0.002 | 0.009 |
| 19 | qwen25_14b | S2 giving (DG) (pp) | sad | 6.213 | 2.232 | 10.193 | 0.002 | 0.009 |
| 22 | qwen25_14b | S2 giving (UG) (pp) | sad | 5.750 | 1.770 | 9.731 | 0.005 | 0.016 |
| 25 | qwen25_14b | S3a returned (pp) | sad | 6.456 | 2.153 | 10.759 | 0.003 | 0.012 |
| 29 | qwen25_14b | S3b sent (pp) | happy | 8.316 | 3.097 | 13.535 | 0.002 | 0.009 |
| 30 | qwen25_3b | S1 rejection (log-OR) | angry | 2.063 | 0.805 | 3.321 | 0.001 | 0.008 |
| 36 | qwen25_3b | S2 giving (UG) (pp) | angry | -20.570 | -33.562 | -7.578 | 0.002 | 0.009 |
| 39 | qwen25_3b | S3a returned (pp) | angry | -19.285 | -31.442 | -7.129 | 0.002 | 0.009 |
| 43 | qwen25_3b | S3b sent (pp) | sad | -14.435 | -25.085 | -3.786 | 0.008 | 0.024 |

## Direction of FDR-significant effects by model (+1 up, -1 down, 0 n.s.)

| test | emotion | qwen25_14b | qwen25_3b | qwen25_7b | qwen25_7b_q8 |
|---|---|---|---|---|---|
| S1 rejection (log-OR) | angry | 0.000 | 1.000 | 1.000 | 0.000 |
| S1 rejection (log-OR) | happy | -1.000 | 0.000 | 0.000 | 0.000 |
| S1 rejection (log-OR) | sad | -1.000 | -1.000 | -1.000 | 0.000 |
| S2 giving (DG) (pp) | angry | 0.000 | 0.000 | 0.000 |  |
| S2 giving (DG) (pp) | happy | 0.000 | 0.000 | 0.000 |  |
| S2 giving (DG) (pp) | sad | 1.000 | 0.000 | 0.000 |  |
| S2 giving (UG) (pp) | angry | 0.000 | -1.000 | -1.000 |  |
| S2 giving (UG) (pp) | happy | 0.000 | 0.000 | 0.000 |  |
| S2 giving (UG) (pp) | sad | 1.000 | 0.000 | 0.000 |  |
| S3a returned (pp) | angry | 0.000 | -1.000 | 0.000 |  |
| S3a returned (pp) | happy | 0.000 | 0.000 | 0.000 |  |
| S3a returned (pp) | sad | 1.000 | 0.000 | 0.000 |  |
| S3b sent (pp) | angry | -1.000 | -1.000 | -1.000 | -1.000 |
| S3b sent (pp) | happy | 1.000 | 0.000 | 0.000 | 0.000 |
| S3b sent (pp) | sad | 1.000 | -1.000 | 0.000 | 0.000 |
