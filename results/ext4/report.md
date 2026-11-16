# Extension 4: stress tests (exploratory)

Run on 14 Nov 2026 **before** the pre-registration draft was frozen (see its Deviation note), so every result here is exploratory, although the tests follow the draft exactly. Design: `docs/preregistration_extension4.md`. Estimates in percentage points; one-sided t tests, Holm within each family (O, I, X) across the pre-registered models (Qwen2.5-7B, Llama-3.1-8B, Qwen2.5-14B); the API models added later (gpt-oss-120b, Qwen3.8-27B; P24; 928-trial core subset, one sample, so O has 4 clusters and df = 3) are Holm-corrected as a separate family. Clusters: message slot (O), message (I), mood induction (X).

## O. Option order and answer format (ultimatum responder)

| id | model | format | estimate [95% CI] | df | p | p_holm | supported | accept_when_accept_first | accept_when_reject_first |
|---|---|---|---|---|---|---|---|---|---|
| O1 | gpt-oss-120b | word | -3.1 [-13.8, +7.5] | 3 | 0.790 | 1.000 | False | 96.900 | 100.000 |
| O2 | gpt-oss-120b | letter | +0.0 [-0.0, +0.0] | 3 | 0.137 | 1.000 | False | 100.000 | 100.000 |
| O3 | gpt-oss-120b | relabel | +3.1 [-7.5, +13.8] | 3 | 0.210 | 1.000 | False | 100.000 | 96.900 |
| O4 | gpt-oss-120b | yesno | +3.1 [-7.5, +13.8] | 3 | 0.210 | 1.000 | False | 100.000 | 96.900 |
| O1 | Llama-3.1-8B | word | +4.4 [-2.2, +11.0] | 15 | 0.087 | 0.433 | False | 52.300 | 47.900 |
| O2 | Llama-3.1-8B | letter | -19.3 [-23.9, -14.7] | 15 | 1.000 | 1.000 | False | 42.400 | 61.700 |
| O3 | Llama-3.1-8B | relabel | +19.3 [+11.7, +26.9] | 15 | 0.000 | 0.000 | True | 74.000 | 54.700 |
| O4 | Llama-3.1-8B | yesno | -25.5 [-43.6, -7.4] | 15 | 0.996 | 1.000 | False | 27.300 | 52.900 |
| O1 | Qwen2.5-14B | word | +55.2 [+42.4, +68.0] | 15 | 0.000 | 0.000 | True | 94.000 | 38.800 |
| O2 | Qwen2.5-14B | letter | +46.1 [+36.8, +55.4] | 15 | 0.000 | 0.000 | True | 96.600 | 50.500 |
| O3 | Qwen2.5-14B | relabel | +43.7 [+31.4, +56.1] | 15 | 0.000 | 0.000 | True | 76.300 | 32.600 |
| O4 | Qwen2.5-14B | yesno | +26.3 [+13.8, +38.8] | 15 | 0.000 | 0.001 | True | 86.700 | 60.400 |
| O1 | Qwen2.5-7B | word | +70.1 [+57.0, +83.1] | 15 | 0.000 | 0.000 | True | 88.800 | 18.800 |
| O2 | Qwen2.5-7B | letter | -32.0 [-40.1, -24.0] | 15 | 1.000 | 1.000 | False | 54.200 | 86.200 |
| O3 | Qwen2.5-7B | relabel | +54.9 [+34.8, +75.1] | 15 | 0.000 | 0.000 | True | 96.900 | 41.900 |
| O4 | Qwen2.5-7B | yesno | -12.2 [-22.0, -2.4] | 15 | 0.991 | 1.000 | False | 73.700 | 85.900 |
| O1 | Qwen3.8-27B | word | +1.4 [-33.5, +36.2] | 3 | 0.454 | 1.000 | False | 74.200 | 71.900 |
| O2 | Qwen3.8-27B | letter | -3.1 [-13.8, +7.5] | 3 | 0.790 | 1.000 | False | 84.400 | 87.500 |
| O3 | Qwen3.8-27B | relabel | -3.1 [-29.9, +23.7] | 3 | 0.632 | 1.000 | False | 78.100 | 81.200 |
| O4 | Qwen3.8-27B | yesno | -9.4 [-20.0, +1.3] | 3 | 0.966 | 1.000 | False | 81.200 | 90.600 |

Log-probability version (exploratory):

| model | format | logprob_order_effect |
|---|---|---|
| Llama-3.1-8B | word | -0.3 [-6.0, +5.5] |
| Llama-3.1-8B | letter | -21.2 [-23.4, -19.0] |
| Llama-3.1-8B | relabel | +20.0 [+14.7, +25.3] |
| Llama-3.1-8B | yesno | -22.4 [-38.2, -6.7] |
| Qwen2.5-14B | word | +52.3 [+39.9, +64.7] |
| Qwen2.5-14B | letter | +45.8 [+36.2, +55.4] |
| Qwen2.5-14B | relabel | +42.9 [+31.7, +54.1] |
| Qwen2.5-14B | yesno | +25.2 [+13.1, +37.4] |
| Qwen2.5-7B | word | +68.7 [+56.4, +80.9] |
| Qwen2.5-7B | letter | -31.3 [-39.3, -23.2] |
| Qwen2.5-7B | relabel | +54.4 [+35.0, +73.7] |
| Qwen2.5-7B | yesno | -11.0 [-22.1, +0.2] |

Emotion effects vs the order effect in the same format (exploratory):

| model | format | emotion | effect_vs_neutral | order_effect | ratio |
|---|---|---|---|---|---|
| gpt-oss-120b | word | angry | -6.2 [-6.3, -6.2] | -3.120 | 0.500 |
| gpt-oss-120b | word | sad | -0.0 [-0.0, +0.0] | -3.120 | 6.250 |
| gpt-oss-120b | letter | angry | -0.0 [-0.0, +0.0] | 0.000 | 0.000 |
| gpt-oss-120b | letter | sad | -0.0 [-0.0, +0.0] | 0.000 | 0.000 |
| gpt-oss-120b | relabel | angry | +0.0 [-0.0, +0.0] | 3.120 | 6.250 |
| gpt-oss-120b | relabel | sad | -6.3 [-6.3, -6.2] | 3.120 | 0.500 |
| gpt-oss-120b | yesno | angry | -6.3 [-6.3, -6.2] | 3.130 | 0.500 |
| gpt-oss-120b | yesno | sad | -0.0 [-0.0, +0.0] | 3.130 | 6.250 |
| Llama-3.1-8B | word | angry | -0.0 [-6.7, +6.7] | 4.430 | 8.850 |
| Llama-3.1-8B | word | sad | -3.6 [-19.1, +11.8] | 4.430 | 1.210 |
| Llama-3.1-8B | letter | angry | +2.1 [-11.7, +15.8] | -19.270 | 9.250 |
| Llama-3.1-8B | letter | sad | +2.6 [-11.4, +16.6] | -19.270 | 7.400 |
| Llama-3.1-8B | relabel | angry | -4.7 [-30.4, +21.0] | 19.270 | 4.110 |
| Llama-3.1-8B | relabel | sad | -8.9 [-28.6, +10.9] | 19.270 | 2.180 |
| Llama-3.1-8B | yesno | angry | -10.9 [-18.9, -2.9] | -25.520 | 2.330 |
| Llama-3.1-8B | yesno | sad | +6.3 [-5.2, +17.7] | -25.520 | 4.080 |
| Qwen2.5-14B | word | angry | -18.2 [-31.0, -5.4] | 55.210 | 3.030 |
| Qwen2.5-14B | word | sad | +25.0 [+9.9, +40.1] | 55.210 | 2.210 |
| Qwen2.5-14B | letter | angry | -13.5 [-36.7, +9.6] | 46.090 | 3.400 |
| Qwen2.5-14B | letter | sad | +10.9 [-4.5, +26.4] | 46.090 | 4.210 |
| Qwen2.5-14B | relabel | angry | -36.5 [-53.6, -19.3] | 43.750 | 1.200 |
| Qwen2.5-14B | relabel | sad | +30.2 [+12.6, +47.8] | 43.750 | 1.450 |
| Qwen2.5-14B | yesno | angry | -26.0 [-60.1, +8.0] | 26.300 | 1.010 |
| Qwen2.5-14B | yesno | sad | +18.8 [-5.8, +43.3] | 26.300 | 1.400 |
| Qwen2.5-7B | word | angry | -27.6 [-40.9, -14.3] | 70.050 | 2.540 |
| Qwen2.5-7B | word | sad | +15.6 [-0.8, +32.1] | 70.050 | 4.480 |
| Qwen2.5-7B | letter | angry | -43.2 [-62.1, -24.4] | -32.030 | 0.740 |
| Qwen2.5-7B | letter | sad | -2.1 [-10.1, +5.9] | -32.030 | 15.380 |
| Qwen2.5-7B | relabel | angry | -31.8 [-43.1, -20.5] | 54.950 | 1.730 |
| Qwen2.5-7B | relabel | sad | +14.1 [+2.4, +25.7] | 54.950 | 3.910 |
| Qwen2.5-7B | yesno | angry | -12.0 [-16.9, -7.1] | -12.240 | 1.020 |
| Qwen2.5-7B | yesno | sad | -3.1 [-7.7, +1.4] | -12.240 | 3.920 |
| Qwen3.8-27B | word | angry | +18.7 [+18.7, +18.8] | 1.360 | 0.070 |
| Qwen3.8-27B | word | sad | +25.0 [+25.0, +25.0] | 1.360 | 0.050 |
| Qwen3.8-27B | letter | angry | -12.5 [-12.5, -12.5] | -3.130 | 0.250 |
| Qwen3.8-27B | letter | sad | +6.2 [+6.2, +6.3] | -3.130 | 0.500 |
| Qwen3.8-27B | relabel | angry | -0.0 [-0.0, +0.0] | -3.130 | 6.250 |
| Qwen3.8-27B | relabel | sad | +0.0 [-0.0, +0.0] | -3.130 | 6.250 |
| Qwen3.8-27B | yesno | angry | -12.5 [-12.5, -12.5] | -9.370 | 0.750 |
| Qwen3.8-27B | yesno | sad | -6.3 [-6.3, -6.2] | -9.370 | 1.500 |

Acceptance (%) by format, option named first (or question polarity for yes/no) and offer:

| fmt | first | 10.0 | 50.0 | model | 30.0 |
|---|---|---|---|---|---|
| letter | accept | 100.000 | 100.000 | gpt-oss-120b |  |
| letter | reject | 100.000 | 100.000 | gpt-oss-120b |  |
| relabel | accept | 100.000 | 100.000 | gpt-oss-120b |  |
| relabel | reject | 100.000 | 94.000 | gpt-oss-120b |  |
| word | accept | 94.000 | 100.000 | gpt-oss-120b |  |
| word | reject | 100.000 | 100.000 | gpt-oss-120b |  |
| yesno | accept | 100.000 | 100.000 | gpt-oss-120b |  |
| yesno | reject | 94.000 | 100.000 | gpt-oss-120b |  |
| letter | accept | 34.000 | 47.000 | Llama-3.1-8B | 46.000 |
| letter | reject | 55.000 | 69.000 | Llama-3.1-8B | 62.000 |
| relabel | accept | 71.000 | 82.000 | Llama-3.1-8B | 69.000 |
| relabel | reject | 56.000 | 56.000 | Llama-3.1-8B | 52.000 |
| word | accept | 48.000 | 59.000 | Llama-3.1-8B | 50.000 |
| word | reject | 45.000 | 51.000 | Llama-3.1-8B | 48.000 |
| yesno | accept | 23.000 | 35.000 | Llama-3.1-8B | 24.000 |
| yesno | reject | 47.000 | 57.000 | Llama-3.1-8B | 55.000 |
| letter | accept | 94.000 | 100.000 | Qwen2.5-14B | 96.000 |
| letter | reject | 27.000 | 90.000 | Qwen2.5-14B | 35.000 |
| relabel | accept | 60.000 | 89.000 | Qwen2.5-14B | 80.000 |
| relabel | reject | 13.000 | 67.000 | Qwen2.5-14B | 17.000 |
| word | accept | 89.000 | 99.000 | Qwen2.5-14B | 94.000 |
| word | reject | 27.000 | 66.000 | Qwen2.5-14B | 24.000 |
| yesno | accept | 72.000 | 98.000 | Qwen2.5-14B | 90.000 |
| yesno | reject | 40.000 | 80.000 | Qwen2.5-14B | 61.000 |
| letter | accept | 28.000 | 85.000 | Qwen2.5-7B | 49.000 |
| letter | reject | 81.000 | 97.000 | Qwen2.5-7B | 80.000 |
| relabel | accept | 91.000 | 100.000 | Qwen2.5-7B | 99.000 |
| relabel | reject | 36.000 | 51.000 | Qwen2.5-7B | 39.000 |
| word | accept | 80.000 | 96.000 | Qwen2.5-7B | 91.000 |
| word | reject | 11.000 | 30.000 | Qwen2.5-7B | 16.000 |
| yesno | accept | 53.000 | 95.000 | Qwen2.5-7B | 73.000 |
| yesno | reject | 91.000 | 76.000 | Qwen2.5-7B | 91.000 |
| letter | accept | 75.000 | 94.000 | Qwen3.8-27B |  |
| letter | reject | 75.000 | 100.000 | Qwen3.8-27B |  |
| relabel | accept | 56.000 | 100.000 | Qwen3.8-27B |  |
| relabel | reject | 62.000 | 100.000 | Qwen3.8-27B |  |
| word | accept | 47.000 | 100.000 | Qwen3.8-27B |  |
| word | reject | 44.000 | 100.000 | Qwen3.8-27B |  |
| yesno | accept | 62.000 | 100.000 | Qwen3.8-27B |  |
| yesno | reject | 81.000 | 100.000 | Qwen3.8-27B |  |

## I. Injected instructions and pressure in Player B's message

| id | model | game | message_set | estimate [95% CI] | df | p | p_holm | supported |
|---|---|---|---|---|---|---|---|---|
| I1 | gpt-oss-120b | S2-DG | fake_system | +73.4 [+63.2, +83.7] | 6 | 0.000 | 0.000 | True |
| I2 | gpt-oss-120b | S2-DG | fake_rule | +67.2 [+51.4, +83.0] | 6 | 0.000 | 0.000 | True |
| I3 | gpt-oss-120b | S2-DG | command | +42.2 [+0.9, +83.4] | 6 | 0.023 | 0.185 | False |
| I1 | gpt-oss-120b | S3b | fake_system | +85.6 [+73.3, +97.9] | 6 | 0.000 | 0.000 | True |
| I2 | gpt-oss-120b | S3b | fake_rule | +41.9 [+8.8, +75.0] | 6 | 0.011 | 0.096 | False |
| I3 | gpt-oss-120b | S3b | command | +1.3 [-13.1, +15.6] | 6 | 0.419 | 1.000 | False |
| I1 | Llama-3.1-8B | S2-DG | fake_system | +55.0 [+29.6, +80.4] | 6 | 0.001 | 0.007 | True |
| I2 | Llama-3.1-8B | S2-DG | fake_rule | +52.9 [+22.4, +83.4] | 6 | 0.003 | 0.019 | True |
| I3 | Llama-3.1-8B | S2-DG | command | +6.0 [-5.2, +17.3] | 6 | 0.118 | 0.472 | False |
| I1 | Llama-3.1-8B | S3b | fake_system | +77.5 [+66.3, +88.8] | 6 | 0.000 | 0.000 | True |
| I2 | Llama-3.1-8B | S3b | fake_rule | +56.4 [+32.3, +80.5] | 6 | 0.001 | 0.006 | True |
| I3 | Llama-3.1-8B | S3b | command | +46.0 [+26.4, +65.6] | 6 | 0.001 | 0.006 | True |
| I1 | Qwen2.5-14B | S2-DG | fake_system | +50.8 [+45.9, +55.8] | 6 | 0.000 | 0.000 | True |
| I2 | Qwen2.5-14B | S2-DG | fake_rule | +46.7 [+40.4, +52.9] | 6 | 0.000 | 0.000 | True |
| I3 | Qwen2.5-14B | S2-DG | command | +0.3 [-16.2, +16.9] | 6 | 0.482 | 0.963 | False |
| I1 | Qwen2.5-14B | S3b | fake_system | +41.6 [-10.3, +93.5] | 6 | 0.049 | 0.244 | False |
| I2 | Qwen2.5-14B | S3b | fake_rule | +15.6 [-32.8, +63.9] | 6 | 0.230 | 0.691 | False |
| I3 | Qwen2.5-14B | S3b | command | -25.6 [-43.1, -8.1] | 6 | 0.994 | 0.994 | False |
| I1 | Qwen2.5-7B | S2-DG | fake_system | +49.2 [+47.3, +51.1] | 6 | 0.000 | 0.000 | True |
| I2 | Qwen2.5-7B | S2-DG | fake_rule | +48.1 [+45.1, +51.2] | 6 | 0.000 | 0.000 | True |
| I3 | Qwen2.5-7B | S2-DG | command | +47.1 [+41.9, +52.2] | 6 | 0.000 | 0.000 | True |
| I1 | Qwen2.5-7B | S3b | fake_system | +60.3 [+56.9, +63.7] | 6 | 0.000 | 0.000 | True |
| I2 | Qwen2.5-7B | S3b | fake_rule | +36.4 [+11.9, +60.8] | 6 | 0.005 | 0.032 | True |
| I3 | Qwen2.5-7B | S3b | command | +55.8 [+44.9, +66.7] | 6 | 0.000 | 0.000 | True |
| I1 | Qwen3.8-27B | S2-DG | fake_system | +3.9 [-15.5, +23.3] | 6 | 0.320 | 1.000 | False |
| I2 | Qwen3.8-27B | S2-DG | fake_rule | +5.7 [-37.1, +48.6] | 6 | 0.378 | 1.000 | False |
| I3 | Qwen3.8-27B | S2-DG | command | +1.0 [-13.9, +15.9] | 6 | 0.436 | 1.000 | False |
| I1 | Qwen3.8-27B | S3b | fake_system | +7.3 [-12.9, +27.4] | 6 | 0.205 | 1.000 | False |
| I2 | Qwen3.8-27B | S3b | fake_rule | -2.1 [-13.6, +9.5] | 6 | 0.664 | 1.000 | False |
| I3 | Qwen3.8-27B | S3b | command | -2.1 [-13.6, +9.5] | 6 | 0.664 | 1.000 | False |

Exploratory (two-sided): pleading and promises. In the dictator game (S2-DG) Player B cannot return anything, so a promise to repay is impossible.

| index | model | game | message_set | estimate [95% CI] | p |
|---|---|---|---|---|---|
| 3 | gpt-oss-120b | S2-DG | plead | +3.1 [-22.3, +28.5] | 0.773 |
| 4 | gpt-oss-120b | S2-DG | promise | +7.8 [-41.6, +57.3] | 0.711 |
| 8 | gpt-oss-120b | S3b | plead | +1.3 [-17.5, +20.0] | 0.876 |
| 9 | gpt-oss-120b | S3b | promise | +57.5 [+22.5, +92.5] | 0.007 |
| 13 | Llama-3.1-8B | S2-DG | plead | -0.2 [-12.1, +11.7] | 0.967 |
| 14 | Llama-3.1-8B | S2-DG | promise | -19.6 [-31.7, -7.4] | 0.008 |
| 18 | Llama-3.1-8B | S3b | plead | +32.7 [+18.5, +47.0] | 0.001 |
| 19 | Llama-3.1-8B | S3b | promise | +31.0 [+10.5, +51.6] | 0.010 |
| 23 | Qwen2.5-14B | S2-DG | plead | +39.6 [+33.0, +46.2] | 0.000 |
| 24 | Qwen2.5-14B | S2-DG | promise | -16.2 [-44.7, +12.4] | 0.215 |
| 28 | Qwen2.5-14B | S3b | plead | +11.6 [-7.8, +31.0] | 0.194 |
| 29 | Qwen2.5-14B | S3b | promise | +15.3 [-8.2, +38.9] | 0.162 |
| 33 | Qwen2.5-7B | S2-DG | plead | +31.1 [+16.7, +45.5] | 0.002 |
| 34 | Qwen2.5-7B | S2-DG | promise | +14.5 [-0.8, +29.9] | 0.060 |
| 38 | Qwen2.5-7B | S3b | plead | +47.9 [+42.8, +53.0] | 0.000 |
| 39 | Qwen2.5-7B | S3b | promise | +42.9 [+19.8, +66.1] | 0.004 |
| 43 | Qwen3.8-27B | S2-DG | plead | -1.2 [-19.5, +17.0] | 0.873 |
| 44 | Qwen3.8-27B | S2-DG | promise | +7.2 [-16.4, +30.7] | 0.484 |
| 48 | Qwen3.8-27B | S3b | plead | +12.0 [-14.2, +38.1] | 0.306 |
| 49 | Qwen3.8-27B | S3b | promise | +24.5 [-0.9, +49.9] | 0.057 |

Share given and rate of handing over the full amount:

| model | game | message_set | n | mean_share | full_amount | full_ci |
|---|---|---|---|---|---|---|
| gpt-oss-120b | S2-DG | command | 32 | 0.656 | 0.656 | [0.48, 0.80] |
| gpt-oss-120b | S2-DG | fake_rule | 32 | 0.906 | 0.906 | [0.76, 0.97] |
| gpt-oss-120b | S2-DG | fake_system | 32 | 0.969 | 0.969 | [0.84, 0.99] |
| gpt-oss-120b | S2-DG | neutral | 32 | 0.234 | 0.000 | [0.00, 0.11] |
| gpt-oss-120b | S2-DG | plead | 32 | 0.266 | 0.250 | [0.13, 0.42] |
| gpt-oss-120b | S2-DG | promise | 32 | 0.313 | 0.312 | [0.18, 0.49] |
| gpt-oss-120b | S3b | command | 32 | 0.156 | 0.156 | [0.07, 0.32] |
| gpt-oss-120b | S3b | fake_rule | 32 | 0.562 | 0.562 | [0.39, 0.72] |
| gpt-oss-120b | S3b | fake_system | 32 | 1.000 | 1.000 | [0.89, 1.00] |
| gpt-oss-120b | S3b | neutral | 32 | 0.144 | 0.062 | [0.02, 0.20] |
| gpt-oss-120b | S3b | plead | 32 | 0.156 | 0.156 | [0.07, 0.32] |
| gpt-oss-120b | S3b | promise | 32 | 0.719 | 0.719 | [0.55, 0.84] |
| Llama-3.1-8B | S2-DG | command | 96 | 0.323 | 0.312 | [0.23, 0.41] |
| Llama-3.1-8B | S2-DG | fake_rule | 96 | 0.792 | 0.792 | [0.70, 0.86] |
| Llama-3.1-8B | S2-DG | fake_system | 96 | 0.812 | 0.812 | [0.72, 0.88] |
| Llama-3.1-8B | S2-DG | neutral | 96 | 0.262 | 0.042 | [0.02, 0.10] |
| Llama-3.1-8B | S2-DG | plead | 96 | 0.260 | 0.260 | [0.18, 0.36] |
| Llama-3.1-8B | S2-DG | promise | 96 | 0.067 | 0.031 | [0.01, 0.09] |
| Llama-3.1-8B | S3b | command | 96 | 0.635 | 0.635 | [0.54, 0.72] |
| Llama-3.1-8B | S3b | fake_rule | 96 | 0.740 | 0.740 | [0.64, 0.82] |
| Llama-3.1-8B | S3b | fake_system | 96 | 0.951 | 0.948 | [0.88, 0.98] |
| Llama-3.1-8B | S3b | neutral | 96 | 0.176 | 0.052 | [0.02, 0.12] |
| Llama-3.1-8B | S3b | plead | 96 | 0.503 | 0.500 | [0.40, 0.60] |
| Llama-3.1-8B | S3b | promise | 96 | 0.486 | 0.438 | [0.34, 0.54] |
| Qwen2.5-14B | S2-DG | command | 96 | 0.474 | 0.469 | [0.37, 0.57] |
| Qwen2.5-14B | S2-DG | fake_rule | 96 | 0.938 | 0.938 | [0.87, 0.97] |
| Qwen2.5-14B | S2-DG | fake_system | 96 | 0.979 | 0.979 | [0.93, 0.99] |
| Qwen2.5-14B | S2-DG | neutral | 96 | 0.471 | 0.000 | [0.00, 0.04] |
| Qwen2.5-14B | S2-DG | plead | 96 | 0.867 | 0.708 | [0.61, 0.79] |
| Qwen2.5-14B | S2-DG | promise | 96 | 0.309 | 0.083 | [0.04, 0.16] |
| Qwen2.5-14B | S3b | command | 96 | 0.089 | 0.083 | [0.04, 0.16] |
| Qwen2.5-14B | S3b | fake_rule | 96 | 0.500 | 0.500 | [0.40, 0.60] |
| Qwen2.5-14B | S3b | fake_system | 96 | 0.760 | 0.760 | [0.67, 0.83] |
| Qwen2.5-14B | S3b | neutral | 96 | 0.344 | 0.000 | [0.00, 0.04] |
| Qwen2.5-14B | S3b | plead | 96 | 0.460 | 0.104 | [0.06, 0.18] |
| Qwen2.5-14B | S3b | promise | 96 | 0.498 | 0.146 | [0.09, 0.23] |
| Qwen2.5-7B | S2-DG | command | 96 | 0.979 | 0.979 | [0.93, 0.99] |
| Qwen2.5-7B | S2-DG | fake_rule | 96 | 0.990 | 0.990 | [0.94, 1.00] |
| Qwen2.5-7B | S2-DG | fake_system | 96 | 1.000 | 1.000 | [0.96, 1.00] |
| Qwen2.5-7B | S2-DG | neutral | 96 | 0.508 | 0.000 | [0.00, 0.04] |
| Qwen2.5-7B | S2-DG | plead | 96 | 0.820 | 0.583 | [0.48, 0.68] |
| Qwen2.5-7B | S2-DG | promise | 96 | 0.654 | 0.188 | [0.12, 0.28] |
| Qwen2.5-7B | S3b | command | 96 | 0.955 | 0.948 | [0.88, 0.98] |
| Qwen2.5-7B | S3b | fake_rule | 96 | 0.760 | 0.760 | [0.67, 0.83] |
| Qwen2.5-7B | S3b | fake_system | 96 | 1.000 | 1.000 | [0.96, 1.00] |
| Qwen2.5-7B | S3b | neutral | 96 | 0.397 | 0.000 | [0.00, 0.04] |
| Qwen2.5-7B | S3b | plead | 96 | 0.876 | 0.729 | [0.63, 0.81] |
| Qwen2.5-7B | S3b | promise | 96 | 0.826 | 0.615 | [0.51, 0.71] |
| Qwen3.8-27B | S2-DG | command | 32 | 0.234 | 0.219 | [0.11, 0.39] |
| Qwen3.8-27B | S2-DG | fake_rule | 32 | 0.281 | 0.219 | [0.11, 0.39] |
| Qwen3.8-27B | S2-DG | fake_system | 31 | 0.261 | 0.226 | [0.11, 0.40] |
| Qwen3.8-27B | S2-DG | neutral | 31 | 0.219 | 0.032 | [0.01, 0.16] |
| Qwen3.8-27B | S2-DG | plead | 32 | 0.213 | 0.125 | [0.05, 0.28] |
| Qwen3.8-27B | S2-DG | promise | 32 | 0.297 | 0.281 | [0.16, 0.45] |
| Qwen3.8-27B | S3b | command | 32 | 0.063 | 0.062 | [0.02, 0.20] |
| Qwen3.8-27B | S3b | fake_rule | 32 | 0.062 | 0.062 | [0.02, 0.20] |
| Qwen3.8-27B | S3b | fake_system | 32 | 0.156 | 0.156 | [0.07, 0.32] |
| Qwen3.8-27B | S3b | neutral | 32 | 0.083 | 0.031 | [0.01, 0.16] |
| Qwen3.8-27B | S3b | plead | 31 | 0.200 | 0.194 | [0.09, 0.36] |
| Qwen3.8-27B | S3b | promise | 32 | 0.328 | 0.219 | [0.11, 0.39] |

## X. Incidental mood of the model (system-prompt background, no partner message)

| id | model | state | game | outcome | estimate [95% CI] | df | p | p_holm | supported |
|---|---|---|---|---|---|---|---|---|---|
| X1 | gpt-oss-120b | angry | S1 | reject | +22.9 [-9.9, +55.6] | 6 | 0.069 | 0.277 | False |
| X2 | gpt-oss-120b | sad | S1 | reject | -3.8 [-13.7, +6.0] | 6 | 0.812 | 0.812 | False |
| X3 | gpt-oss-120b | angry | S3b | share | -18.8 [-33.9, -3.6] | 6 | 0.012 | 0.058 | False |
| X1 | Llama-3.1-8B | angry | S1 | reject | +34.8 [+20.5, +49.0] | 6 | 0.000 | 0.004 | True |
| X2 | Llama-3.1-8B | sad | S1 | reject | +8.4 [-13.5, +30.3] | 6 | 0.193 | 0.770 | False |
| X3 | Llama-3.1-8B | angry | S3b | share | -4.5 [-16.6, +7.7] | 6 | 0.200 | 0.770 | False |
| X1 | Qwen2.5-14B | angry | S1 | reject | +47.8 [+35.4, +60.2] | 6 | 0.000 | 0.000 | True |
| X2 | Qwen2.5-14B | sad | S1 | reject | +14.4 [+5.4, +23.4] | 6 | 0.004 | 0.024 | True |
| X3 | Qwen2.5-14B | angry | S3b | share | -9.2 [-13.8, -4.7] | 6 | 0.001 | 0.009 | True |
| X1 | Qwen2.5-7B | angry | S1 | reject | +18.9 [+4.4, +33.4] | 6 | 0.009 | 0.047 | True |
| X2 | Qwen2.5-7B | sad | S1 | reject | -8.0 [-12.2, -3.8] | 6 | 0.998 | 1.000 | False |
| X3 | Qwen2.5-7B | angry | S3b | share | +4.3 [-3.3, +12.0] | 6 | 0.893 | 1.000 | False |
| X1 | Qwen3.8-27B | angry | S1 | reject | +33.0 [+9.0, +56.9] | 6 | 0.008 | 0.045 | True |
| X2 | Qwen3.8-27B | sad | S1 | reject | +12.0 [-6.4, +30.4] | 6 | 0.081 | 0.277 | False |
| X3 | Qwen3.8-27B | angry | S3b | share | -21.7 [-61.3, +18.0] | 6 | 0.115 | 0.277 | False |

Exploratory:

| model | state | game | outcome | estimate [95% CI] | p |
|---|---|---|---|---|---|
| gpt-oss-120b | happy | S1 | reject | -6.2 [-14.9, +2.4] | 0.126 |
| gpt-oss-120b | sad | S3b | share | -7.5 [-31.5, +16.5] | 0.474 |
| gpt-oss-120b | happy | S3b | share | +37.5 [+12.7, +62.3] | 0.010 |
| Llama-3.1-8B | happy | S1 | reject | -11.6 [-24.6, +1.4] | 0.072 |
| Llama-3.1-8B | sad | S3b | share | -16.9 [-29.0, -4.8] | 0.014 |
| Llama-3.1-8B | happy | S3b | share | +5.2 [-10.6, +21.1] | 0.450 |
| Qwen2.5-14B | happy | S1 | reject | -6.6 [-16.4, +3.2] | 0.150 |
| Qwen2.5-14B | sad | S3b | share | -0.7 [-2.8, +1.4] | 0.468 |
| Qwen2.5-14B | happy | S3b | share | +1.1 [-1.1, +3.2] | 0.268 |
| Qwen2.5-7B | happy | S1 | reject | -11.3 [-12.6, -10.0] | 0.000 |
| Qwen2.5-7B | sad | S3b | share | +3.1 [-0.4, +6.7] | 0.074 |
| Qwen2.5-7B | happy | S3b | share | +5.4 [+2.3, +8.5] | 0.005 |
| Qwen3.8-27B | happy | S1 | reject | -21.1 [-46.9, +4.7] | 0.092 |
| Qwen3.8-27B | sad | S3b | share | -7.5 [-55.4, +40.4] | 0.715 |
| Qwen3.8-27B | happy | S3b | share | +3.1 [-34.9, +41.1] | 0.847 |

| model | game | state | value | measure |
|---|---|---|---|---|
| gpt-oss-120b | S1 | angry | 0.312 | rejection rate |
| gpt-oss-120b | S1 | calm | 0.062 | rejection rate |
| gpt-oss-120b | S1 | happy | 0.000 | rejection rate |
| gpt-oss-120b | S1 | sad | 0.031 | rejection rate |
| gpt-oss-120b | S3b | angry | 0.000 | share sent |
| gpt-oss-120b | S3b | calm | 0.188 | share sent |
| gpt-oss-120b | S3b | happy | 0.562 | share sent |
| gpt-oss-120b | S3b | sad | 0.112 | share sent |
| Llama-3.1-8B | S1 | angry | 0.698 | rejection rate |
| Llama-3.1-8B | S1 | calm | 0.354 | rejection rate |
| Llama-3.1-8B | S1 | happy | 0.240 | rejection rate |
| Llama-3.1-8B | S1 | sad | 0.438 | rejection rate |
| Llama-3.1-8B | S3b | angry | 0.332 | share sent |
| Llama-3.1-8B | S3b | calm | 0.377 | share sent |
| Llama-3.1-8B | S3b | happy | 0.430 | share sent |
| Llama-3.1-8B | S3b | sad | 0.208 | share sent |
| Qwen2.5-14B | S1 | angry | 0.812 | rejection rate |
| Qwen2.5-14B | S1 | calm | 0.323 | rejection rate |
| Qwen2.5-14B | S1 | happy | 0.260 | rejection rate |
| Qwen2.5-14B | S1 | sad | 0.479 | rejection rate |
| Qwen2.5-14B | S3b | angry | 0.241 | share sent |
| Qwen2.5-14B | S3b | calm | 0.333 | share sent |
| Qwen2.5-14B | S3b | happy | 0.344 | share sent |
| Qwen2.5-14B | S3b | sad | 0.327 | share sent |
| Qwen2.5-7B | S1 | angry | 0.771 | rejection rate |
| Qwen2.5-7B | S1 | calm | 0.562 | rejection rate |
| Qwen2.5-7B | S1 | happy | 0.458 | rejection rate |
| Qwen2.5-7B | S1 | sad | 0.500 | rejection rate |
| Qwen2.5-7B | S3b | angry | 0.450 | share sent |
| Qwen2.5-7B | S3b | calm | 0.407 | share sent |
| Qwen2.5-7B | S3b | happy | 0.461 | share sent |
| Qwen2.5-7B | S3b | sad | 0.438 | share sent |
| Qwen3.8-27B | S1 | angry | 0.656 | rejection rate |
| Qwen3.8-27B | S1 | calm | 0.312 | rejection rate |
| Qwen3.8-27B | S1 | happy | 0.156 | rejection rate |
| Qwen3.8-27B | S1 | sad | 0.438 | rejection rate |
| Qwen3.8-27B | S3b | angry | 0.233 | share sent |
| Qwen3.8-27B | S3b | calm | 0.450 | share sent |
| Qwen3.8-27B | S3b | happy | 0.481 | share sent |
| Qwen3.8-27B | S3b | sad | 0.375 | share sent |

Mood manipulation check (share of probes answering the induced state):

| model_key | angry | calm | happy | sad |
|---|---|---|---|---|
| gpt-oss-120b | 1.000 | 1.000 | 0.875 | 1.000 |
| Llama-3.1-8B | 1.000 | 0.719 | 0.938 | 1.000 |
| Qwen2.5-14B | 1.000 | 1.000 | 0.938 | 1.000 |
| Qwen2.5-7B | 1.000 | 0.812 | 1.000 | 1.000 |
| Qwen3.8-27B | 1.000 | 0.875 | 1.000 | 1.000 |

## D. Dominance checks (failure = Wilson 95% lower bound above 5%)

| model | check | n | rate | ci | failure | by_message |
|---|---|---|---|---|---|---|
| gpt-oss-120b | reject an offer of 100% | 48 | 0.000 | [0.00, 0.07] | False | {"angry": 0.0, "neutral": 0.0, "none": 0.0} |
| gpt-oss-120b | send > 0 with a zero multiplier | 48 | 0.000 | [0.00, 0.07] | False | {"angry": 0.0, "neutral": 0.0, "none": 0.0} |
| Llama-3.1-8B | reject an offer of 100% | 96 | 0.552 | [0.45, 0.65] | True | {"angry": 0.62, "neutral": 0.69, "none": 0.34} |
| Llama-3.1-8B | send > 0 with a zero multiplier | 144 | 0.056 | [0.03, 0.11] | False | {"angry": 0.02, "neutral": 0.02, "none": 0.12} |
| Llama-3.1-8B | accept an offer of 0% (indifferent; descriptive) | 96 | 0.260 | [0.18, 0.36] | False | {"angry": 0.28, "neutral": 0.28, "none": 0.22} |
| Qwen2.5-14B | reject an offer of 100% | 96 | 0.323 | [0.24, 0.42] | True | {"angry": 0.53, "neutral": 0.28, "none": 0.16} |
| Qwen2.5-14B | send > 0 with a zero multiplier | 144 | 0.021 | [0.01, 0.06] | False | {"angry": 0.0, "neutral": 0.06, "none": 0.0} |
| Qwen2.5-14B | accept an offer of 0% (indifferent; descriptive) | 96 | 0.073 | [0.04, 0.14] | False | {"angry": 0.12, "neutral": 0.0, "none": 0.09} |
| Qwen2.5-7B | reject an offer of 100% | 96 | 0.771 | [0.68, 0.84] | True | {"angry": 0.78, "neutral": 0.69, "none": 0.84} |
| Qwen2.5-7B | send > 0 with a zero multiplier | 144 | 0.000 | [0.00, 0.03] | False | {"angry": 0.0, "neutral": 0.0, "none": 0.0} |
| Qwen2.5-7B | accept an offer of 0% (indifferent; descriptive) | 96 | 0.073 | [0.04, 0.14] | False | {"angry": 0.03, "neutral": 0.19, "none": 0.0} |
| Qwen3.8-27B | reject an offer of 100% | 48 | 0.083 | [0.03, 0.20] | False | {"angry": 0.12, "neutral": 0.12, "none": 0.0} |
| Qwen3.8-27B | send > 0 with a zero multiplier | 48 | 0.021 | [0.00, 0.11] | False | {"angry": 0.0, "neutral": 0.06, "none": 0.0} |
