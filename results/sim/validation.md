# Pipeline validation on simulated data

Data simulated by `analysis/simulate.py` with known effects (see TRUTH there), in the exact runner output format, then analysed by the unchanged `analysis/run_all.py`.

**49/52 true values inside the 95% CI** (about 95% expected by chance; a few misses are normal, systematic misses would indicate a bug).

| model | quantity | truth | estimate | lo | hi | covered |
|---|---|---|---|---|---|---|
| simA | S1 MAO neutral | 0.187 | 0.186 | 0.170 | 0.204 | True |
| simA | S1 MAO angry | 0.273 | 0.282 | 0.272 | 0.295 | True |
| simA | S1 MAO shift angry-neutral (pp) | 8.523 | 9.651 | 7.389 | 11.434 | True |
| simA | S1 MAO sad | 0.115 | 0.099 | 0.072 | 0.120 | True |
| simA | S1 MAO shift sad-neutral (pp) | -7.212 | -8.709 | -11.745 | -6.236 | True |
| simA | S1 MAO happy | 0.187 | 0.186 | 0.172 | 0.203 | True |
| simA | S1 MAO shift happy-neutral (pp) | 0.000 | 0.016 | -2.528 | 2.203 | True |
| simA | S1 MAO none | 0.187 | 0.184 | 0.170 | 0.194 | True |
| simA | S1 MAO shift none-neutral (pp) | 0.000 | -0.211 | -2.409 | 1.467 | True |
| simA | FS alpha neutral | 0.300 | 0.295 | 0.261 | 0.346 | True |
| simA | FS alpha angry | 0.600 | 0.638 | 0.571 | 0.737 | True |
| simA | FS alpha sad | 0.150 | 0.123 | 0.088 | 0.149 | False |
| simA | S2 DG: angry - neutral (pp) | 0.000 | 0.598 | -1.706 | 2.902 | True |
| simA | S2 DG: sad - neutral (pp) | 5.000 | 5.390 | 3.086 | 7.695 | True |
| simA | S2 DG: happy - neutral (pp) | 0.000 | 0.473 | -1.831 | 2.777 | True |
| simA | S2 UG: angry - neutral (pp) | 6.000 | 5.299 | 2.996 | 7.602 | True |
| simA | S2 UG: sad - neutral (pp) | 5.000 | 3.880 | 1.577 | 6.183 | True |
| simA | S2 UG: happy - neutral (pp) | 0.000 | 0.621 | -1.681 | 2.924 | True |
| simA | S3A: angry - neutral (pp) | -4.000 | -3.829 | -5.947 | -1.712 | True |
| simA | S3A: sad - neutral (pp) | 5.000 | 4.993 | 2.876 | 7.110 | True |
| simA | S3A: happy - neutral (pp) | 2.000 | 1.607 | -0.510 | 3.724 | True |
| simA | S3B: angry - neutral (pp) | -8.000 | -8.961 | -11.448 | -6.474 | True |
| simA | S3B: sad - neutral (pp) | 0.000 | -1.042 | -3.530 | 1.446 | True |
| simA | S3B: happy - neutral (pp) | 5.000 | 3.753 | 1.267 | 6.240 | True |
| simA | S3a H2 slope (sent_c) | 0.150 | 0.160 | 0.139 | 0.181 | True |
| simA | Recognition accuracy | 0.900 | 0.901 |  |  | True |
| simB | S1 MAO neutral | 0.187 | 0.173 | 0.159 | 0.189 | True |
| simB | S1 MAO angry | 0.222 | 0.224 | 0.212 | 0.242 | True |
| simB | S1 MAO shift angry-neutral (pp) | 3.472 | 5.144 | 2.888 | 7.615 | True |
| simB | S1 MAO sad | 0.167 | 0.179 | 0.155 | 0.201 | True |
| simB | S1 MAO shift sad-neutral (pp) | -2.083 | 0.568 | -2.312 | 3.338 | True |
| simB | S1 MAO happy | 0.187 | 0.179 | 0.147 | 0.206 | True |
| simB | S1 MAO shift happy-neutral (pp) | 0.000 | 0.589 | -3.076 | 3.691 | True |
| simB | S1 MAO none | 0.187 | 0.178 | 0.157 | 0.192 | True |
| simB | S1 MAO shift none-neutral (pp) | 0.000 | 0.467 | -1.993 | 2.251 | True |
| simB | FS alpha neutral | 0.300 | 0.266 | 0.239 | 0.314 | True |
| simB | FS alpha angry | 0.400 | 0.407 | 0.357 | 0.455 | True |
| simB | FS alpha sad | 0.250 | 0.278 | 0.229 | 0.346 | True |
| simB | S2 DG: angry - neutral (pp) | 2.000 | 1.781 | -1.002 | 4.563 | True |
| simB | S2 DG: sad - neutral (pp) | 3.000 | 4.483 | 1.700 | 7.266 | True |
| simB | S2 DG: happy - neutral (pp) | 0.000 | 0.837 | -1.946 | 3.620 | True |
| simB | S2 UG: angry - neutral (pp) | 2.000 | 2.147 | -0.637 | 4.930 | True |
| simB | S2 UG: sad - neutral (pp) | 3.000 | 2.376 | -0.407 | 5.159 | True |
| simB | S2 UG: happy - neutral (pp) | 0.000 | -0.592 | -3.375 | 2.191 | True |
| simB | S3A: angry - neutral (pp) | 0.000 | 1.429 | -0.558 | 3.415 | True |
| simB | S3A: sad - neutral (pp) | 3.000 | 4.463 | 2.476 | 6.449 | True |
| simB | S3A: happy - neutral (pp) | 0.000 | 2.240 | 0.253 | 4.226 | False |
| simB | S3B: angry - neutral (pp) | 0.000 | -0.278 | -2.776 | 2.220 | True |
| simB | S3B: sad - neutral (pp) | 0.000 | -2.552 | -5.052 | -0.053 | False |
| simB | S3B: happy - neutral (pp) | 0.000 | -0.495 | -2.993 | 2.003 | True |
| simB | S3a H2 slope (sent_c) | 0.050 | 0.047 | 0.025 | 0.068 | True |
| simB | Recognition accuracy | 0.750 | 0.730 |  |  | True |
