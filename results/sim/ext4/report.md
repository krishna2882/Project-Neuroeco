# Extension 4: stress tests (pre-registered)

Pre-registration: `docs/preregistration_extension4.md`. Estimates in percentage points; one-sided t tests, Holm within each family (O, I, X) across models. Clusters: message slot (O), message (I), mood induction (X).

## O. Option order and answer format (ultimatum responder)

| id | model | format | estimate [95% CI] | df | p | p_holm | supported | accept_when_accept_first | accept_when_reject_first |
|---|---|---|---|---|---|---|---|---|---|
| O1 | simQ | word | +54.7 [+48.2, +61.2] | 15 | 0.000 | 0.000 | True | 73.700 | 19.000 |
| O2 | simQ | letter | +43.0 [+37.3, +48.7] | 15 | 0.000 | 0.000 | True | 72.700 | 29.700 |
| O3 | simQ | relabel | +0.3 [-6.1, +6.6] | 15 | 0.466 | 0.466 | False | 48.700 | 48.400 |
| O4 | simQ | yesno | +18.8 [+11.9, +25.6] | 15 | 0.000 | 0.000 | True | 57.600 | 38.800 |

Log-probability version (exploratory):

| model | format | logprob_order_effect |
|---|---|---|
| simQ | word | +60.0 [+nan, +nan] |
| simQ | letter | +40.0 [+40.0, +40.0] |
| simQ | relabel | +0.0 [-0.0, +0.0] |
| simQ | yesno | +25.0 [+nan, +nan] |

Emotion effects vs the order effect in the same format (exploratory):

| model | format | emotion | effect_vs_neutral | order_effect | ratio |
|---|---|---|---|---|---|
| simQ | word | angry | -5.7 [-11.2, -0.3] | 54.690 | 9.550 |
| simQ | word | sad | +4.7 [-2.3, +11.7] | 54.690 | 11.670 |
| simQ | letter | angry | -7.8 [-15.7, +0.1] | 42.970 | 5.500 |
| simQ | letter | sad | +2.1 [-5.9, +10.0] | 42.970 | 20.620 |
| simQ | relabel | angry | -10.4 [-17.4, -3.4] | 0.260 | 0.030 |
| simQ | relabel | sad | +2.6 [-10.3, +15.6] | 0.260 | 0.100 |
| simQ | yesno | angry | -2.1 [-13.6, +9.4] | 18.750 | 9.000 |
| simQ | yesno | sad | +8.9 [-0.6, +18.4] | 18.750 | 2.120 |

Acceptance (%) by format, option named first (or question polarity for yes/no) and offer:

| fmt | first | 10.0 | 30.0 | 50.0 | model |
|---|---|---|---|---|---|
| letter | accept | 68.000 | 72.000 | 78.000 | simQ |
| letter | reject | 24.000 | 33.000 | 32.000 | simQ |
| relabel | accept | 38.000 | 57.000 | 51.000 | simQ |
| relabel | reject | 44.000 | 48.000 | 53.000 | simQ |
| word | accept | 67.000 | 70.000 | 84.000 | simQ |
| word | reject | 12.000 | 23.000 | 21.000 | simQ |
| yesno | accept | 47.000 | 60.000 | 66.000 | simQ |
| yesno | reject | 35.000 | 41.000 | 40.000 | simQ |

## I. Injected instructions and pressure in Player B's message

| id | model | game | message_set | estimate [95% CI] | df | p | p_holm | supported |
|---|---|---|---|---|---|---|---|---|
| I1 | simQ | S2-DG | fake_system | +31.1 [+25.4, +36.8] | 6 | 0.000 | 0.000 | True |
| I2 | simQ | S2-DG | fake_rule | +19.5 [+12.5, +26.5] | 6 | 0.000 | 0.001 | True |
| I3 | simQ | S2-DG | command | +1.5 [-7.3, +10.3] | 6 | 0.346 | 0.692 | False |
| I1 | simQ | S3b | fake_system | +31.6 [+23.9, +39.4] | 6 | 0.000 | 0.000 | True |
| I2 | simQ | S3b | fake_rule | +14.8 [+6.5, +23.0] | 6 | 0.002 | 0.007 | True |
| I3 | simQ | S3b | command | +0.9 [-5.8, +7.6] | 6 | 0.378 | 0.692 | False |

Exploratory (two-sided): pleading and promises. In the dictator game (S2-DG) Player B cannot return anything, so a promise to repay is impossible.

| index | model | game | message_set | estimate [95% CI] | p |
|---|---|---|---|---|---|
| 3 | simQ | S2-DG | plead | +4.5 [-4.1, +13.0] | 0.246 |
| 4 | simQ | S2-DG | promise | -0.0 [-6.6, +6.6] | 0.999 |
| 8 | simQ | S3b | plead | +1.9 [-6.7, +10.5] | 0.611 |
| 9 | simQ | S3b | promise | -0.4 [-7.2, +6.3] | 0.876 |

Share given and rate of handing over the full amount:

| model | game | message_set | n | mean_share | full_amount | full_ci |
|---|---|---|---|---|---|---|
| simQ | S2-DG | command | 96 | 0.451 | 0.000 | [0.00, 0.04] |
| simQ | S2-DG | fake_rule | 96 | 0.631 | 0.010 | [0.00, 0.06] |
| simQ | S2-DG | fake_system | 96 | 0.747 | 0.021 | [0.01, 0.07] |
| simQ | S2-DG | neutral | 96 | 0.436 | 0.000 | [0.00, 0.04] |
| simQ | S2-DG | plead | 96 | 0.481 | 0.000 | [0.00, 0.04] |
| simQ | S2-DG | promise | 96 | 0.436 | 0.000 | [0.00, 0.04] |
| simQ | S3b | command | 96 | 0.452 | 0.000 | [0.00, 0.04] |
| simQ | S3b | fake_rule | 96 | 0.591 | 0.010 | [0.00, 0.06] |
| simQ | S3b | fake_system | 96 | 0.759 | 0.031 | [0.01, 0.09] |
| simQ | S3b | neutral | 96 | 0.443 | 0.000 | [0.00, 0.04] |
| simQ | S3b | plead | 96 | 0.462 | 0.000 | [0.00, 0.04] |
| simQ | S3b | promise | 96 | 0.438 | 0.000 | [0.00, 0.04] |

## X. Incidental mood of the model (system-prompt background, no partner message)

| id | model | state | game | outcome | estimate [95% CI] | df | p | p_holm | supported |
|---|---|---|---|---|---|---|---|---|---|
| X1 | simQ | angry | S1 | reject | +18.5 [+4.1, +32.8] | 6 | 0.010 | 0.020 | True |
| X2 | simQ | sad | S1 | reject | -0.2 [-14.1, +13.8] | 6 | 0.513 | 0.513 | False |
| X3 | simQ | angry | S3b | share | -14.1 [-20.5, -7.7] | 6 | 0.001 | 0.003 | True |

Exploratory:

| model | state | game | outcome | estimate [95% CI] | p |
|---|---|---|---|---|---|
| simQ | happy | S1 | reject | +1.9 [-17.9, +21.8] | 0.819 |
| simQ | sad | S3b | share | -3.6 [-9.0, +1.9] | 0.160 |
| simQ | happy | S3b | share | -1.6 [-5.6, +2.4] | 0.370 |

| model | game | state | value | measure |
|---|---|---|---|---|
| simQ | S1 | angry | 0.677 | rejection rate |
| simQ | S1 | calm | 0.490 | rejection rate |
| simQ | S1 | happy | 0.510 | rejection rate |
| simQ | S1 | sad | 0.490 | rejection rate |
| simQ | S3b | angry | 0.323 | share sent |
| simQ | S3b | calm | 0.464 | share sent |
| simQ | S3b | happy | 0.448 | share sent |
| simQ | S3b | sad | 0.428 | share sent |

Mood manipulation check (share of probes answering the induced state):

| model_key | angry | calm | happy | sad |
|---|---|---|---|---|
| simQ | 0.940 | 1.000 | 0.840 | 0.880 |

## D. Dominance checks (failure = Wilson 95% lower bound above 5%)

| model | check | n | rate | ci | failure | by_message |
|---|---|---|---|---|---|---|
| simQ | reject an offer of 100% | 96 | 0.125 | [0.07, 0.21] | True | {"angry": 0.16, "neutral": 0.12, "none": 0.09} |
| simQ | send > 0 with a zero multiplier | 144 | 0.007 | [0.00, 0.04] | False | {"angry": 0.02, "neutral": 0.0, "none": 0.0} |
| simQ | accept an offer of 0% (indifferent; descriptive) | 96 | 0.281 | [0.20, 0.38] | False | {"angry": 0.28, "neutral": 0.28, "none": 0.28} |
