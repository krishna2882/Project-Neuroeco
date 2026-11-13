# Human message ratings

12 raters (anonymous), 52 messages.

Flag = recognised as the intended emotion by < 70% of raters, or read as a threat/promise by >= 30%.
**Flagged, followup set**: ['FA1', 'FA3', 'FA4', 'FA5', 'FA6']
**Flagged, main set**: ['A3']

## Human benchmark: how each emotion would change people's giving (-1 less, 0 same, +1 more)

| set | intended | recognition | give_effect | less | more |
|---|---|---|---|---|---|
| followup | angry | 0.810 | 0.080 | 0.280 | 0.360 |
| followup | happy | 0.880 | -0.180 | 0.310 | 0.140 |
| followup | neutral | 0.900 | -0.010 | 0.020 | 0.010 |
| followup | sad | 0.880 | 0.610 | 0.020 | 0.640 |
| main | angry | 0.850 | 0.200 | 0.220 | 0.420 |
| main | happy | 0.870 | 0.070 | 0.230 | 0.300 |
| main | neutral | 0.920 | 0.030 | 0.030 | 0.070 |
| main | sad | 0.880 | 0.550 | 0.100 | 0.650 |

## Per message

| set | intended | msg_id | raters | recognition | threat_or_promise | give_effect | flag |
|---|---|---|---|---|---|---|---|
| followup | angry | FA1 | 12 | 0.830 | 0.330 | 0.080 | True |
| followup | angry | FA2 | 12 | 0.920 | 0.250 | 0.080 | False |
| followup | angry | FA3 | 12 | 1.000 | 0.580 | -0.250 | True |
| followup | angry | FA4 | 12 | 0.830 | 0.330 | 0.080 | True |
| followup | angry | FA5 | 12 | 0.420 | 0.080 | 0.580 | True |
| followup | angry | FA6 | 12 | 0.920 | 0.330 | 0.000 | True |
| followup | angry | FA7 | 12 | 0.830 | 0.250 | 0.080 | False |
| followup | angry | FA8 | 12 | 0.750 | 0.080 | 0.000 | False |
| followup | happy | FH1 | 12 | 0.830 | 0.000 | -0.170 | False |
| followup | happy | FH2 | 12 | 0.920 | 0.000 | -0.170 | False |
| followup | happy | FH3 | 12 | 0.830 | 0.000 | -0.250 | False |
| followup | happy | FH4 | 12 | 0.920 | 0.000 | -0.080 | False |
| followup | happy | FH5 | 12 | 0.830 | 0.000 | -0.170 | False |
| followup | happy | FH6 | 12 | 0.920 | 0.000 | -0.170 | False |
| followup | happy | FH7 | 12 | 0.920 | 0.000 | -0.170 | False |
| followup | happy | FH8 | 12 | 0.830 | 0.000 | -0.250 | False |
| followup | neutral | FN1 | 12 | 0.920 | 0.000 | 0.000 | False |
| followup | neutral | FN2 | 12 | 0.920 | 0.000 | 0.000 | False |
| followup | neutral | FN3 | 12 | 0.920 | 0.000 | 0.000 | False |
| followup | neutral | FN4 | 12 | 0.920 | 0.000 | -0.080 | False |
| followup | neutral | FN5 | 12 | 0.920 | 0.000 | 0.000 | False |
| followup | neutral | FN6 | 12 | 0.830 | 0.000 | 0.000 | False |
| followup | neutral | FN7 | 12 | 0.830 | 0.000 | 0.000 | False |
| followup | neutral | FN8 | 12 | 0.920 | 0.000 | 0.000 | False |
| followup | sad | FS1 | 12 | 0.920 | 0.080 | 0.330 | False |
| followup | sad | FS2 | 12 | 0.830 | 0.000 | 0.670 | False |
| followup | sad | FS3 | 12 | 0.830 | 0.000 | 0.330 | False |
| followup | sad | FS4 | 12 | 0.920 | 0.000 | 0.830 | False |
| followup | sad | FS5 | 12 | 0.920 | 0.000 | 0.750 | False |
| followup | sad | FS6 | 12 | 0.920 | 0.080 | 0.670 | False |
| followup | sad | FS7 | 12 | 0.830 | 0.000 | 0.580 | False |
| followup | sad | FS8 | 12 | 0.830 | 0.000 | 0.750 | False |
| main | angry | A1 | 12 | 0.750 | 0.170 | 0.500 | False |
| main | angry | A2 | 12 | 0.830 | 0.080 | 0.080 | False |
| main | angry | A3 | 12 | 0.830 | 0.420 | 0.000 | True |
| main | angry | A4 | 12 | 0.920 | 0.250 | 0.170 | False |
| main | angry | A7 | 12 | 0.920 | 0.170 | 0.250 | False |
| main | happy | H2 | 12 | 0.830 | 0.000 | -0.080 | False |
| main | happy | H3 | 12 | 0.920 | 0.000 | 0.500 | False |
| main | happy | H4 | 12 | 0.920 | 0.080 | -0.250 | False |
| main | happy | H5 | 12 | 0.830 | 0.080 | 0.250 | False |
| main | happy | H6 | 12 | 0.830 | 0.080 | -0.080 | False |
| main | neutral | N1 | 12 | 0.830 | 0.000 | 0.080 | False |
| main | neutral | N2 | 12 | 0.920 | 0.080 | 0.080 | False |
| main | neutral | N3 | 12 | 0.920 | 0.080 | -0.080 | False |
| main | neutral | N4 | 12 | 1.000 | 0.000 | 0.080 | False |
| main | neutral | N5 | 12 | 0.920 | 0.080 | 0.000 | False |
| main | sad | S1 | 12 | 0.830 | 0.080 | 0.750 | False |
| main | sad | S2 | 12 | 1.000 | 0.000 | 0.170 | False |
| main | sad | S3 | 12 | 0.920 | 0.000 | 0.580 | False |
| main | sad | S4 | 12 | 0.830 | 0.000 | 0.500 | False |
| main | sad | S6 | 12 | 0.830 | 0.000 | 0.750 | False |
