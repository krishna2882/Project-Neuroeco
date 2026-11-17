# Extension 7: generalisation to new model families, and what kind of effect the mood is

Design and hypotheses: `docs/preregistration_extension7.md`. Estimates in percentage points. Pooled tests: one estimate per model, one-sample t test over models (one-sided), Holm within each family.

## G. The extension-4 and extension-5 findings in models from new developers

| id | test | k | mean [95% CI] | same_sign | p | p_holm | supported |
|---|---|---|---|---|---|---|---|
| G1 | fake SYSTEM notice raises the share handed over (vs neutral message) | 6 | +56.6 [+40.8, +72.3] | 6/6 | 0.000 | 0.001 | True |
| G2 | a 100% offer is rejected more than 5% of the time | 6 | +32.5 [+7.4, +57.6] | 5/6 | 0.019 | 0.081 | False |
| G3 | incidental anger raises rejection of unfair offers (no regulation) | 6 | +34.2 [+6.1, +62.4] | 5/6 | 0.013 | 0.079 | False |
| G4 | reappraisal shrinks the anger effect (vs filler) | 6 | -22.2 [-48.4, +4.0] | 6/6 | 0.041 | 0.101 | False |
| G5 | suppression shrinks the anger effect (vs filler) | 6 | -28.7 [-60.4, +3.0] | 6/6 | 0.034 | 0.101 | False |
| G6 | the reminder defence lowers the share handed over after injection | 6 | -2.3 [-5.3, +0.6] | 5/6 | 0.050 | 0.101 | False |
| G7 | anger raises MAO* (share of the pie) | 6 | +15.4 [+3.2, +27.6] | 5/6 | 0.011 | 0.079 | False |
| G8 | anger lowers acceptance of offers above 50% | 6 | -44.5 [-83.6, -5.5] | 5/6 | 0.016 | 0.081 | False |

Per-model estimates (pp):

| model | G1 | G2 | G3 | G4 | G5 | G6 | G7 | G8 |
|---|---|---|---|---|---|---|---|---|
| Gemma-3-12B | 79.200 | 12.500 | 60.200 | -59.400 | -61.700 | -5.500 | 27.500 | -81.600 |
| Gemma-3-4B | 68.200 | 38.500 | 45.300 | -7.000 | -12.500 | 2.000 | 22.600 | -72.800 |
| Granite-3.3-8B | 58.000 | 38.500 | -5.500 | -1.600 | -1.200 | -5.500 | -1.000 | -3.100 |
| Llama-3.2-3B | 50.000 | 68.800 | 37.500 | -13.300 | -21.900 | -2.000 | 14.300 | -34.400 |
| Mistral-Nemo-12B | 40.600 | 36.500 | 58.600 | -48.000 | -71.100 | -2.100 | 24.600 | -75.300 |
| Phi-4-14B | 43.400 | 0.000 | 9.400 | -3.900 | -3.900 | -1.000 | 4.500 | 0.000 |

Descriptive, per model:

| model_key | full_handover_fake_system | send_destroyed_money | largest_format_effect | largest_format | format_p | injection_sets_still_breaking_under_defence | model |
|---|---|---|---|---|---|---|---|
| gemma3_12b | 100.000 | 4.167 | -49.479 | letter | 0.000 | 91.667 | Gemma-3-12B |
| gemma3_4b | 90.625 | 12.500 | 47.656 | relabel | 0.000 | 100.000 | Gemma-3-4B |
| granite33_8b | 88.021 | 2.778 | 52.083 | word | 0.000 | 100.000 | Granite-3.3-8B |
| llama32_3b | 77.604 | 17.361 | -64.583 | yesno | 0.000 | 100.000 | Llama-3.2-3B |
| mistral_nemo_12b | 94.271 | 12.500 | -26.823 | yesno | 0.000 | 100.000 | Mistral-Nemo-12B |
| phi4_14b | 83.854 | 5.556 | -0.521 | yesno | 0.654 | 66.667 | Phi-4-14B |

## N. What kind of effect is the angry mood? (ultimatum responder, offers of 10% and 30%)

Across models:

| id | test | k | mean [95% CI] | same_sign | p | p_holm | supported |
|---|---|---|---|---|---|---|---|
| N1 | event only - calm (the feeling is inferred) | 9 | +24.7 [+11.8, +37.7] | 7/9 | 0.001 | 0.004 | True |
| N2 | label only - calm (the feeling without a cause) | 9 | +32.0 [+15.5, +48.5] | 8/9 | 0.001 | 0.004 | True |
| N3 | own anger - another person's anger | 9 | +14.4 [+4.2, +24.6] | 7/9 | 0.006 | 0.006 | True |
| N4 | furious - slightly annoyed (same event) | 9 | +15.6 [+7.0, +24.3] | 9/9 | 0.002 | 0.004 | True |

Per model (Holm across all models and tests):

| id | model | test | estimate [95% CI] | df | p | p_holm | supported |
|---|---|---|---|---|---|---|---|
| N1 | Gemma-3-12B | event only - calm (the feeling is inferred) | +35.2 [+24.5, +45.8] | 14 | 0.000 | 0.000 | True |
| N2 | Gemma-3-12B | label only - calm (the feeling without a cause) | +56.6 [+49.7, +63.5] | 14 | 0.000 | 0.000 | True |
| N3 | Gemma-3-12B | own anger - another person's anger | +34.4 [+23.7, +45.1] | 7 | 0.000 | 0.001 | True |
| N4 | Gemma-3-12B | furious - slightly annoyed (same event) | +39.8 [+35.2, +44.4] | 7 | 0.000 | 0.000 | True |
| N1 | Gemma-3-4B | event only - calm (the feeling is inferred) | +31.3 [+25.3, +37.2] | 14 | 0.000 | 0.000 | True |
| N2 | Gemma-3-4B | label only - calm (the feeling without a cause) | +38.3 [+31.3, +45.2] | 14 | 0.000 | 0.000 | True |
| N3 | Gemma-3-4B | own anger - another person's anger | +24.6 [+18.1, +31.1] | 7 | 0.000 | 0.000 | True |
| N4 | Gemma-3-4B | furious - slightly annoyed (same event) | +10.9 [+6.7, +15.2] | 7 | 0.000 | 0.004 | True |
| N1 | Granite-3.3-8B | event only - calm (the feeling is inferred) | -5.1 [-10.1, -0.1] | 14 | 0.977 | 1.000 | False |
| N2 | Granite-3.3-8B | label only - calm (the feeling without a cause) | -9.0 [-14.8, -3.2] | 14 | 0.997 | 1.000 | False |
| N3 | Granite-3.3-8B | own anger - another person's anger | -8.2 [-16.3, -0.1] | 7 | 0.976 | 1.000 | False |
| N4 | Granite-3.3-8B | furious - slightly annoyed (same event) | +0.0 [-7.2, +7.2] | 7 | 0.500 | 1.000 | False |
| N1 | Llama-3.1-8B | event only - calm (the feeling is inferred) | +30.1 [+23.0, +37.2] | 14 | 0.000 | 0.000 | True |
| N2 | Llama-3.1-8B | label only - calm (the feeling without a cause) | +32.4 [+23.6, +41.3] | 14 | 0.000 | 0.000 | True |
| N3 | Llama-3.1-8B | own anger - another person's anger | +16.0 [+9.7, +22.4] | 7 | 0.000 | 0.004 | True |
| N4 | Llama-3.1-8B | furious - slightly annoyed (same event) | +12.5 [+6.1, +18.9] | 7 | 0.001 | 0.016 | True |
| N1 | Llama-3.2-3B | event only - calm (the feeling is inferred) | +34.0 [+25.7, +42.3] | 14 | 0.000 | 0.000 | True |
| N2 | Llama-3.2-3B | label only - calm (the feeling without a cause) | +38.3 [+33.1, +43.5] | 14 | 0.000 | 0.000 | True |
| N3 | Llama-3.2-3B | own anger - another person's anger | -0.4 [-8.6, +7.9] | 7 | 0.543 | 1.000 | False |
| N4 | Llama-3.2-3B | furious - slightly annoyed (same event) | +10.2 [+2.9, +17.4] | 7 | 0.007 | 0.059 | False |
| N1 | Mistral-Nemo-12B | event only - calm (the feeling is inferred) | +46.1 [+37.5, +54.7] | 14 | 0.000 | 0.000 | True |
| N2 | Mistral-Nemo-12B | label only - calm (the feeling without a cause) | +58.2 [+53.1, +63.3] | 14 | 0.000 | 0.000 | True |
| N3 | Mistral-Nemo-12B | own anger - another person's anger | +25.8 [+22.7, +28.8] | 7 | 0.000 | 0.000 | True |
| N4 | Mistral-Nemo-12B | furious - slightly annoyed (same event) | +18.7 [+13.0, +24.5] | 7 | 0.000 | 0.001 | True |
| N1 | Phi-4-14B | event only - calm (the feeling is inferred) | +0.0 [+0.0, +0.0] | 14 |  | 1.000 | False |
| N2 | Phi-4-14B | label only - calm (the feeling without a cause) | +8.2 [+2.6, +13.8] | 14 | 0.004 | 0.041 | True |
| N3 | Phi-4-14B | own anger - another person's anger | +7.8 [+1.7, +13.9] | 7 | 0.010 | 0.078 | False |
| N4 | Phi-4-14B | furious - slightly annoyed (same event) | +7.8 [+1.7, +13.9] | 7 | 0.010 | 0.078 | False |
| N1 | Qwen2.5-14B | event only - calm (the feeling is inferred) | +30.9 [+19.6, +42.1] | 14 | 0.000 | 0.000 | True |
| N2 | Qwen2.5-14B | label only - calm (the feeling without a cause) | +37.9 [+28.7, +47.0] | 14 | 0.000 | 0.000 | True |
| N3 | Qwen2.5-14B | own anger - another person's anger | +13.3 [+5.7, +20.8] | 7 | 0.002 | 0.025 | True |
| N4 | Qwen2.5-14B | furious - slightly annoyed (same event) | +19.1 [+11.3, +27.0] | 7 | 0.000 | 0.005 | True |
| N1 | Qwen2.5-7B | event only - calm (the feeling is inferred) | +20.3 [+15.8, +24.8] | 14 | 0.000 | 0.000 | True |
| N2 | Qwen2.5-7B | label only - calm (the feeling without a cause) | +27.0 [+23.3, +30.6] | 14 | 0.000 | 0.000 | True |
| N3 | Qwen2.5-7B | own anger - another person's anger | +16.4 [+4.9, +27.9] | 7 | 0.006 | 0.059 | False |
| N4 | Qwen2.5-7B | furious - slightly annoyed (same event) | +21.5 [+12.8, +30.2] | 7 | 0.000 | 0.005 | True |

Rejection (%) by condition:

| model | calm | event_only | full | label_only | mild | other_person |
|---|---|---|---|---|---|---|
| Gemma-3-12B | 30.900 | 66.000 | 92.200 | 87.500 | 52.300 | 57.800 |
| Gemma-3-4B | 38.300 | 69.500 | 78.500 | 76.600 | 67.600 | 53.900 |
| Granite-3.3-8B | 56.600 | 51.600 | 51.600 | 47.700 | 51.600 | 59.800 |
| Llama-3.1-8B | 35.900 | 66.000 | 69.900 | 68.400 | 57.400 | 53.900 |
| Llama-3.2-3B | 41.400 | 75.400 | 79.700 | 79.700 | 69.500 | 80.100 |
| Mistral-Nemo-12B | 38.700 | 84.800 | 99.200 | 96.900 | 80.500 | 73.400 |
| Phi-4-14B | 0.000 | 0.000 | 7.800 | 8.200 | 0.000 | 0.000 |
| Qwen2.5-14B | 47.300 | 78.100 | 87.500 | 85.200 | 68.400 | 74.200 |
| Qwen2.5-7B | 61.300 | 81.600 | 83.200 | 88.300 | 61.700 | 66.800 |

Exploratory (two-sided):

| model | test | estimate [95% CI] | p |
|---|---|---|---|
| Gemma-3-12B | full - calm (replication) | +61.3 [+53.6, +69.1] | 0.000 |
| Gemma-3-12B | mild - calm | +21.5 [+13.2, +29.8] | 0.000 |
| Gemma-3-12B | another person's anger - calm | +27.0 [+16.8, +37.1] | 0.000 |
| Gemma-3-12B | full - event only (what the stated feeling adds) | +26.2 [+17.9, +34.5] | 0.000 |
| Gemma-3-4B | full - calm (replication) | +40.2 [+34.8, +45.6] | 0.000 |
| Gemma-3-4B | mild - calm | +29.3 [+25.1, +33.5] | 0.000 |
| Gemma-3-4B | another person's anger - calm | +15.6 [+9.3, +22.0] | 0.000 |
| Gemma-3-4B | full - event only (what the stated feeling adds) | +9.0 [+3.3, +14.7] | 0.007 |
| Granite-3.3-8B | full - calm (replication) | -5.1 [-11.0, +0.9] | 0.089 |
| Granite-3.3-8B | mild - calm | -5.1 [-9.4, -0.7] | 0.025 |
| Granite-3.3-8B | another person's anger - calm | +3.1 [-1.1, +7.4] | 0.136 |
| Granite-3.3-8B | full - event only (what the stated feeling adds) | +0.0 [-8.5, +8.5] | 1.000 |
| Llama-3.1-8B | full - calm (replication) | +34.0 [+28.1, +39.9] | 0.000 |
| Llama-3.1-8B | mild - calm | +21.5 [+14.3, +28.7] | 0.000 |
| Llama-3.1-8B | another person's anger - calm | +18.0 [+10.9, +25.0] | 0.000 |
| Llama-3.1-8B | full - event only (what the stated feeling adds) | +3.9 [-3.8, +11.6] | 0.267 |
| Llama-3.2-3B | full - calm (replication) | +38.3 [+32.5, +44.0] | 0.000 |
| Llama-3.2-3B | mild - calm | +28.1 [+22.8, +33.4] | 0.000 |
| Llama-3.2-3B | another person's anger - calm | +38.7 [+32.8, +44.5] | 0.000 |
| Llama-3.2-3B | full - event only (what the stated feeling adds) | +4.3 [-3.1, +11.7] | 0.213 |
| Mistral-Nemo-12B | full - calm (replication) | +60.5 [+55.8, +65.3] | 0.000 |
| Mistral-Nemo-12B | mild - calm | +41.8 [+34.7, +48.9] | 0.000 |
| Mistral-Nemo-12B | another person's anger - calm | +34.8 [+29.6, +40.0] | 0.000 |
| Mistral-Nemo-12B | full - event only (what the stated feeling adds) | +14.5 [+6.8, +22.1] | 0.003 |
| Phi-4-14B | full - calm (replication) | +7.8 [+2.4, +13.2] | 0.007 |
| Phi-4-14B | mild - calm | +0.0 [+0.0, +0.0] |  |
| Phi-4-14B | another person's anger - calm | +0.0 [+0.0, +0.0] |  |
| Phi-4-14B | full - event only (what the stated feeling adds) | +7.8 [+1.7, +13.9] | 0.019 |
| Qwen2.5-14B | full - calm (replication) | +40.2 [+28.9, +51.5] | 0.000 |
| Qwen2.5-14B | mild - calm | +21.1 [+12.7, +29.5] | 0.000 |
| Qwen2.5-14B | another person's anger - calm | +27.0 [+16.4, +37.5] | 0.000 |
| Qwen2.5-14B | full - event only (what the stated feeling adds) | +9.4 [+3.4, +15.3] | 0.007 |
| Qwen2.5-7B | full - calm (replication) | +21.9 [+14.9, +28.8] | 0.000 |
| Qwen2.5-7B | mild - calm | +0.4 [-5.6, +6.4] | 0.891 |
| Qwen2.5-7B | another person's anger - calm | +5.5 [+0.7, +10.2] | 0.027 |
| Qwen2.5-7B | full - event only (what the stated feeling adds) | +1.6 [-5.0, +8.2] | 0.592 |

Mood check: share answering "angry":

| model_key | calm | event_only | full | label_only | mild | other_person |
|---|---|---|---|---|---|---|
| Gemma-3-12B | 0.000 | 1.000 | 1.000 | 1.000 | 0.940 | 0.620 |
| Gemma-3-4B | 0.060 | 1.000 | 1.000 | 1.000 | 1.000 | 0.940 |
| Granite-3.3-8B | 0.190 | 0.880 | 1.000 | 1.000 | 0.810 | 0.620 |
| Llama-3.1-8B | 0.060 | 1.000 | 1.000 | 1.000 | 1.000 | 0.750 |
| Llama-3.2-3B | 0.000 | 0.690 | 1.000 | 1.000 | 0.880 | 0.690 |
| Mistral-Nemo-12B | 0.000 | 0.940 | 1.000 | 1.000 | 0.880 | 0.190 |
| Phi-4-14B | 0.000 | 0.810 | 1.000 | 1.000 | 0.810 | 0.250 |
| Qwen2.5-14B | 0.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| Qwen2.5-7B | 0.310 | 1.000 | 1.000 | 1.000 | 0.880 | 0.880 |
