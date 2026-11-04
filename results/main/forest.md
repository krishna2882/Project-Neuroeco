# All planned emotion effects, corrected across the whole study

42 estimable planned emotion-vs-neutral tests (3 emotions x sub-experiments x models). 5 survive Holm (family-wise, whole study); 8 survive Benjamini-Hochberg FDR 5%.

## Survive Holm across the whole study

| index | model | test | emotion | est | lo | hi | p | p_holm_study |
|---|---|---|---|---|---|---|---|---|
| 27 | qwen25_7b | S3b sent (pp) | angry | -11.225 | -17.389 | -5.061 | 0.000 | 0.014 |
| 34 | mistral | S2 giving (DG) (pp) | sad | 24.567 | 17.945 | 31.188 | 0.000 | 0.000 |
| 39 | mistral | S3a returned (pp) | angry | 9.712 | 4.273 | 15.151 | 0.001 | 0.018 |
| 40 | mistral | S3a returned (pp) | sad | 12.009 | 6.571 | 17.448 | 0.000 | 0.001 |
| 41 | mistral | S3a returned (pp) | happy | 13.702 | 8.263 | 19.140 | 0.000 | 0.000 |

## Additionally survive FDR (not Holm)

| index | model | test | emotion | est | lo | hi | p | p_bh_study |
|---|---|---|---|---|---|---|---|---|
| 16 | qwen25_7b | S1 rejection (log-OR) | sad | -0.953 | -1.652 | -0.254 | 0.008 | 0.040 |
| 33 | mistral | S2 giving (DG) (pp) | angry | 9.621 | 3.003 | 16.239 | 0.004 | 0.026 |
| 44 | mistral | S3b sent (pp) | happy | 10.837 | 4.123 | 17.551 | 0.002 | 0.011 |

## Direction of FDR-significant effects by model (+1 up, -1 down, 0 n.s.)

| test | emotion | llama31_8b | mistral | qwen25_7b |
|---|---|---|---|---|
| S1 rejection (log-OR) | angry | 0.000 |  | 0.000 |
| S1 rejection (log-OR) | happy | 0.000 |  | 0.000 |
| S1 rejection (log-OR) | sad | 0.000 |  | -1.000 |
| S2 giving (DG) (pp) | angry | 0.000 | 1.000 | 0.000 |
| S2 giving (DG) (pp) | happy | 0.000 | 0.000 | 0.000 |
| S2 giving (DG) (pp) | sad | 0.000 | 1.000 | 0.000 |
| S2 giving (UG) (pp) | angry | 0.000 | 0.000 | 0.000 |
| S2 giving (UG) (pp) | happy | 0.000 | 0.000 | 0.000 |
| S2 giving (UG) (pp) | sad | 0.000 | 0.000 | 0.000 |
| S3a returned (pp) | angry | 0.000 | 1.000 | 0.000 |
| S3a returned (pp) | happy | 0.000 | 1.000 | 0.000 |
| S3a returned (pp) | sad | 0.000 | 1.000 | 0.000 |
| S3b sent (pp) | angry | 0.000 | 0.000 | -1.000 |
| S3b sent (pp) | happy | 0.000 | 1.000 | 0.000 |
| S3b sent (pp) | sad | 0.000 | 0.000 | 0.000 |
