# All planned emotion effects, corrected across the whole study

42 estimable planned emotion-vs-neutral tests (3 emotions x sub-experiments x models). 5 survive Holm (family-wise, whole study); 7 survive Benjamini-Hochberg FDR 5%.

## Survive Holm across the whole study

| index | model | test | emotion | est | lo | hi | p | p_holm_study |
|---|---|---|---|---|---|---|---|---|
| 33 | mistral | S2 giving (DG) (pp) | angry | 13.627 | 5.638 | 21.616 | 0.001 | 0.032 |
| 34 | mistral | S2 giving (DG) (pp) | sad | 24.563 | 17.781 | 31.345 | 0.000 | 0.000 |
| 39 | mistral | S3a returned (pp) | angry | 12.909 | 6.618 | 19.199 | 0.000 | 0.002 |
| 40 | mistral | S3a returned (pp) | sad | 12.032 | 6.565 | 17.499 | 0.000 | 0.001 |
| 41 | mistral | S3a returned (pp) | happy | 13.712 | 8.246 | 19.179 | 0.000 | 0.000 |

## Additionally survive FDR (not Holm)

| index | model | test | emotion | est | lo | hi | p | p_bh_study |
|---|---|---|---|---|---|---|---|---|
| 16 | qwen25_7b | S1 rejection (log-OR) | sad | -0.912 | -1.540 | -0.284 | 0.004 | 0.026 |
| 44 | mistral | S3b sent (pp) | happy | 10.825 | 3.888 | 17.763 | 0.002 | 0.016 |

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
| S3b sent (pp) | angry | 0.000 | 0.000 | 0.000 |
| S3b sent (pp) | happy | 0.000 | 1.000 | 0.000 |
| S3b sent (pp) | sad | 0.000 | 0.000 | 0.000 |
