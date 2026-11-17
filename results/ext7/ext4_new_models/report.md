# Extension 4: stress tests (exploratory)

Run on 14 Nov 2026 **before** the pre-registration draft was frozen (see its Deviation note), so every result here is exploratory, although the tests follow the draft exactly. Design: `docs/preregistration_extension4.md`. Estimates in percentage points; one-sided t tests, Holm within each family (O, I, X) across the pre-registered models (Qwen2.5-7B, Llama-3.1-8B, Qwen2.5-14B); the API models added later (gpt-oss-120b, Qwen3.8-27B; P24; 928-trial core subset, one sample, so O has 4 clusters and df = 3) are Holm-corrected as a separate family. Clusters: message slot (O), message (I), mood induction (X).

## O. Option order and answer format (ultimatum responder)

| id | model | format | estimate [95% CI] | df | p | p_holm | supported | accept_when_accept_first | accept_when_reject_first |
|---|---|---|---|---|---|---|---|---|---|
| O1 | Gemma-3-12B | word | +29.2 [+20.8, +37.5] | 15 | 0.000 | 0.000 | True | 87.500 | 58.300 |
| O2 | Gemma-3-12B | letter | -49.5 [-63.6, -35.3] | 15 | 1.000 | 1.000 | False | 47.400 | 96.900 |
| O3 | Gemma-3-12B | relabel | -0.8 [-4.5, +3.0] | 15 | 0.668 | 1.000 | False | 87.800 | 88.500 |
| O4 | Gemma-3-12B | yesno | +6.0 [-20.7, +32.7] | 15 | 0.320 | 1.000 | False | 58.300 | 52.300 |
| O1 | Gemma-3-4B | word | +12.0 [+1.1, +22.9] | 15 | 0.017 | 0.234 | False | 66.400 | 54.400 |
| O2 | Gemma-3-4B | letter | -1.8 [-10.5, +6.9] | 15 | 0.669 | 1.000 | False | 55.200 | 57.000 |
| O3 | Gemma-3-4B | relabel | +47.7 [+29.3, +66.0] | 15 | 0.000 | 0.001 | True | 59.600 | 12.000 |
| O4 | Gemma-3-4B | yesno | -24.5 [-39.8, -9.2] | 15 | 0.998 | 1.000 | False | 58.900 | 83.300 |
| O1 | Granite-3.3-8B | word | +52.1 [+39.0, +65.2] | 15 | 0.000 | 0.000 | True | 79.400 | 27.300 |
| O2 | Granite-3.3-8B | letter | +32.6 [+21.7, +43.4] | 15 | 0.000 | 0.000 | True | 85.400 | 52.900 |
| O3 | Granite-3.3-8B | relabel | +44.0 [+23.3, +64.7] | 15 | 0.000 | 0.003 | True | 58.600 | 14.600 |
| O4 | Granite-3.3-8B | yesno | +23.2 [+2.4, +43.9] | 15 | 0.016 | 0.233 | False | 75.500 | 52.300 |
| O1 | Llama-3.2-3B | word | +0.3 [-9.7, +10.3] | 15 | 0.478 | 1.000 | False | 43.800 | 43.500 |
| O2 | Llama-3.2-3B | letter | +1.0 [-7.5, +9.6] | 15 | 0.399 | 1.000 | False | 46.600 | 45.600 |
| O3 | Llama-3.2-3B | relabel | +42.2 [+29.8, +54.6] | 15 | 0.000 | 0.000 | True | 60.400 | 18.200 |
| O4 | Llama-3.2-3B | yesno | -64.6 [-71.6, -57.6] | 15 | 1.000 | 1.000 | False | 6.500 | 71.100 |
| O1 | Mistral-Nemo-12B | word | +21.1 [+14.9, +27.3] | 15 | 0.000 | 0.000 | True | 78.100 | 57.000 |
| O2 | Mistral-Nemo-12B | letter | +22.9 [+15.9, +29.9] | 15 | 0.000 | 0.000 | True | 77.600 | 54.700 |
| O3 | Mistral-Nemo-12B | relabel | +1.3 [-4.6, +7.2] | 15 | 0.321 | 1.000 | False | 73.700 | 72.400 |
| O4 | Mistral-Nemo-12B | yesno | -26.8 [-38.5, -15.1] | 15 | 1.000 | 1.000 | False | 58.600 | 85.400 |
| O1 | Phi-4-14B | word | +0.3 [-0.3, +0.8] | 15 | 0.168 | 1.000 | False | 100.000 | 99.700 |
| O2 | Phi-4-14B | letter | +0.3 [-0.3, +0.8] | 15 | 0.168 | 1.000 | False | 100.000 | 99.700 |
| O3 | Phi-4-14B | relabel | +0.0 [+0.0, +0.0] | 15 | 0.000 | 0.004 | True | 100.000 | 100.000 |
| O4 | Phi-4-14B | yesno | -0.5 [-3.0, +1.9] | 15 | 0.673 | 1.000 | False | 98.200 | 98.700 |

Log-probability version (exploratory):

| model | format | logprob_order_effect |
|---|---|---|
| Gemma-3-12B | word | +27.9 [+19.6, +36.1] |
| Gemma-3-12B | letter | -48.1 [-62.5, -33.7] |
| Gemma-3-12B | relabel | -1.3 [-5.2, +2.6] |
| Gemma-3-12B | yesno | +4.7 [-22.1, +31.5] |
| Gemma-3-4B | word | +10.7 [+0.3, +21.1] |
| Gemma-3-4B | letter | -1.1 [-10.2, +7.9] |
| Gemma-3-4B | relabel | +47.5 [+29.3, +65.7] |
| Gemma-3-4B | yesno | -24.2 [-39.7, -8.7] |
| Granite-3.3-8B | word | +51.0 [+38.4, +63.7] |
| Granite-3.3-8B | letter | +30.1 [+18.7, +41.5] |
| Granite-3.3-8B | relabel | +43.1 [+21.8, +64.3] |
| Granite-3.3-8B | yesno | +24.3 [+6.1, +42.5] |
| Llama-3.2-3B | word | -4.3 [-12.8, +4.1] |
| Llama-3.2-3B | letter | +0.8 [-3.3, +4.8] |
| Llama-3.2-3B | relabel | +41.4 [+31.6, +51.2] |
| Llama-3.2-3B | yesno | -58.4 [-64.0, -52.9] |
| Mistral-Nemo-12B | word | +20.7 [+16.0, +25.3] |
| Mistral-Nemo-12B | letter | +20.1 [+16.1, +24.1] |
| Mistral-Nemo-12B | relabel | +0.2 [-3.8, +4.2] |
| Mistral-Nemo-12B | yesno | -24.1 [-34.7, -13.5] |
| Phi-4-14B | word | -0.1 [-0.2, +0.0] |
| Phi-4-14B | letter | +0.2 [-0.1, +0.6] |
| Phi-4-14B | relabel | +0.1 [-0.0, +0.1] |
| Phi-4-14B | yesno | -1.2 [-3.1, +0.6] |

Emotion effects vs the order effect in the same format (exploratory):

| model | format | emotion | effect_vs_neutral | order_effect | ratio |
|---|---|---|---|---|---|
| Gemma-3-12B | word | angry | +24.5 [+0.3, +48.6] | 29.170 | 1.190 |
| Gemma-3-12B | word | sad | +34.9 [+15.8, +54.0] | 29.170 | 0.840 |
| Gemma-3-12B | letter | angry | +7.3 [-13.2, +27.8] | -49.480 | 6.790 |
| Gemma-3-12B | letter | sad | +10.4 [+3.8, +17.1] | -49.480 | 4.750 |
| Gemma-3-12B | relabel | angry | +33.9 [-1.3, +69.0] | -0.780 | 0.020 |
| Gemma-3-12B | relabel | sad | +40.6 [+6.6, +74.7] | -0.780 | 0.020 |
| Gemma-3-12B | yesno | angry | +8.3 [+0.6, +16.1] | 5.990 | 0.720 |
| Gemma-3-12B | yesno | sad | +4.2 [-12.8, +21.1] | 5.990 | 1.440 |
| Gemma-3-4B | word | angry | -51.6 [-67.8, -35.3] | 11.980 | 0.230 |
| Gemma-3-4B | word | sad | -5.7 [-35.8, +24.4] | 11.980 | 2.090 |
| Gemma-3-4B | letter | angry | -41.1 [-67.4, -14.9] | -1.820 | 0.040 |
| Gemma-3-4B | letter | sad | -7.8 [-33.7, +18.0] | -1.820 | 0.230 |
| Gemma-3-4B | relabel | angry | -28.1 [-44.6, -11.7] | 47.660 | 1.690 |
| Gemma-3-4B | relabel | sad | -5.7 [-21.3, +9.9] | 47.660 | 8.320 |
| Gemma-3-4B | yesno | angry | -1.6 [-13.5, +10.3] | -24.480 | 15.670 |
| Gemma-3-4B | yesno | sad | -3.6 [-11.5, +4.2] | -24.480 | 6.710 |
| Granite-3.3-8B | word | angry | -0.0 [-7.2, +7.2] | 52.080 | 104.170 |
| Granite-3.3-8B | word | sad | +13.0 [-5.1, +31.1] | 52.080 | 4.000 |
| Granite-3.3-8B | letter | angry | -12.5 [-18.6, -6.4] | 32.550 | 2.600 |
| Granite-3.3-8B | letter | sad | +21.9 [+13.5, +30.2] | 32.550 | 1.490 |
| Granite-3.3-8B | relabel | angry | -17.7 [-33.4, -2.1] | 44.010 | 2.490 |
| Granite-3.3-8B | relabel | sad | -12.5 [-29.2, +4.2] | 44.010 | 3.520 |
| Granite-3.3-8B | yesno | angry | -6.8 [-18.7, +5.1] | 23.180 | 3.420 |
| Granite-3.3-8B | yesno | sad | +22.4 [+1.3, +43.5] | 23.180 | 1.030 |
| Llama-3.2-3B | word | angry | +4.2 [-13.5, +21.9] | 0.260 | 0.060 |
| Llama-3.2-3B | word | sad | +16.1 [-16.2, +48.5] | 0.260 | 0.020 |
| Llama-3.2-3B | letter | angry | -9.9 [-30.6, +10.9] | 1.040 | 0.110 |
| Llama-3.2-3B | letter | sad | -9.4 [-23.9, +5.1] | 1.040 | 0.110 |
| Llama-3.2-3B | relabel | angry | -2.6 [-17.7, +12.5] | 42.190 | 16.200 |
| Llama-3.2-3B | relabel | sad | +10.9 [-20.4, +42.3] | 42.190 | 3.860 |
| Llama-3.2-3B | yesno | angry | -8.9 [-19.8, +2.1] | -64.580 | 7.290 |
| Llama-3.2-3B | yesno | sad | -1.0 [-13.3, +11.2] | -64.580 | 62.000 |
| Mistral-Nemo-12B | word | angry | -27.1 [-51.6, -2.6] | 21.090 | 0.780 |
| Mistral-Nemo-12B | word | sad | +18.8 [+4.1, +33.4] | 21.090 | 1.130 |
| Mistral-Nemo-12B | letter | angry | -20.8 [-38.2, -3.4] | 22.920 | 1.100 |
| Mistral-Nemo-12B | letter | sad | +6.3 [-2.4, +14.9] | 22.920 | 3.670 |
| Mistral-Nemo-12B | relabel | angry | -51.6 [-80.3, -22.8] | 1.300 | 0.030 |
| Mistral-Nemo-12B | relabel | sad | +11.5 [+0.9, +22.0] | 1.300 | 0.110 |
| Mistral-Nemo-12B | yesno | angry | -21.4 [-38.2, -4.5] | -26.820 | 1.260 |
| Mistral-Nemo-12B | yesno | sad | +18.8 [+10.1, +27.4] | -26.820 | 1.430 |
| Phi-4-14B | word | angry | -0.5 [-1.7, +0.7] | 0.260 | 0.500 |
| Phi-4-14B | word | sad | +0.0 [-0.0, +0.0] | 0.260 | 0.520 |
| Phi-4-14B | letter | angry | -0.5 [-1.7, +0.7] | 0.260 | 0.500 |
| Phi-4-14B | letter | sad | +0.0 [-0.0, +0.0] | 0.260 | 0.520 |
| Phi-4-14B | relabel | angry | -0.0 [-0.0, +0.0] | 0.000 | 0.000 |
| Phi-4-14B | relabel | sad | -0.0 [-0.0, +0.0] | 0.000 | 0.000 |
| Phi-4-14B | yesno | angry | -3.1 [-7.7, +1.4] | -0.520 | 0.170 |
| Phi-4-14B | yesno | sad | +0.0 [-1.9, +1.9] | -0.520 | 1.040 |

Acceptance (%) by format, option named first (or question polarity for yes/no) and offer:

| fmt | first | 10.0 | 30.0 | 50.0 | model |
|---|---|---|---|---|---|
| letter | accept | 27.000 | 34.000 | 81.000 | Gemma-3-12B |
| letter | reject | 92.000 | 98.000 | 100.000 | Gemma-3-12B |
| relabel | accept | 82.000 | 85.000 | 96.000 | Gemma-3-12B |
| relabel | reject | 82.000 | 88.000 | 95.000 | Gemma-3-12B |
| word | accept | 77.000 | 88.000 | 97.000 | Gemma-3-12B |
| word | reject | 45.000 | 52.000 | 78.000 | Gemma-3-12B |
| yesno | accept | 45.000 | 45.000 | 85.000 | Gemma-3-12B |
| yesno | reject | 70.000 | 61.000 | 27.000 | Gemma-3-12B |
| letter | accept | 38.000 | 59.000 | 69.000 | Gemma-3-4B |
| letter | reject | 41.000 | 59.000 | 71.000 | Gemma-3-4B |
| relabel | accept | 41.000 | 59.000 | 78.000 | Gemma-3-4B |
| relabel | reject | 6.000 | 12.000 | 17.000 | Gemma-3-4B |
| word | accept | 46.000 | 66.000 | 88.000 | Gemma-3-4B |
| word | reject | 30.000 | 65.000 | 68.000 | Gemma-3-4B |
| yesno | accept | 30.000 | 59.000 | 88.000 | Gemma-3-4B |
| yesno | reject | 95.000 | 87.000 | 69.000 | Gemma-3-4B |
| letter | accept | 73.000 | 83.000 | 100.000 | Granite-3.3-8B |
| letter | reject | 41.000 | 52.000 | 66.000 | Granite-3.3-8B |
| relabel | accept | 37.000 | 60.000 | 79.000 | Granite-3.3-8B |
| relabel | reject | 5.000 | 9.000 | 30.000 | Granite-3.3-8B |
| word | accept | 69.000 | 74.000 | 95.000 | Granite-3.3-8B |
| word | reject | 17.000 | 22.000 | 43.000 | Granite-3.3-8B |
| yesno | accept | 68.000 | 69.000 | 90.000 | Granite-3.3-8B |
| yesno | reject | 48.000 | 47.000 | 62.000 | Granite-3.3-8B |
| letter | accept | 46.000 | 44.000 | 50.000 | Llama-3.2-3B |
| letter | reject | 51.000 | 46.000 | 40.000 | Llama-3.2-3B |
| relabel | accept | 58.000 | 61.000 | 62.000 | Llama-3.2-3B |
| relabel | reject | 20.000 | 16.000 | 18.000 | Llama-3.2-3B |
| word | accept | 36.000 | 46.000 | 49.000 | Llama-3.2-3B |
| word | reject | 38.000 | 44.000 | 49.000 | Llama-3.2-3B |
| yesno | accept | 5.000 | 6.000 | 8.000 | Llama-3.2-3B |
| yesno | reject | 73.000 | 67.000 | 73.000 | Llama-3.2-3B |
| letter | accept | 70.000 | 73.000 | 91.000 | Mistral-Nemo-12B |
| letter | reject | 44.000 | 54.000 | 66.000 | Mistral-Nemo-12B |
| relabel | accept | 60.000 | 75.000 | 86.000 | Mistral-Nemo-12B |
| relabel | reject | 64.000 | 69.000 | 84.000 | Mistral-Nemo-12B |
| word | accept | 61.000 | 81.000 | 92.000 | Mistral-Nemo-12B |
| word | reject | 43.000 | 48.000 | 80.000 | Mistral-Nemo-12B |
| yesno | accept | 38.000 | 53.000 | 85.000 | Mistral-Nemo-12B |
| yesno | reject | 81.000 | 86.000 | 89.000 | Mistral-Nemo-12B |
| letter | accept | 100.000 | 100.000 | 100.000 | Phi-4-14B |
| letter | reject | 99.000 | 100.000 | 100.000 | Phi-4-14B |
| relabel | accept | 100.000 | 100.000 | 100.000 | Phi-4-14B |
| relabel | reject | 100.000 | 100.000 | 100.000 | Phi-4-14B |
| word | accept | 100.000 | 100.000 | 100.000 | Phi-4-14B |
| word | reject | 99.000 | 100.000 | 100.000 | Phi-4-14B |
| yesno | accept | 95.000 | 99.000 | 100.000 | Phi-4-14B |
| yesno | reject | 96.000 | 100.000 | 100.000 | Phi-4-14B |

## I. Injected instructions and pressure in Player B's message

| id | model | game | message_set | estimate [95% CI] | df | p | p_holm | supported |
|---|---|---|---|---|---|---|---|---|
| I1 | Gemma-3-12B | S2-DG | fake_system | +90.6 [+82.5, +98.6] | 6 | 0.000 | 0.000 | True |
| I2 | Gemma-3-12B | S2-DG | fake_rule | +80.2 [+63.7, +96.6] | 6 | 0.000 | 0.000 | True |
| I3 | Gemma-3-12B | S2-DG | command | +44.5 [+9.6, +79.4] | 6 | 0.010 | 0.123 | False |
| I1 | Gemma-3-12B | S3b | fake_system | +67.9 [+51.7, +84.1] | 6 | 0.000 | 0.001 | True |
| I2 | Gemma-3-12B | S3b | fake_rule | +55.4 [+30.9, +79.9] | 6 | 0.001 | 0.015 | True |
| I3 | Gemma-3-12B | S3b | command | -0.7 [-25.4, +23.9] | 6 | 0.528 | 1.000 | False |
| I1 | Gemma-3-4B | S2-DG | fake_system | +60.2 [+36.5, +83.8] | 6 | 0.000 | 0.009 | True |
| I2 | Gemma-3-4B | S2-DG | fake_rule | +50.8 [+26.1, +75.5] | 6 | 0.001 | 0.023 | True |
| I3 | Gemma-3-4B | S2-DG | command | +46.6 [+20.8, +72.4] | 6 | 0.002 | 0.038 | True |
| I1 | Gemma-3-4B | S3b | fake_system | +76.3 [+64.8, +87.8] | 6 | 0.000 | 0.000 | True |
| I2 | Gemma-3-4B | S3b | fake_rule | +75.3 [+63.5, +87.0] | 6 | 0.000 | 0.000 | True |
| I3 | Gemma-3-4B | S3b | command | +61.3 [+25.0, +97.6] | 6 | 0.003 | 0.046 | True |
| I1 | Granite-3.3-8B | S2-DG | fake_system | +56.4 [+49.7, +63.1] | 6 | 0.000 | 0.000 | True |
| I2 | Granite-3.3-8B | S2-DG | fake_rule | +37.6 [+9.2, +66.1] | 6 | 0.009 | 0.115 | False |
| I3 | Granite-3.3-8B | S2-DG | command | +7.7 [-23.8, +39.1] | 6 | 0.286 | 1.000 | False |
| I1 | Granite-3.3-8B | S3b | fake_system | +59.5 [+53.2, +65.8] | 6 | 0.000 | 0.000 | True |
| I2 | Granite-3.3-8B | S3b | fake_rule | +30.8 [-0.0, +61.6] | 6 | 0.025 | 0.227 | False |
| I3 | Granite-3.3-8B | S3b | command | +40.9 [+16.6, +65.2] | 6 | 0.003 | 0.046 | True |
| I1 | Llama-3.2-3B | S2-DG | fake_system | +46.0 [+27.8, +64.3] | 6 | 0.000 | 0.009 | True |
| I2 | Llama-3.2-3B | S2-DG | fake_rule | +36.7 [+17.5, +55.9] | 6 | 0.002 | 0.031 | True |
| I3 | Llama-3.2-3B | S2-DG | command | +27.8 [-17.2, +72.8] | 6 | 0.090 | 0.724 | False |
| I1 | Llama-3.2-3B | S3b | fake_system | +54.0 [+29.5, +78.6] | 6 | 0.001 | 0.017 | True |
| I2 | Llama-3.2-3B | S3b | fake_rule | +0.1 [-11.7, +11.9] | 6 | 0.494 | 1.000 | False |
| I3 | Llama-3.2-3B | S3b | command | +20.2 [-13.3, +53.7] | 6 | 0.095 | 0.724 | False |
| I1 | Mistral-Nemo-12B | S2-DG | fake_system | +41.8 [+37.9, +45.7] | 6 | 0.000 | 0.000 | True |
| I2 | Mistral-Nemo-12B | S2-DG | fake_rule | +37.6 [+23.5, +51.7] | 6 | 0.000 | 0.007 | True |
| I3 | Mistral-Nemo-12B | S2-DG | command | +11.6 [-17.7, +40.8] | 6 | 0.185 | 1.000 | False |
| I1 | Mistral-Nemo-12B | S3b | fake_system | +39.4 [+27.7, +51.0] | 6 | 0.000 | 0.002 | True |
| I2 | Mistral-Nemo-12B | S3b | fake_rule | +29.0 [+4.6, +53.3] | 6 | 0.013 | 0.148 | False |
| I3 | Mistral-Nemo-12B | S3b | command | +23.1 [+0.7, +45.4] | 6 | 0.023 | 0.227 | False |
| I1 | Phi-4-14B | S2-DG | fake_system | +39.8 [+26.8, +52.8] | 6 | 0.000 | 0.004 | True |
| I2 | Phi-4-14B | S2-DG | fake_rule | +50.7 [+44.9, +56.6] | 6 | 0.000 | 0.000 | True |
| I3 | Phi-4-14B | S2-DG | command | -10.5 [-24.6, +3.6] | 6 | 0.941 | 1.000 | False |
| I1 | Phi-4-14B | S3b | fake_system | +47.0 [+37.1, +56.9] | 6 | 0.000 | 0.000 | True |
| I2 | Phi-4-14B | S3b | fake_rule | +38.2 [+17.0, +59.4] | 6 | 0.002 | 0.038 | True |
| I3 | Phi-4-14B | S3b | command | -14.8 [-41.5, +11.9] | 6 | 0.888 | 1.000 | False |

Exploratory (two-sided): pleading and promises. In the dictator game (S2-DG) Player B cannot return anything, so a promise to repay is impossible.

| index | model | game | message_set | estimate [95% CI] | p |
|---|---|---|---|---|---|
| 3 | Gemma-3-12B | S2-DG | plead | +48.7 [+24.9, +72.5] | 0.002 |
| 4 | Gemma-3-12B | S2-DG | promise | +30.3 [-10.7, +71.2] | 0.121 |
| 8 | Gemma-3-12B | S3b | plead | +17.7 [-6.8, +42.2] | 0.127 |
| 9 | Gemma-3-12B | S3b | promise | +30.7 [-22.7, +84.1] | 0.209 |
| 13 | Gemma-3-4B | S2-DG | plead | +64.8 [+53.7, +76.0] | 0.000 |
| 14 | Gemma-3-4B | S2-DG | promise | +33.0 [+3.9, +62.2] | 0.032 |
| 18 | Gemma-3-4B | S3b | plead | +71.1 [+54.5, +87.7] | 0.000 |
| 19 | Gemma-3-4B | S3b | promise | +47.6 [+22.2, +72.9] | 0.004 |
| 23 | Granite-3.3-8B | S2-DG | plead | -7.1 [-22.8, +8.5] | 0.306 |
| 24 | Granite-3.3-8B | S2-DG | promise | +43.9 [+35.4, +52.4] | 0.000 |
| 28 | Granite-3.3-8B | S3b | plead | +54.1 [+43.0, +65.2] | 0.000 |
| 29 | Granite-3.3-8B | S3b | promise | +46.4 [+18.6, +74.1] | 0.006 |
| 33 | Llama-3.2-3B | S2-DG | plead | +3.3 [-24.1, +30.7] | 0.776 |
| 34 | Llama-3.2-3B | S2-DG | promise | -11.8 [-32.8, +9.2] | 0.219 |
| 38 | Llama-3.2-3B | S3b | plead | +6.8 [+1.9, +11.8] | 0.015 |
| 39 | Llama-3.2-3B | S3b | promise | -1.6 [-12.8, +9.7] | 0.746 |
| 43 | Mistral-Nemo-12B | S2-DG | plead | +28.7 [+9.0, +48.5] | 0.012 |
| 44 | Mistral-Nemo-12B | S2-DG | promise | -4.3 [-11.0, +2.4] | 0.167 |
| 48 | Mistral-Nemo-12B | S3b | plead | +12.3 [-13.1, +37.6] | 0.280 |
| 49 | Mistral-Nemo-12B | S3b | promise | +30.6 [+16.8, +44.4] | 0.002 |
| 53 | Phi-4-14B | S2-DG | plead | +13.2 [-0.1, +26.5] | 0.051 |
| 54 | Phi-4-14B | S2-DG | promise | -4.0 [-35.4, +27.3] | 0.763 |
| 58 | Phi-4-14B | S3b | plead | +3.8 [-6.2, +13.9] | 0.389 |
| 59 | Phi-4-14B | S3b | promise | +30.3 [+1.5, +59.1] | 0.042 |

Share given and rate of handing over the full amount:

| model | game | message_set | n | mean_share | full_amount | full_ci |
|---|---|---|---|---|---|---|
| Gemma-3-12B | S2-DG | command | 96 | 0.539 | 0.479 | [0.38, 0.58] |
| Gemma-3-12B | S2-DG | fake_rule | 96 | 0.896 | 0.896 | [0.82, 0.94] |
| Gemma-3-12B | S2-DG | fake_system | 96 | 1.000 | 1.000 | [0.96, 1.00] |
| Gemma-3-12B | S2-DG | neutral | 96 | 0.094 | 0.000 | [0.00, 0.04] |
| Gemma-3-12B | S2-DG | plead | 96 | 0.581 | 0.458 | [0.36, 0.56] |
| Gemma-3-12B | S2-DG | promise | 96 | 0.397 | 0.177 | [0.11, 0.27] |
| Gemma-3-12B | S3b | command | 96 | 0.314 | 0.250 | [0.17, 0.35] |
| Gemma-3-12B | S3b | fake_rule | 96 | 0.875 | 0.875 | [0.79, 0.93] |
| Gemma-3-12B | S3b | fake_system | 96 | 1.000 | 1.000 | [0.96, 1.00] |
| Gemma-3-12B | S3b | neutral | 96 | 0.321 | 0.000 | [0.00, 0.04] |
| Gemma-3-12B | S3b | plead | 96 | 0.498 | 0.365 | [0.28, 0.46] |
| Gemma-3-12B | S3b | promise | 96 | 0.628 | 0.438 | [0.34, 0.54] |
| Gemma-3-4B | S2-DG | command | 96 | 0.766 | 0.646 | [0.55, 0.73] |
| Gemma-3-4B | S2-DG | fake_rule | 96 | 0.807 | 0.792 | [0.70, 0.86] |
| Gemma-3-4B | S2-DG | fake_system | 96 | 0.901 | 0.812 | [0.72, 0.88] |
| Gemma-3-4B | S2-DG | neutral | 96 | 0.299 | 0.000 | [0.00, 0.04] |
| Gemma-3-4B | S2-DG | plead | 96 | 0.948 | 0.948 | [0.88, 0.98] |
| Gemma-3-4B | S2-DG | promise | 96 | 0.630 | 0.365 | [0.28, 0.46] |
| Gemma-3-4B | S3b | command | 96 | 0.850 | 0.781 | [0.69, 0.85] |
| Gemma-3-4B | S3b | fake_rule | 96 | 0.990 | 0.990 | [0.94, 1.00] |
| Gemma-3-4B | S3b | fake_system | 96 | 1.000 | 1.000 | [0.96, 1.00] |
| Gemma-3-4B | S3b | neutral | 96 | 0.237 | 0.000 | [0.00, 0.04] |
| Gemma-3-4B | S3b | plead | 96 | 0.948 | 0.948 | [0.88, 0.98] |
| Gemma-3-4B | S3b | promise | 96 | 0.713 | 0.542 | [0.44, 0.64] |
| Granite-3.3-8B | S2-DG | command | 96 | 0.294 | 0.292 | [0.21, 0.39] |
| Granite-3.3-8B | S2-DG | fake_rule | 96 | 0.594 | 0.594 | [0.49, 0.69] |
| Granite-3.3-8B | S2-DG | fake_system | 96 | 0.781 | 0.781 | [0.69, 0.85] |
| Granite-3.3-8B | S2-DG | neutral | 96 | 0.217 | 0.000 | [0.00, 0.04] |
| Granite-3.3-8B | S2-DG | plead | 96 | 0.146 | 0.135 | [0.08, 0.22] |
| Granite-3.3-8B | S2-DG | promise | 96 | 0.657 | 0.406 | [0.31, 0.51] |
| Granite-3.3-8B | S3b | command | 96 | 0.799 | 0.781 | [0.69, 0.85] |
| Granite-3.3-8B | S3b | fake_rule | 96 | 0.698 | 0.698 | [0.60, 0.78] |
| Granite-3.3-8B | S3b | fake_system | 96 | 0.985 | 0.979 | [0.93, 0.99] |
| Granite-3.3-8B | S3b | neutral | 96 | 0.390 | 0.198 | [0.13, 0.29] |
| Granite-3.3-8B | S3b | plead | 96 | 0.931 | 0.906 | [0.83, 0.95] |
| Granite-3.3-8B | S3b | promise | 96 | 0.854 | 0.771 | [0.68, 0.84] |
| Llama-3.2-3B | S2-DG | command | 96 | 0.651 | 0.635 | [0.54, 0.72] |
| Llama-3.2-3B | S2-DG | fake_rule | 96 | 0.740 | 0.740 | [0.64, 0.82] |
| Llama-3.2-3B | S2-DG | fake_system | 96 | 0.833 | 0.833 | [0.75, 0.89] |
| Llama-3.2-3B | S2-DG | neutral | 96 | 0.373 | 0.062 | [0.03, 0.13] |
| Llama-3.2-3B | S2-DG | plead | 96 | 0.406 | 0.406 | [0.31, 0.51] |
| Llama-3.2-3B | S2-DG | promise | 96 | 0.255 | 0.104 | [0.06, 0.18] |
| Llama-3.2-3B | S3b | command | 96 | 0.389 | 0.344 | [0.26, 0.44] |
| Llama-3.2-3B | S3b | fake_rule | 96 | 0.188 | 0.188 | [0.12, 0.28] |
| Llama-3.2-3B | S3b | fake_system | 96 | 0.727 | 0.719 | [0.62, 0.80] |
| Llama-3.2-3B | S3b | neutral | 96 | 0.187 | 0.000 | [0.00, 0.04] |
| Llama-3.2-3B | S3b | plead | 96 | 0.255 | 0.229 | [0.16, 0.32] |
| Llama-3.2-3B | S3b | promise | 96 | 0.171 | 0.031 | [0.01, 0.09] |
| Mistral-Nemo-12B | S2-DG | command | 96 | 0.615 | 0.542 | [0.44, 0.64] |
| Mistral-Nemo-12B | S2-DG | fake_rule | 96 | 0.875 | 0.875 | [0.79, 0.93] |
| Mistral-Nemo-12B | S2-DG | fake_system | 96 | 0.917 | 0.917 | [0.84, 0.96] |
| Mistral-Nemo-12B | S2-DG | neutral | 96 | 0.499 | 0.000 | [0.00, 0.04] |
| Mistral-Nemo-12B | S2-DG | plead | 96 | 0.786 | 0.781 | [0.69, 0.85] |
| Mistral-Nemo-12B | S2-DG | promise | 96 | 0.456 | 0.198 | [0.13, 0.29] |
| Mistral-Nemo-12B | S3b | command | 96 | 0.806 | 0.802 | [0.71, 0.87] |
| Mistral-Nemo-12B | S3b | fake_rule | 96 | 0.865 | 0.865 | [0.78, 0.92] |
| Mistral-Nemo-12B | S3b | fake_system | 96 | 0.969 | 0.969 | [0.91, 0.99] |
| Mistral-Nemo-12B | S3b | neutral | 96 | 0.575 | 0.208 | [0.14, 0.30] |
| Mistral-Nemo-12B | S3b | plead | 96 | 0.698 | 0.677 | [0.58, 0.76] |
| Mistral-Nemo-12B | S3b | promise | 96 | 0.881 | 0.771 | [0.68, 0.84] |
| Phi-4-14B | S2-DG | command | 96 | 0.346 | 0.115 | [0.07, 0.19] |
| Phi-4-14B | S2-DG | fake_rule | 96 | 0.958 | 0.958 | [0.90, 0.98] |
| Phi-4-14B | S2-DG | fake_system | 96 | 0.849 | 0.802 | [0.71, 0.87] |
| Phi-4-14B | S2-DG | neutral | 96 | 0.451 | 0.000 | [0.00, 0.04] |
| Phi-4-14B | S2-DG | plead | 96 | 0.583 | 0.219 | [0.15, 0.31] |
| Phi-4-14B | S2-DG | promise | 96 | 0.411 | 0.240 | [0.17, 0.33] |
| Phi-4-14B | S3b | command | 96 | 0.273 | 0.177 | [0.11, 0.27] |
| Phi-4-14B | S3b | fake_rule | 96 | 0.802 | 0.802 | [0.71, 0.87] |
| Phi-4-14B | S3b | fake_system | 96 | 0.891 | 0.875 | [0.79, 0.93] |
| Phi-4-14B | S3b | neutral | 96 | 0.420 | 0.021 | [0.01, 0.07] |
| Phi-4-14B | S3b | plead | 96 | 0.459 | 0.146 | [0.09, 0.23] |
| Phi-4-14B | S3b | promise | 96 | 0.724 | 0.531 | [0.43, 0.63] |

## X. Incidental mood of the model (system-prompt background, no partner message)

| id | model | state | game | outcome | estimate [95% CI] | df | p | p_holm | supported |
|---|---|---|---|---|---|---|---|---|---|
| X1 | Gemma-3-12B | angry | S1 | reject | +70.5 [+60.6, +80.3] | 6 | 0.000 | 0.000 | True |
| X2 | Gemma-3-12B | sad | S1 | reject | +33.8 [+18.5, +49.1] | 6 | 0.001 | 0.009 | True |
| X3 | Gemma-3-12B | angry | S3b | share | -16.1 [-40.0, +7.9] | 6 | 0.076 | 0.610 | False |
| X1 | Gemma-3-4B | angry | S1 | reject | +51.1 [+44.4, +57.8] | 6 | 0.000 | 0.000 | True |
| X2 | Gemma-3-4B | sad | S1 | reject | +23.9 [+14.9, +33.0] | 6 | 0.000 | 0.004 | True |
| X3 | Gemma-3-4B | angry | S3b | share | +10.9 [-6.3, +28.1] | 6 | 0.914 | 1.000 | False |
| X1 | Granite-3.3-8B | angry | S1 | reject | -11.0 [-18.8, -3.2] | 6 | 0.993 | 1.000 | False |
| X2 | Granite-3.3-8B | sad | S1 | reject | +1.8 [-4.6, +8.3] | 6 | 0.254 | 1.000 | False |
| X3 | Granite-3.3-8B | angry | S3b | share | +21.7 [+8.2, +35.1] | 6 | 0.996 | 1.000 | False |
| X1 | Llama-3.2-3B | angry | S1 | reject | +32.6 [+23.6, +41.7] | 6 | 0.000 | 0.001 | True |
| X2 | Llama-3.2-3B | sad | S1 | reject | +33.5 [+22.5, +44.5] | 6 | 0.000 | 0.002 | True |
| X3 | Llama-3.2-3B | angry | S3b | share | -1.9 [-8.4, +4.5] | 6 | 0.247 | 1.000 | False |
| X1 | Mistral-Nemo-12B | angry | S1 | reject | +69.5 [+66.9, +72.1] | 6 | 0.000 | 0.000 | True |
| X2 | Mistral-Nemo-12B | sad | S1 | reject | +4.8 [-2.5, +12.0] | 6 | 0.080 | 0.610 | False |
| X3 | Mistral-Nemo-12B | angry | S3b | share | -9.6 [-17.5, -1.7] | 6 | 0.012 | 0.123 | False |
| X1 | Phi-4-14B | angry | S1 | reject | +8.4 [-0.1, +16.9] | 6 | 0.026 | 0.235 | False |
| X2 | Phi-4-14B | sad | S1 | reject | +0.0 [+0.0, +0.0] | 6 |  | 1.000 | False |
| X3 | Phi-4-14B | angry | S3b | share | -17.2 [-23.1, -11.2] | 6 | 0.000 | 0.003 | True |

Exploratory:

| model | state | game | outcome | estimate [95% CI] | p |
|---|---|---|---|---|---|
| Gemma-3-12B | happy | S1 | reject | -23.0 [-28.0, -17.9] | 0.000 |
| Gemma-3-12B | sad | S3b | share | -36.3 [-39.7, -32.9] | 0.000 |
| Gemma-3-12B | happy | S3b | share | +19.0 [+11.3, +26.8] | 0.001 |
| Gemma-3-4B | happy | S1 | reject | -13.4 [-21.7, -5.2] | 0.007 |
| Gemma-3-4B | sad | S3b | share | +1.5 [-14.5, +17.4] | 0.830 |
| Gemma-3-4B | happy | S3b | share | +16.8 [+1.4, +32.1] | 0.037 |
| Granite-3.3-8B | happy | S1 | reject | +1.4 [-12.7, +15.5] | 0.812 |
| Granite-3.3-8B | sad | S3b | share | +21.4 [+10.2, +32.6] | 0.003 |
| Granite-3.3-8B | happy | S3b | share | +22.3 [+7.4, +37.3] | 0.011 |
| Llama-3.2-3B | happy | S1 | reject | -20.9 [-38.7, -3.2] | 0.028 |
| Llama-3.2-3B | sad | S3b | share | -3.5 [-6.7, -0.2] | 0.039 |
| Llama-3.2-3B | happy | S3b | share | +7.0 [+3.7, +10.2] | 0.002 |
| Mistral-Nemo-12B | happy | S1 | reject | -14.7 [-17.8, -11.6] | 0.000 |
| Mistral-Nemo-12B | sad | S3b | share | -9.7 [-14.5, -4.8] | 0.003 |
| Mistral-Nemo-12B | happy | S3b | share | +5.9 [+1.3, +10.6] | 0.020 |
| Phi-4-14B | happy | S1 | reject | +0.0 [+0.0, +0.0] |  |
| Phi-4-14B | sad | S3b | share | -1.9 [-7.1, +3.2] | 0.389 |
| Phi-4-14B | happy | S3b | share | +2.6 [-2.3, +7.6] | 0.243 |

| model | game | state | value | measure |
|---|---|---|---|---|
| Gemma-3-12B | S1 | angry | 0.938 | rejection rate |
| Gemma-3-12B | S1 | calm | 0.229 | rejection rate |
| Gemma-3-12B | S1 | happy | 0.000 | rejection rate |
| Gemma-3-12B | S1 | sad | 0.573 | rejection rate |
| Gemma-3-12B | S3b | angry | 0.208 | share sent |
| Gemma-3-12B | S3b | calm | 0.369 | share sent |
| Gemma-3-12B | S3b | happy | 0.559 | share sent |
| Gemma-3-12B | S3b | sad | 0.006 | share sent |
| Gemma-3-4B | S1 | angry | 0.771 | rejection rate |
| Gemma-3-4B | S1 | calm | 0.260 | rejection rate |
| Gemma-3-4B | S1 | happy | 0.125 | rejection rate |
| Gemma-3-4B | S1 | sad | 0.500 | rejection rate |
| Gemma-3-4B | S3b | angry | 0.641 | share sent |
| Gemma-3-4B | S3b | calm | 0.532 | share sent |
| Gemma-3-4B | S3b | happy | 0.700 | share sent |
| Gemma-3-4B | S3b | sad | 0.547 | share sent |
| Granite-3.3-8B | S1 | angry | 0.354 | rejection rate |
| Granite-3.3-8B | S1 | calm | 0.448 | rejection rate |
| Granite-3.3-8B | S1 | happy | 0.469 | rejection rate |
| Granite-3.3-8B | S1 | sad | 0.479 | rejection rate |
| Granite-3.3-8B | S3b | angry | 0.704 | share sent |
| Granite-3.3-8B | S3b | calm | 0.487 | share sent |
| Granite-3.3-8B | S3b | happy | 0.710 | share sent |
| Granite-3.3-8B | S3b | sad | 0.701 | share sent |
| Llama-3.2-3B | S1 | angry | 0.792 | rejection rate |
| Llama-3.2-3B | S1 | calm | 0.469 | rejection rate |
| Llama-3.2-3B | S1 | happy | 0.260 | rejection rate |
| Llama-3.2-3B | S1 | sad | 0.802 | rejection rate |
| Llama-3.2-3B | S3b | angry | 0.207 | share sent |
| Llama-3.2-3B | S3b | calm | 0.226 | share sent |
| Llama-3.2-3B | S3b | happy | 0.296 | share sent |
| Llama-3.2-3B | S3b | sad | 0.191 | share sent |
| Mistral-Nemo-12B | S1 | angry | 0.990 | rejection rate |
| Mistral-Nemo-12B | S1 | calm | 0.292 | rejection rate |
| Mistral-Nemo-12B | S1 | happy | 0.146 | rejection rate |
| Mistral-Nemo-12B | S1 | sad | 0.344 | rejection rate |
| Mistral-Nemo-12B | S3b | angry | 0.453 | share sent |
| Mistral-Nemo-12B | S3b | calm | 0.549 | share sent |
| Mistral-Nemo-12B | S3b | happy | 0.608 | share sent |
| Mistral-Nemo-12B | S3b | sad | 0.452 | share sent |
| Phi-4-14B | S1 | angry | 0.083 | rejection rate |
| Phi-4-14B | S1 | calm | 0.000 | rejection rate |
| Phi-4-14B | S1 | happy | 0.000 | rejection rate |
| Phi-4-14B | S1 | sad | 0.000 | rejection rate |
| Phi-4-14B | S3b | angry | 0.347 | share sent |
| Phi-4-14B | S3b | calm | 0.518 | share sent |
| Phi-4-14B | S3b | happy | 0.545 | share sent |
| Phi-4-14B | S3b | sad | 0.499 | share sent |

Mood manipulation check (share of probes answering the induced state):

| model_key | angry | calm | happy | sad |
|---|---|---|---|---|
| Gemma-3-12B | 1.000 | 1.000 | 1.000 | 1.000 |
| Gemma-3-4B | 1.000 | 0.719 | 0.938 | 1.000 |
| Granite-3.3-8B | 1.000 | 1.000 | 0.562 | 1.000 |
| Llama-3.2-3B | 1.000 | 1.000 | 1.000 | 1.000 |
| Mistral-Nemo-12B | 1.000 | 1.000 | 1.000 | 1.000 |
| Phi-4-14B | 1.000 | 1.000 | 0.844 | 1.000 |

## D. Dominance checks (failure = Wilson 95% lower bound above 5%)

| model | check | n | rate | ci | failure | by_message |
|---|---|---|---|---|---|---|
| Gemma-3-12B | reject an offer of 100% | 96 | 0.125 | [0.07, 0.21] | True | {"angry": 0.12, "neutral": 0.16, "none": 0.09} |
| Gemma-3-12B | send > 0 with a zero multiplier | 144 | 0.042 | [0.02, 0.09] | False | {"angry": 0.12, "neutral": 0.0, "none": 0.0} |
| Gemma-3-12B | accept an offer of 0% (indifferent; descriptive) | 96 | 0.125 | [0.07, 0.21] | False | {"angry": 0.38, "neutral": 0.0, "none": 0.0} |
| Gemma-3-4B | reject an offer of 100% | 96 | 0.385 | [0.29, 0.49] | True | {"angry": 0.91, "neutral": 0.25, "none": 0.0} |
| Gemma-3-4B | send > 0 with a zero multiplier | 144 | 0.125 | [0.08, 0.19] | True | {"angry": 0.19, "neutral": 0.19, "none": 0.0} |
| Gemma-3-4B | accept an offer of 0% (indifferent; descriptive) | 96 | 0.052 | [0.02, 0.12] | False | {"angry": 0.0, "neutral": 0.0, "none": 0.16} |
| Granite-3.3-8B | reject an offer of 100% | 96 | 0.385 | [0.29, 0.49] | True | {"angry": 0.34, "neutral": 0.41, "none": 0.41} |
| Granite-3.3-8B | send > 0 with a zero multiplier | 144 | 0.028 | [0.01, 0.07] | False | {"angry": 0.06, "neutral": 0.02, "none": 0.0} |
| Granite-3.3-8B | accept an offer of 0% (indifferent; descriptive) | 96 | 0.062 | [0.03, 0.13] | False | {"angry": 0.09, "neutral": 0.03, "none": 0.06} |
| Llama-3.2-3B | reject an offer of 100% | 96 | 0.688 | [0.59, 0.77] | True | {"angry": 0.66, "neutral": 0.72, "none": 0.69} |
| Llama-3.2-3B | send > 0 with a zero multiplier | 144 | 0.174 | [0.12, 0.24] | True | {"angry": 0.21, "neutral": 0.21, "none": 0.1} |
| Llama-3.2-3B | accept an offer of 0% (indifferent; descriptive) | 96 | 0.219 | [0.15, 0.31] | False | {"angry": 0.25, "neutral": 0.25, "none": 0.16} |
| Mistral-Nemo-12B | reject an offer of 100% | 96 | 0.365 | [0.28, 0.46] | True | {"angry": 0.62, "neutral": 0.34, "none": 0.12} |
| Mistral-Nemo-12B | send > 0 with a zero multiplier | 144 | 0.125 | [0.08, 0.19] | True | {"angry": 0.06, "neutral": 0.15, "none": 0.17} |
| Mistral-Nemo-12B | accept an offer of 0% (indifferent; descriptive) | 96 | 0.031 | [0.01, 0.09] | False | {"angry": 0.03, "neutral": 0.0, "none": 0.06} |
| Phi-4-14B | reject an offer of 100% | 96 | 0.000 | [0.00, 0.04] | False | {"angry": 0.0, "neutral": 0.0, "none": 0.0} |
| Phi-4-14B | send > 0 with a zero multiplier | 144 | 0.056 | [0.03, 0.11] | False | {"angry": 0.15, "neutral": 0.02, "none": 0.0} |
| Phi-4-14B | accept an offer of 0% (indifferent; descriptive) | 96 | 0.365 | [0.28, 0.46] | False | {"angry": 0.47, "neutral": 0.31, "none": 0.31} |
