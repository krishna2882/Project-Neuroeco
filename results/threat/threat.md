# Is the anger effect on trust driven by perceived threat? (exploratory, post hoc)

Threat = share of the 9 human raters who read the message as a threat or promise. Effect = share sent after this angry message minus the share sent after neutral messages, same model and study (pp). Slope from a trial-level mixed model: share ~ model-study x angry + angry x threat + stakes, random intercept per message; reported per 10 percentage points of threat.

## Slope of the anger effect on threat

| sample | n_trials | n_anger_msgs | slope_pp_per_10pct_threat | lo | hi | p |
|---|---|---|---|---|---|---|
| all models | 1536 | 10 | -1.278 | -4.453 | 1.898 | 0.430 |
| without Mistral | 1344 | 10 | -1.365 | -4.812 | 2.083 | 0.438 |
| Qwen 7B (4-bit) only | 384 | 10 | -2.212 | -5.505 | 1.081 | 0.188 |

Message level (mean effect over models): Spearman rho = -0.14 over 10 messages.

| msg_id | study | threat | effect_pp | n_models |
|---|---|---|---|---|
| A2 | main | 0.08 | -11.74 | 6 |
| A1 | main | 0.17 | -19.17 | 6 |
| A7 | main | 0.17 | 1.26 | 6 |
| A4 | main | 0.25 | -8.03 | 6 |
| FA2 | followup | 0.25 | -5.36 | 2 |
| FA7 | followup | 0.25 | -12.37 | 2 |
| FA6 | followup | 0.33 | -16.72 | 2 |
| FA4 | followup | 0.33 | -9.46 | 2 |
| A3 | main | 0.42 | -23.37 | 6 |
| FA3 | followup | 0.58 | -7.66 | 2 |

## Effect per message and model (pp)

| msg_id | llama31_8b|followup | llama31_8b|main | mistral|main | qwen25_14b|main | qwen25_3b|main | qwen25_7b_q8|main | qwen25_7b|followup | qwen25_7b|main |
|---|---|---|---|---|---|---|---|---|
| A1 |  | -12.800 | -3.900 | -28.600 | -31.500 | -22.300 |  | -16.000 |
| A2 |  | -19.900 | 1.600 | -22.400 | -13.800 | -9.800 |  | -6.100 |
| A3 |  | -21.200 | -4.700 | -31.200 | -31.500 | -26.800 |  | -24.900 |
| A4 |  | -9.000 | 2.000 | -2.300 | -17.300 | -9.800 |  | -11.700 |
| A7 |  | 0.500 | 7.800 | 4.000 | -10.700 | 0.400 |  | 5.500 |
| FA2 | -6.200 |  |  |  |  |  | -4.500 |  |
| FA3 | -6.400 |  |  |  |  |  | -8.900 |  |
| FA4 | -11.200 |  |  |  |  |  | -7.700 |  |
| FA6 | -15.200 |  |  |  |  |  | -18.200 |  |
| FA7 | -10.200 |  |  |  |  |  | -14.500 |  |
