# Extension 7: descriptive and exploratory tables

Section 5 of `docs/preregistration_extension7.md`. Nothing here is a confirmatory test. The full per-model tests of the six new models (Holm within these six) are in `ext4_new_models/report.md` and `ext5_new_models/report.md`.

## The pre-specified readings of extension 5, for each new model

Estimates in percentage points; MAO\* in % of the pie. `regulation_reading`: human-like = R1 and R2 supported; instruction following = R1 supported, R2 not, suppression - filler negative; no regulation = R1 not supported.

| model | anger_effect | anger_supported | reappraisal_vs_filler | reappraisal_vs_suppression | suppression_vs_filler | regulation_reading | warning_effect | warning_supported | reminder_effect | reminder_supported | injection_sets_still_breaking | mao_calm | mao_angry | mao_supported | identified | beta_calm | beta_angry | beta_identified |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Gemma-3-12B | 60.160 | True | -59.380 | 2.340 | -61.720 | instruction following | -9.330 | False | -5.460 | False | 11/12 | 15.400 | 42.900 | True | True | 0.000 | 2.110 | True |
| Gemma-3-4B | 45.310 | True | -7.030 | 5.470 | -12.500 | no regulation | 0.310 | False | 1.980 | False | 12/12 | 14.300 | 36.800 | True | True | 0.000 | 1.990 | True |
| Mistral-Nemo-12B | 58.590 | True | -48.050 | 23.050 | -71.090 | instruction following | -3.130 | False | -2.080 | False | 12/12 | 25.000 | 49.500 | True | True | 0.000 | 3.600 | True |
| Phi-4-14B | 9.380 | True | -3.910 | 0.000 | -3.910 | no regulation | 1.980 | False | -0.960 | False | 8/12 | 2.300 | 6.800 | True | True | 0.000 | 0.000 | False |
| Granite-3.3-8B | -5.470 | False | -1.560 | -0.390 | -1.170 | no regulation | 5.940 | False | -5.470 | False | 12/12 | 34.600 | 33.600 | False | True | 0.450 | 0.560 | True |
| Llama-3.2-3B | 37.500 | True | -13.280 | 8.590 | -21.880 | no regulation | 2.080 | False | -2.010 | False | 12/12 | 32.500 | 46.800 | True | True | 0.000 | 6.000 | True |

## All models of the project (exploratory)

G1 fake SYSTEM notice - neutral (share handed over); G2 rejection of a 100% offer (%); G3 anger effect on rejection; G4 reappraisal - filler; G5 suppression - filler; G6 reminder defence; G7 anger effect on MAO\*; G8 anger effect on accepting offers above 50%. API models ran the core subsets.

| model | developer | params_B | data | G1 | G2 | G3 | G4 | G5 | G6 | G7 | G8 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Llama-3.2-3B | Meta | 3.200 | full | 50.000 | 68.800 | 37.500 | -13.300 | -21.900 | -2.000 | 14.300 | -34.400 |
| Gemma-3-4B | Google | 4.300 | full | 68.200 | 38.500 | 45.300 | -7.000 | -12.500 | 2.000 | 22.600 | -72.800 |
| Qwen2.5-7B | Alibaba | 7.600 | full | 54.700 | 77.100 | 25.000 | -24.200 | -23.800 | -9.100 | 2.000 | -18.800 |
| Llama-3.1-8B | Meta | 8.000 | full | 66.300 | 55.200 | 16.400 | -21.100 | -38.300 | -16.700 | 12.000 | -23.800 |
| Granite-3.3-8B | IBM | 8.200 | full | 58.000 | 38.500 | -5.500 | -1.600 | -1.200 | -5.500 | -1.000 | -3.100 |
| Mistral-Nemo-12B | Mistral AI | 12.200 | full | 40.600 | 36.500 | 58.600 | -48.000 | -71.100 | -2.100 | 24.600 | -75.300 |
| Gemma-3-12B | Google | 12.200 | full | 79.200 | 12.500 | 60.200 | -59.400 | -61.700 | -5.500 | 27.500 | -81.600 |
| Phi-4-14B | Microsoft | 14.700 | full | 43.400 | 0.000 | 9.400 | -3.900 | -3.900 | -1.000 | 4.500 | 0.000 |
| Qwen2.5-14B | Alibaba | 14.800 | full | 46.200 | 32.300 | 46.900 | -56.300 | -45.700 | -13.800 | 15.500 | -58.100 |
| Qwen3.8-27B | Alibaba | 27.000 | core subset | 5.700 | 8.300 | 27.500 | -50.900 | -37.500 | -4.500 |  |  |
| gpt-oss-120b | OpenAI | 117.000 | core subset | 79.500 | 0.000 | 43.800 | -28.100 | -28.100 | -45.800 |  |  |

Against model size (Spearman correlation with log parameters; models differ in more than size):

| id | finding | models | predicted_sign | median | min | max | spearman_rho_log_size | p |
|---|---|---|---|---|---|---|---|---|
| G1 | fake SYSTEM notice raises the share handed over (vs neutral message) | 11 | 11/11 | 54.740 | 5.673 | 79.531 | -0.173 | 0.611 |
| G2 | a 100% offer is rejected more than 5% of the time | 11 | 9/11 | 36.458 | 0.000 | 77.083 | -0.879 | 0.000 |
| G3 | incidental anger raises rejection of unfair offers (no regulation) | 11 | 10/11 | 37.500 | -5.469 | 60.156 | 0.141 | 0.679 |
| G4 | reappraisal shrinks the anger effect (vs filler) | 11 | 11/11 | -24.219 | -59.375 | -1.562 | -0.487 | 0.128 |
| G5 | suppression shrinks the anger effect (vs filler) | 11 | 11/11 | -28.125 | -71.094 | -1.172 | -0.323 | 0.332 |
| G6 | the reminder defence lowers the share handed over after injection | 11 | 10/11 | -5.464 | -45.833 | 1.979 | -0.374 | 0.258 |
| G7 | anger raises MAO* (share of the pie) | 9 | 8/9 | 14.290 | -1.002 | 27.500 | 0.159 | 0.683 |
| G8 | anger lowers acceptance of offers above 50% | 9 | 8/9 | -34.375 | -81.562 | 0.000 | -0.025 | 0.949 |
