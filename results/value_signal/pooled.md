# Pooled valuation model across runs (exploratory, post hoc; P19)

Logit P(accept) from S1 log-probabilities, all runs stacked. Random effects: message, run × message, run × emotion; the emotion effect is the average over runs, and its SE includes how much it varies between runs. t with df = #runs − 1 (conservative); 95% CIs on the t scale; Holm over the 6 tests within each sample. Value shift > 0 = the same offer is more acceptable than after a neutral message.

| sample | emotion | measure | estimate | p_t | p_z | p_holm |
|---|---|---|---|---|---|---|
| all 7 runs | angry | value shift (logit at 30% offer) | -1.13 [-2.52, +0.25] | 0.092 | 0.045 | 0.326 |
| all 7 runs | angry | gain shift (slope on offer) | -1.06 [-2.29, +0.18] | 0.081 | 0.036 | 0.326 |
| all 7 runs | sad | value shift (logit at 30% offer) | +1.05 [-0.34, +2.43] | 0.114 | 0.065 | 0.326 |
| all 7 runs | sad | gain shift (slope on offer) | -2.54 [-3.77, -1.30] | 0.002 | 0.000 | 0.014 |
| all 7 runs | happy | value shift (logit at 30% offer) | +0.65 [-0.74, +2.03] | 0.297 | 0.254 | 0.326 |
| all 7 runs | happy | gain shift (slope on offer) | -1.43 [-2.66, -0.19] | 0.030 | 0.005 | 0.151 |
| Qwen runs only | angry | value shift (logit at 30% offer) | -1.50 [-6.12, +3.12] | 0.418 | 0.367 | 1.000 |
| Qwen runs only | angry | gain shift (slope on offer) | -1.47 [-3.42, +0.48] | 0.104 | 0.036 | 0.416 |
| Qwen runs only | sad | value shift (logit at 30% offer) | +1.59 [-3.03, +6.21] | 0.394 | 0.340 | 1.000 |
| Qwen runs only | sad | gain shift (slope on offer) | -3.65 [-5.60, -1.70] | 0.006 | 0.000 | 0.039 |
| Qwen runs only | happy | value shift (logit at 30% offer) | +1.05 [-3.56, +5.67] | 0.560 | 0.526 | 1.000 |
| Qwen runs only | happy | gain shift (slope on offer) | -2.09 [-4.04, -0.13] | 0.041 | 0.003 | 0.206 |

## Random-effect SDs (logit scale)

| sample | converged | SD msg | SD run_emo | SD run_msg |
|---|---|---|---|---|
| all 7 runs | True | 0.554 | 0.836 | 0.859 |
| Qwen runs only | True | 1.072 | 2.441 | 0.900 |
