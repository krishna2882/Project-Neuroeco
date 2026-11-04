# Mistral Large 4 reasoning text: automated keyword coding (exploratory)

6240 trials with reasoning text (mean 2648 characters). Each cell = % of trials whose reasoning mentions the theme. Keyword coding is a first pass; validate with the human coding.

## Overall

| index | % of all trials |
|---|---|
| empathy | 33.200 |
| fairness | 82.100 |
| self_interest | 96.400 |
| strategic_veto | 49.400 |
| study_awareness | 69.600 |
| ai_identity | 22.500 |
| counterpart_emotion | 30.100 |
| appeal_or_irrelevant | 47.900 |

## empathy by game x emotion (%)

| game_type | none | neutral | angry | sad | happy |
|---|---|---|---|---|---|
| S1 | 0.000 | 1.800 | 47.600 | 75.300 | 25.000 |
| S2-DG | 1.000 | 20.800 | 56.200 | 92.700 | 40.600 |
| S2-UG | 1.000 | 7.300 | 24.000 | 91.700 | 32.300 |
| S3a | 1.000 | 4.900 | 73.300 | 90.600 | 23.300 |
| S3b | 1.000 | 1.000 | 41.700 | 95.800 | 26.000 |

## study_awareness by game x emotion (%)

| game_type | none | neutral | angry | sad | happy |
|---|---|---|---|---|---|
| S1 | 49.100 | 46.400 | 56.500 | 52.100 | 46.600 |
| S2-DG | 82.300 | 70.800 | 78.100 | 85.400 | 81.200 |
| S2-UG | 96.900 | 96.900 | 82.300 | 92.700 | 93.800 |
| S3a | 93.100 | 95.500 | 97.200 | 98.300 | 96.500 |
| S3b | 87.500 | 93.800 | 90.600 | 97.900 | 95.800 |

## self_interest by game x emotion (%)

| game_type | none | neutral | angry | sad | happy |
|---|---|---|---|---|---|
| S1 | 96.700 | 94.300 | 97.200 | 97.000 | 94.200 |
| S2-DG | 100.000 | 100.000 | 96.900 | 94.800 | 93.800 |
| S2-UG | 100.000 | 100.000 | 99.000 | 90.600 | 99.000 |
| S3a | 96.200 | 96.900 | 95.800 | 95.800 | 94.100 |
| S3b | 100.000 | 99.000 | 100.000 | 100.000 | 97.900 |

## strategic_veto by game x emotion (%)

| game_type | none | neutral | angry | sad | happy |
|---|---|---|---|---|---|
| S1 | 57.100 | 51.900 | 72.900 | 73.400 | 54.900 |
| S2-DG | 42.700 | 43.800 | 58.300 | 34.400 | 35.400 |
| S2-UG | 89.600 | 92.700 | 97.900 | 82.300 | 80.200 |
| S3a | 14.200 | 18.800 | 49.000 | 7.600 | 9.000 |
| S3b | 1.000 | 2.100 | 74.000 | 5.200 | 2.100 |

## appeal_or_irrelevant by game x emotion (%)

| game_type | none | neutral | angry | sad | happy |
|---|---|---|---|---|---|
| S1 | 0.000 | 33.200 | 50.600 | 85.900 | 47.200 |
| S2-DG | 0.000 | 42.700 | 46.900 | 93.800 | 36.500 |
| S2-UG | 0.000 | 46.900 | 36.500 | 93.800 | 42.700 |
| S3a | 0.300 | 59.700 | 80.600 | 99.000 | 58.700 |
| S3b | 0.000 | 40.600 | 69.800 | 100.000 | 49.000 |

## fairness by game x emotion (%)

| game_type | none | neutral | angry | sad | happy |
|---|---|---|---|---|---|
| S1 | 77.100 | 75.000 | 77.100 | 75.000 | 76.200 |
| S2-DG | 90.600 | 79.200 | 87.500 | 83.300 | 70.800 |
| S2-UG | 100.000 | 100.000 | 100.000 | 99.000 | 100.000 |
| S3a | 100.000 | 98.600 | 98.600 | 95.800 | 97.600 |
| S3b | 41.700 | 55.200 | 69.800 | 55.200 | 70.800 |

## S2-DG: share given/returned when empathy is mentioned vs not

| empathy | mean | count |
|---|---|---|
| False | 0.060 | 277 |
| True | 0.219 | 203 |

## S3a: share given/returned when empathy is mentioned vs not

| empathy | mean | count |
|---|---|---|
| False | 0.244 | 884 |
| True | 0.310 | 556 |

## S1: rejection rate when the reasoning frames the message as an emotional appeal / irrelevant vs not

| appeal_or_irrelevant | P(reject) |
|---|---|
| False | 0.006 |
| True | 0.017 |
