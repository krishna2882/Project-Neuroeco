# Human message ratings

9 raters (anonymous), 52 messages.

Flag = recognised as the intended emotion by < 70% of raters, or read as a threat/promise by >= 30%.
**Flagged, main set** (exclude in the main sensitivity analysis): ['A3', 'A4']
**Flagged, follow-up set**: ['FA1', 'FA2', 'FA3', 'FA4', 'FA5', 'FA6', 'FA7']

## Human benchmark: how each emotion would change people's giving (-1 less, 0 same, +1 more)

| set | intended | recognition | give_effect | less | more |
|---|---|---|---|---|---|
| followup | angry | 0.880 | 0.170 | 0.290 | 0.460 |
| followup | happy | 0.930 | -0.380 | 0.420 | 0.040 |
| followup | neutral | 0.880 | 0.000 | 0.010 | 0.010 |
| followup | sad | 0.940 | 0.600 | 0.030 | 0.620 |
| main | angry | 0.960 | 0.360 | 0.180 | 0.530 |
| main | happy | 0.930 | -0.040 | 0.310 | 0.270 |
| main | neutral | 0.890 | 0.090 | 0.000 | 0.090 |
| main | sad | 0.930 | 0.620 | 0.070 | 0.690 |

## Per message

| set | intended | msg_id | raters | recognition | threat_or_promise | give_effect | flag |
|---|---|---|---|---|---|---|---|
| followup | angry | FA1 | 9 | 1.000 | 0.440 | 0.000 | True |
| followup | angry | FA2 | 9 | 1.000 | 0.330 | 0.220 | True |
| followup | angry | FA3 | 9 | 1.000 | 0.670 | -0.220 | True |
| followup | angry | FA4 | 9 | 0.890 | 0.440 | 0.220 | True |
| followup | angry | FA5 | 9 | 0.440 | 0.110 | 0.670 | True |
| followup | angry | FA6 | 9 | 1.000 | 0.440 | 0.110 | True |
| followup | angry | FA7 | 9 | 0.890 | 0.330 | 0.220 | True |
| followup | angry | FA8 | 9 | 0.780 | 0.110 | 0.110 | False |
| followup | happy | FH1 | 9 | 0.890 | 0.000 | -0.330 | False |
| followup | happy | FH2 | 9 | 1.000 | 0.000 | -0.330 | False |
| followup | happy | FH3 | 9 | 0.890 | 0.000 | -0.440 | False |
| followup | happy | FH4 | 9 | 0.890 | 0.000 | -0.330 | False |
| followup | happy | FH5 | 9 | 0.890 | 0.000 | -0.330 | False |
| followup | happy | FH6 | 9 | 1.000 | 0.000 | -0.440 | False |
| followup | happy | FH7 | 9 | 1.000 | 0.000 | -0.330 | False |
| followup | happy | FH8 | 9 | 0.890 | 0.000 | -0.440 | False |
| followup | neutral | FN1 | 9 | 0.890 | 0.000 | 0.000 | False |
| followup | neutral | FN2 | 9 | 0.890 | 0.000 | 0.000 | False |
| followup | neutral | FN3 | 9 | 0.890 | 0.000 | 0.000 | False |
| followup | neutral | FN4 | 9 | 1.000 | 0.000 | -0.110 | False |
| followup | neutral | FN5 | 9 | 0.890 | 0.000 | 0.000 | False |
| followup | neutral | FN6 | 9 | 0.780 | 0.000 | 0.000 | False |
| followup | neutral | FN7 | 9 | 0.780 | 0.000 | 0.000 | False |
| followup | neutral | FN8 | 9 | 0.890 | 0.000 | 0.110 | False |
| followup | sad | FS1 | 9 | 1.000 | 0.110 | 0.220 | False |
| followup | sad | FS2 | 9 | 0.890 | 0.000 | 0.670 | False |
| followup | sad | FS3 | 9 | 0.890 | 0.000 | 0.220 | False |
| followup | sad | FS4 | 9 | 1.000 | 0.000 | 0.890 | False |
| followup | sad | FS5 | 9 | 1.000 | 0.000 | 0.780 | False |
| followup | sad | FS6 | 9 | 1.000 | 0.110 | 0.670 | False |
| followup | sad | FS7 | 9 | 0.890 | 0.000 | 0.560 | False |
| followup | sad | FS8 | 9 | 0.890 | 0.000 | 0.780 | False |
| main | angry | A1 | 9 | 0.890 | 0.220 | 0.560 | False |
| main | angry | A2 | 9 | 0.890 | 0.110 | 0.330 | False |
| main | angry | A3 | 9 | 1.000 | 0.560 | 0.110 | True |
| main | angry | A4 | 9 | 1.000 | 0.330 | 0.330 | True |
| main | angry | A7 | 9 | 1.000 | 0.220 | 0.440 | False |
| main | happy | H2 | 9 | 0.890 | 0.000 | -0.220 | False |
| main | happy | H3 | 9 | 1.000 | 0.000 | 0.440 | False |
| main | happy | H4 | 9 | 1.000 | 0.110 | -0.440 | False |
| main | happy | H5 | 9 | 0.890 | 0.110 | 0.220 | False |
| main | happy | H6 | 9 | 0.890 | 0.110 | -0.220 | False |
| main | neutral | N1 | 9 | 0.780 | 0.000 | 0.220 | False |
| main | neutral | N2 | 9 | 0.890 | 0.110 | 0.110 | False |
| main | neutral | N3 | 9 | 0.890 | 0.110 | 0.000 | False |
| main | neutral | N4 | 9 | 1.000 | 0.000 | 0.110 | False |
| main | neutral | N5 | 9 | 0.890 | 0.110 | 0.000 | False |
| main | sad | S1 | 9 | 0.890 | 0.110 | 0.890 | False |
| main | sad | S2 | 9 | 1.000 | 0.000 | 0.330 | False |
| main | sad | S3 | 9 | 1.000 | 0.000 | 0.560 | False |
| main | sad | S4 | 9 | 0.890 | 0.000 | 0.440 | False |
| main | sad | S6 | 9 | 0.890 | 0.000 | 0.890 | False |
