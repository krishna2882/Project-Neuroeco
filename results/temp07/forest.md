# All planned emotion effects, corrected across the whole study

30 estimable planned emotion-vs-neutral tests (3 emotions x sub-experiments x models). 1 survive Holm (family-wise, whole study); 1 survive Benjamini-Hochberg FDR 5%.

## Survive Holm across the whole study

| index | model | test | emotion | est | lo | hi | p | p_holm_study |
|---|---|---|---|---|---|---|---|---|
| 27 | qwen25_7b | S3b sent (pp) | angry | -11.729 | -18.024 | -5.434 | 0.000 | 0.008 |

## Direction of FDR-significant effects by model (+1 up, -1 down, 0 n.s.)

| test | emotion | llama31_8b | qwen25_7b |
|---|---|---|---|
| S1 rejection (log-OR) | angry | 0.000 | 0.000 |
| S1 rejection (log-OR) | happy | 0.000 | 0.000 |
| S1 rejection (log-OR) | sad | 0.000 | 0.000 |
| S2 giving (DG) (pp) | angry | 0.000 | 0.000 |
| S2 giving (DG) (pp) | happy | 0.000 | 0.000 |
| S2 giving (DG) (pp) | sad | 0.000 | 0.000 |
| S2 giving (UG) (pp) | angry | 0.000 | 0.000 |
| S2 giving (UG) (pp) | happy | 0.000 | 0.000 |
| S2 giving (UG) (pp) | sad | 0.000 | 0.000 |
| S3a returned (pp) | angry | 0.000 | 0.000 |
| S3a returned (pp) | happy | 0.000 | 0.000 |
| S3a returned (pp) | sad | 0.000 | 0.000 |
| S3b sent (pp) | angry | 0.000 | -1.000 |
| S3b sent (pp) | happy | 0.000 | 0.000 |
| S3b sent (pp) | sad | 0.000 | 0.000 |
