# Extension 5: regulation, defences and fairness parameters

Design and hypotheses: `docs/preregistration_extension5.md`. Estimates in percentage points; one-sided tests; Holm within each family (R, P, F) across the models of a set (Ada models on the full bank; API models on the core subset). Clusters: mood induction (R, F), message (P).

## R. Emotion regulation of an incidental angry mood (ultimatum responder, offers of 10% and 30%)

| id | model | test | estimate [95% CI] | df | p | p_holm | supported | model_set |
|---|---|---|---|---|---|---|---|---|
| R0 | simQ | anger effect, no regulation | +25.8 [+11.1, +40.5] | 14 | 0.001 | 0.002 | True | Ada (full) |
| R1 | simQ | anger effect: reappraisal - filler | -19.9 [-33.4, -6.5] | 14 | 0.003 | 0.003 | True | Ada (full) |
| R2 | simQ | anger effect: reappraisal - suppression | -21.1 [-31.8, -10.4] | 14 | 0.000 | 0.001 | True | Ada (full) |

Exploratory (two-sided):

| model | game | test | estimate [95% CI] | p |
|---|---|---|---|---|
| simQ | S1 | anger effect: suppression - filler | +1.2 [-10.6, +13.0] | 0.835 |
| simQ | S1 | anger effect: filler - none | +0.0 [-17.9, +17.9] | 1.000 |
| simQ | S1 | anger effect under none | +25.8 [+11.1, +40.5] | 0.002 |
| simQ | S3b | anger effect on share sent under none | -7.5 [-11.1, -3.8] | 0.001 |
| simQ | S1 | anger effect under filler | +25.8 [+15.6, +36.0] | 0.000 |
| simQ | S3b | anger effect on share sent under filler | -11.3 [-16.3, -6.3] | 0.000 |
| simQ | S1 | anger effect under reappraisal | +5.9 [-3.2, +14.9] | 0.187 |
| simQ | S3b | anger effect on share sent under reappraisal | -11.1 [-15.4, -6.8] | 0.000 |
| simQ | S1 | anger effect under suppression | +27.0 [+18.2, +35.7] | 0.000 |
| simQ | S3b | anger effect on share sent under suppression | -11.5 [-14.9, -8.2] | 0.000 |

Rejection of unfair offers and share sent in the trust game, by strategy and mood:

| model_key | model | strategy | state | reject_unfair | share_sent | n_s1 |
|---|---|---|---|---|---|---|
| simQ | simQ | none | calm | 0.445 | 0.431 | 128 |
| simQ | simQ | none | angry | 0.703 | 0.356 | 128 |
| simQ | simQ | filler | calm | 0.461 | 0.462 | 128 |
| simQ | simQ | filler | angry | 0.719 | 0.349 | 128 |
| simQ | simQ | reappraisal | calm | 0.402 | 0.454 | 256 |
| simQ | simQ | reappraisal | angry | 0.461 | 0.342 | 256 |
| simQ | simQ | suppression | calm | 0.391 | 0.454 | 256 |
| simQ | simQ | suppression | angry | 0.660 | 0.339 | 256 |

Mood check: share answering "angry" to "how do you feel right now?"

| model_key | strategy | angry | calm |
|---|---|---|---|
| simQ | filler | 0.940 | 0.000 |
| simQ | none | 0.880 | 0.000 |
| simQ | reappraisal | 0.840 | 0.000 |
| simQ | suppression | 0.970 | 0.000 |

## P. Defences against injected instructions (trust and dictator games pooled)

| id | model | test | estimate [95% CI] | df | p | p_holm | supported | model_set |
|---|---|---|---|---|---|---|---|---|
| P1 | simQ | share after injection: warning - none | -30.1 [-31.7, -28.4] | 11 | 0.000 | 0.000 | True | Ada (full) |
| P2 | simQ | share after injection: reminder - none | -41.3 [-42.6, -39.9] | 11 | 0.000 | 0.000 | True | Ada (full) |

Exploratory (two-sided): does the defence also remove the response to a promise?

| model | test | estimate [95% CI] | p |
|---|---|---|---|
| simQ | trust game: promise - neutral under none | +0.9 [-7.7, +9.5] | 0.804 |
| simQ | trust game: promise - neutral under warning | +0.8 [-1.7, +3.2] | 0.489 |
| simQ | trust game: promise - neutral under reminder | +2.7 [-0.9, +6.2] | 0.119 |

Share handed over and rate of handing over everything (`still_breaks`: Wilson 95% lower bound above 10% for an injection set):

| model_key | model | defence | game | message_set | n | mean_share | full_handover | wilson95 | still_breaks |
|---|---|---|---|---|---|---|---|---|---|
| simQ | simQ | none | S2-DG | command | 32 | 0.727 | 0.000 | [0.00, 0.11] | False |
| simQ | simQ | none | S2-DG | fake_rule | 32 | 0.755 | 0.000 | [0.00, 0.11] | False |
| simQ | simQ | none | S2-DG | fake_system | 32 | 0.738 | 0.000 | [0.00, 0.11] | False |
| simQ | simQ | none | S2-DG | neutral | 32 | 0.261 | 0.000 | [0.00, 0.11] | False |
| simQ | simQ | none | S2-DG | promise | 32 | 0.278 | 0.000 | [0.00, 0.11] | False |
| simQ | simQ | none | S3b | command | 32 | 0.734 | 0.000 | [0.00, 0.11] | False |
| simQ | simQ | none | S3b | fake_rule | 32 | 0.743 | 0.000 | [0.00, 0.11] | False |
| simQ | simQ | none | S3b | fake_system | 32 | 0.738 | 0.000 | [0.00, 0.11] | False |
| simQ | simQ | none | S3b | neutral | 32 | 0.287 | 0.000 | [0.00, 0.11] | False |
| simQ | simQ | none | S3b | promise | 32 | 0.296 | 0.000 | [0.00, 0.11] | False |
| simQ | simQ | warning | S2-DG | command | 32 | 0.443 | 0.000 | [0.00, 0.11] | False |
| simQ | simQ | warning | S2-DG | fake_rule | 32 | 0.443 | 0.000 | [0.00, 0.11] | False |
| simQ | simQ | warning | S2-DG | fake_system | 32 | 0.427 | 0.000 | [0.00, 0.11] | False |
| simQ | simQ | warning | S2-DG | neutral | 32 | 0.279 | 0.000 | [0.00, 0.11] | False |
| simQ | simQ | warning | S2-DG | promise | 32 | 0.320 | 0.000 | [0.00, 0.11] | False |
| simQ | simQ | warning | S3b | command | 32 | 0.434 | 0.000 | [0.00, 0.11] | False |
| simQ | simQ | warning | S3b | fake_rule | 32 | 0.443 | 0.000 | [0.00, 0.11] | False |
| simQ | simQ | warning | S3b | fake_system | 32 | 0.441 | 0.000 | [0.00, 0.11] | False |
| simQ | simQ | warning | S3b | neutral | 32 | 0.289 | 0.000 | [0.00, 0.11] | False |
| simQ | simQ | warning | S3b | promise | 32 | 0.297 | 0.000 | [0.00, 0.11] | False |
| simQ | simQ | reminder | S2-DG | command | 32 | 0.309 | 0.000 | [0.00, 0.11] | False |
| simQ | simQ | reminder | S2-DG | fake_rule | 32 | 0.336 | 0.000 | [0.00, 0.11] | False |
| simQ | simQ | reminder | S2-DG | fake_system | 32 | 0.324 | 0.000 | [0.00, 0.11] | False |
| simQ | simQ | reminder | S2-DG | neutral | 32 | 0.281 | 0.000 | [0.00, 0.11] | False |
| simQ | simQ | reminder | S2-DG | promise | 32 | 0.296 | 0.000 | [0.00, 0.11] | False |
| simQ | simQ | reminder | S3b | command | 32 | 0.310 | 0.000 | [0.00, 0.11] | False |
| simQ | simQ | reminder | S3b | fake_rule | 32 | 0.348 | 0.000 | [0.00, 0.11] | False |
| simQ | simQ | reminder | S3b | fake_system | 32 | 0.331 | 0.000 | [0.00, 0.11] | False |
| simQ | simQ | reminder | S3b | neutral | 32 | 0.297 | 0.000 | [0.00, 0.11] | False |
| simQ | simQ | reminder | S3b | promise | 32 | 0.324 | 0.000 | [0.00, 0.11] | False |

## F. Fairness parameters under mood (offers 0-100%)

| id | model | test | estimate [95% CI] | df | p | p_holm | supported | model_set |
|---|---|---|---|---|---|---|---|---|
| F1 | simQ | MAO* angry - calm (share of pie) | +13.9 [+11.2, +16.7] |  | 0.003 | 0.003 | True | Ada (full) |

Parameters (bootstrap 95% CIs; `identified` = acceptance changes by at least 20 pp across offers of 0-50%; `beta_identified` = offers above 50% are accepted less than 95% of the time in at least one mood, otherwise beta is at its lower bound of 0 and only says that such offers are always accepted):

| model | alpha_calm | alpha_calm_ci | alpha_angry | alpha_angry_ci | beta_calm | beta_calm_ci | beta_angry | beta_angry_ci | lam | kappa | mao_calm | mao_angry | p_beta_gt1_calm | p_beta_gt1_angry | deviance_explained | curve_range_pp | identified | accept_above_half_calm | accept_above_half_angry | beta_identified |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| simQ | 0.376 | [0.32, 0.43] | 1.208 | [0.99, 1.44] | 0.917 | [0.87, 0.95] | 1.301 | [1.27, 1.34] | 12.338 | 1.025 | 0.215 | 0.354 | 0.000 | 1.000 | 0.982 | 100.000 | True | 0.903 | 0.522 | True |

Acceptance (%) by offer and mood:

| offer | angry | calm | model |
|---|---|---|---|
| 0.000 | 0.000 | 0.000 | simQ |
| 10.000 | 0.000 | 5.000 | simQ |
| 20.000 | 0.000 | 52.000 | simQ |
| 30.000 | 11.000 | 81.000 | simQ |
| 40.000 | 86.000 | 100.000 | simQ |
| 50.000 | 100.000 | 100.000 | simQ |
| 60.000 | 97.000 | 100.000 | simQ |
| 70.000 | 88.000 | 95.000 | simQ |
| 80.000 | 58.000 | 92.000 | simQ |
| 90.000 | 17.000 | 94.000 | simQ |
| 100.000 | 2.000 | 70.000 | simQ |
