# All planned emotion effects, corrected across the whole study

16 estimable planned emotion-vs-neutral tests (3 emotions x sub-experiments x models). 1 survive Holm (family-wise, whole study); 2 survive Benjamini-Hochberg FDR 5%.

## Survive Holm across the whole study

| index | model | test | emotion | est | lo | hi | p | p_holm_study |
|---|---|---|---|---|---|---|---|---|
| 7 | llama31_8b | S3b sent (pp) | happy | 20.831 | 9.351 | 32.311 | 0.000 | 0.006 |

## Additionally survive FDR (not Holm)

| index | model | test | emotion | est | lo | hi | p | p_bh_study |
|---|---|---|---|---|---|---|---|---|
| 11 | qwen25_7b | S2 giving (DG) (pp) | happy | 6.476 | 2.094 | 10.857 | 0.004 | 0.030 |

## Direction of FDR-significant effects by model (+1 up, -1 down, 0 n.s.)

| test | emotion | llama31_8b | qwen25_7b |
|---|---|---|---|
| S1 rejection (log-OR) | happy | 0.000 | 0.000 |
| S1 rejection (log-OR) | sad | 0.000 | 0.000 |
| S2 giving (DG) (pp) | happy | 0.000 | 1.000 |
| S2 giving (DG) (pp) | sad | 0.000 | 0.000 |
| S2 giving (UG) (pp) | happy | 0.000 | 0.000 |
| S2 giving (UG) (pp) | sad | 0.000 | 0.000 |
| S3b sent (pp) | happy | 1.000 | 0.000 |
| S3b sent (pp) | sad | 0.000 | 0.000 |
