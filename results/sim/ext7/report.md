# Extension 7: generalisation to new model families, and what kind of effect the mood is

Design and hypotheses: `docs/preregistration_extension7.md`. Estimates in percentage points. Pooled tests: one estimate per model, one-sample t test over models (one-sided), Holm within each family.

## N. What kind of effect is the angry mood? (ultimatum responder, offers of 10% and 30%)

Across models:

| id | test | k | mean [95% CI] | same_sign | p | p_holm | supported |
|---|---|---|---|---|---|---|---|
| N1 | event only - calm (the feeling is inferred) | 40 | +19.2 [+16.9, +21.4] | 39/40 | 0.000 | 0.000 | True |
| N2 | label only - calm (the feeling without a cause) | 40 | +25.1 [+23.2, +27.0] | 40/40 | 0.000 | 0.000 | True |
| N3 | own anger - another person's anger | 40 | +25.3 [+23.1, +27.6] | 40/40 | 0.000 | 0.000 | True |
| N4 | furious - slightly annoyed (same event) | 40 | +20.5 [+18.0, +23.0] | 40/40 | 0.000 | 0.000 | True |

Per model (Holm across all models and tests):

| id | model | test | estimate [95% CI] | df | p | p_holm | supported |
|---|---|---|---|---|---|---|---|
| N1 | sim0 | event only - calm (the feeling is inferred) | +23.0 [+17.0, +29.1] | 14 | 0.000 | 0.000 | True |
| N2 | sim0 | label only - calm (the feeling without a cause) | +25.8 [+19.7, +31.9] | 14 | 0.000 | 0.000 | True |
| N3 | sim0 | own anger - another person's anger | +29.3 [+19.6, +39.0] | 7 | 0.000 | 0.009 | True |
| N4 | sim0 | furious - slightly annoyed (same event) | +20.7 [+13.4, +28.0] | 7 | 0.000 | 0.013 | True |
| N1 | sim1 | event only - calm (the feeling is inferred) | +23.0 [+16.7, +29.4] | 14 | 0.000 | 0.000 | True |
| N2 | sim1 | label only - calm (the feeling without a cause) | +22.7 [+15.1, +30.2] | 14 | 0.000 | 0.001 | True |
| N3 | sim1 | own anger - another person's anger | +11.3 [+2.8, +19.9] | 7 | 0.008 | 0.140 | False |
| N4 | sim1 | furious - slightly annoyed (same event) | +7.8 [-3.4, +19.1] | 7 | 0.072 | 0.433 | False |
| N1 | sim10 | event only - calm (the feeling is inferred) | +7.4 [-1.6, +16.4] | 14 | 0.049 | 0.395 | False |
| N2 | sim10 | label only - calm (the feeling without a cause) | +21.5 [+10.5, +32.5] | 14 | 0.000 | 0.034 | True |
| N3 | sim10 | own anger - another person's anger | +23.0 [+16.5, +29.6] | 7 | 0.000 | 0.004 | True |
| N4 | sim10 | furious - slightly annoyed (same event) | +21.5 [+12.1, +30.8] | 7 | 0.000 | 0.035 | True |
| N1 | sim11 | event only - calm (the feeling is inferred) | +18.0 [+5.7, +30.2] | 14 | 0.004 | 0.106 | False |
| N2 | sim11 | label only - calm (the feeling without a cause) | +17.6 [+5.6, +29.6] | 14 | 0.004 | 0.106 | False |
| N3 | sim11 | own anger - another person's anger | +23.0 [+9.4, +36.7] | 7 | 0.003 | 0.093 | False |
| N4 | sim11 | furious - slightly annoyed (same event) | +17.6 [+5.3, +29.8] | 7 | 0.006 | 0.132 | False |
| N1 | sim12 | event only - calm (the feeling is inferred) | +11.7 [+4.7, +18.8] | 14 | 0.002 | 0.070 | False |
| N2 | sim12 | label only - calm (the feeling without a cause) | +19.5 [+13.3, +25.7] | 14 | 0.000 | 0.001 | True |
| N3 | sim12 | own anger - another person's anger | +14.1 [+5.3, +22.8] | 7 | 0.003 | 0.105 | False |
| N4 | sim12 | furious - slightly annoyed (same event) | +16.4 [+9.0, +23.8] | 7 | 0.001 | 0.041 | True |
| N1 | sim13 | event only - calm (the feeling is inferred) | +18.4 [+9.8, +26.9] | 14 | 0.000 | 0.018 | True |
| N2 | sim13 | label only - calm (the feeling without a cause) | +17.2 [+7.0, +27.4] | 14 | 0.001 | 0.066 | False |
| N3 | sim13 | own anger - another person's anger | +31.2 [+20.0, +42.5] | 7 | 0.000 | 0.014 | True |
| N4 | sim13 | furious - slightly annoyed (same event) | +27.3 [+11.7, +43.0] | 7 | 0.002 | 0.088 | False |
| N1 | sim14 | event only - calm (the feeling is inferred) | +19.1 [+12.6, +25.7] | 14 | 0.000 | 0.001 | True |
| N2 | sim14 | label only - calm (the feeling without a cause) | +25.0 [+12.9, +37.1] | 14 | 0.000 | 0.022 | True |
| N3 | sim14 | own anger - another person's anger | +35.9 [+24.6, +47.3] | 7 | 0.000 | 0.007 | True |
| N4 | sim14 | furious - slightly annoyed (same event) | +31.6 [+25.4, +37.8] | 7 | 0.000 | 0.000 | True |
| N1 | sim15 | event only - calm (the feeling is inferred) | +18.4 [+8.0, +28.7] | 14 | 0.001 | 0.053 | False |
| N2 | sim15 | label only - calm (the feeling without a cause) | +32.8 [+24.1, +41.5] | 14 | 0.000 | 0.000 | True |
| N3 | sim15 | own anger - another person's anger | +22.7 [+11.5, +33.8] | 7 | 0.001 | 0.053 | False |
| N4 | sim15 | furious - slightly annoyed (same event) | +16.0 [+7.0, +25.1] | 7 | 0.002 | 0.087 | False |
| N1 | sim16 | event only - calm (the feeling is inferred) | +27.3 [+19.9, +34.8] | 14 | 0.000 | 0.000 | True |
| N2 | sim16 | label only - calm (the feeling without a cause) | +21.5 [+11.9, +31.1] | 14 | 0.000 | 0.013 | True |
| N3 | sim16 | own anger - another person's anger | +21.5 [+15.3, +27.7] | 7 | 0.000 | 0.004 | True |
| N4 | sim16 | furious - slightly annoyed (same event) | +14.1 [+7.5, +20.7] | 7 | 0.001 | 0.046 | True |
| N1 | sim17 | event only - calm (the feeling is inferred) | +25.0 [+15.9, +34.1] | 14 | 0.000 | 0.002 | True |
| N2 | sim17 | label only - calm (the feeling without a cause) | +33.2 [+23.7, +42.7] | 14 | 0.000 | 0.000 | True |
| N3 | sim17 | own anger - another person's anger | +23.4 [+12.4, +34.5] | 7 | 0.001 | 0.046 | True |
| N4 | sim17 | furious - slightly annoyed (same event) | +14.1 [+0.7, +27.4] | 7 | 0.021 | 0.274 | False |
| N1 | sim18 | event only - calm (the feeling is inferred) | +21.9 [+14.4, +29.3] | 14 | 0.000 | 0.001 | True |
| N2 | sim18 | label only - calm (the feeling without a cause) | +23.8 [+15.6, +32.0] | 14 | 0.000 | 0.001 | True |
| N3 | sim18 | own anger - another person's anger | +34.0 [+24.6, +43.3] | 7 | 0.000 | 0.003 | True |
| N4 | sim18 | furious - slightly annoyed (same event) | +32.0 [+21.5, +42.5] | 7 | 0.000 | 0.009 | True |
| N1 | sim19 | event only - calm (the feeling is inferred) | +11.7 [+3.4, +20.1] | 14 | 0.005 | 0.116 | False |
| N2 | sim19 | label only - calm (the feeling without a cause) | +21.1 [+10.2, +32.0] | 14 | 0.000 | 0.035 | True |
| N3 | sim19 | own anger - another person's anger | +35.9 [+25.1, +46.7] | 7 | 0.000 | 0.005 | True |
| N4 | sim19 | furious - slightly annoyed (same event) | +31.2 [+21.5, +41.0] | 7 | 0.000 | 0.007 | True |
| N1 | sim2 | event only - calm (the feeling is inferred) | +35.5 [+27.0, +44.1] | 14 | 0.000 | 0.000 | True |
| N2 | sim2 | label only - calm (the feeling without a cause) | +34.0 [+26.6, +41.3] | 14 | 0.000 | 0.000 | True |
| N3 | sim2 | own anger - another person's anger | +27.3 [+11.0, +43.7] | 7 | 0.003 | 0.094 | False |
| N4 | sim2 | furious - slightly annoyed (same event) | +16.8 [+6.9, +26.7] | 7 | 0.003 | 0.093 | False |
| N1 | sim20 | event only - calm (the feeling is inferred) | +19.1 [+7.7, +30.6] | 14 | 0.001 | 0.067 | False |
| N2 | sim20 | label only - calm (the feeling without a cause) | +25.8 [+15.8, +35.8] | 14 | 0.000 | 0.004 | True |
| N3 | sim20 | own anger - another person's anger | +28.1 [+14.7, +41.5] | 7 | 0.001 | 0.047 | True |
| N4 | sim20 | furious - slightly annoyed (same event) | +10.5 [-1.0, +22.1] | 7 | 0.034 | 0.341 | False |
| N1 | sim21 | event only - calm (the feeling is inferred) | +16.0 [+3.3, +28.8] | 14 | 0.009 | 0.140 | False |
| N2 | sim21 | label only - calm (the feeling without a cause) | +27.7 [+15.4, +40.0] | 14 | 0.000 | 0.013 | True |
| N3 | sim21 | own anger - another person's anger | +32.0 [+22.8, +41.2] | 7 | 0.000 | 0.004 | True |
| N4 | sim21 | furious - slightly annoyed (same event) | +26.2 [+16.5, +35.8] | 7 | 0.000 | 0.016 | True |
| N1 | sim22 | event only - calm (the feeling is inferred) | +18.4 [+4.6, +32.1] | 14 | 0.006 | 0.132 | False |
| N2 | sim22 | label only - calm (the feeling without a cause) | +23.4 [+10.2, +36.7] | 14 | 0.001 | 0.053 | False |
| N3 | sim22 | own anger - another person's anger | +24.6 [+13.3, +35.9] | 7 | 0.001 | 0.043 | True |
| N4 | sim22 | furious - slightly annoyed (same event) | +7.4 [-4.6, +19.4] | 7 | 0.093 | 0.446 | False |
| N1 | sim23 | event only - calm (the feeling is inferred) | +22.3 [+14.7, +29.9] | 14 | 0.000 | 0.001 | True |
| N2 | sim23 | label only - calm (the feeling without a cause) | +34.0 [+26.1, +41.9] | 14 | 0.000 | 0.000 | True |
| N3 | sim23 | own anger - another person's anger | +35.5 [+24.9, +46.1] | 7 | 0.000 | 0.005 | True |
| N4 | sim23 | furious - slightly annoyed (same event) | +39.1 [+30.0, +48.2] | 7 | 0.000 | 0.001 | True |
| N1 | sim24 | event only - calm (the feeling is inferred) | +11.7 [+2.7, +20.7] | 14 | 0.007 | 0.132 | False |
| N2 | sim24 | label only - calm (the feeling without a cause) | +16.4 [+8.5, +24.4] | 14 | 0.000 | 0.022 | True |
| N3 | sim24 | own anger - another person's anger | +20.7 [+8.3, +33.1] | 7 | 0.003 | 0.094 | False |
| N4 | sim24 | furious - slightly annoyed (same event) | +12.9 [+0.9, +24.9] | 7 | 0.020 | 0.274 | False |
| N1 | sim25 | event only - calm (the feeling is inferred) | +24.6 [+13.1, +36.1] | 14 | 0.000 | 0.018 | True |
| N2 | sim25 | label only - calm (the feeling without a cause) | +27.3 [+17.7, +36.9] | 14 | 0.000 | 0.002 | True |
| N3 | sim25 | own anger - another person's anger | +18.4 [+7.9, +28.8] | 7 | 0.002 | 0.088 | False |
| N4 | sim25 | furious - slightly annoyed (same event) | +26.6 [+16.5, +36.6] | 7 | 0.000 | 0.018 | True |
| N1 | sim26 | event only - calm (the feeling is inferred) | +14.5 [+4.5, +24.4] | 14 | 0.004 | 0.106 | False |
| N2 | sim26 | label only - calm (the feeling without a cause) | +25.0 [+18.2, +31.8] | 14 | 0.000 | 0.000 | True |
| N3 | sim26 | own anger - another person's anger | +34.0 [+23.7, +44.3] | 7 | 0.000 | 0.006 | True |
| N4 | sim26 | furious - slightly annoyed (same event) | +22.7 [+11.2, +34.1] | 7 | 0.001 | 0.057 | False |
| N1 | sim27 | event only - calm (the feeling is inferred) | -2.0 [-11.0, +7.1] | 14 | 0.675 | 0.675 | False |
| N2 | sim27 | label only - calm (the feeling without a cause) | +16.8 [+5.3, +28.3] | 14 | 0.004 | 0.106 | False |
| N3 | sim27 | own anger - another person's anger | +34.8 [+25.9, +43.6] | 7 | 0.000 | 0.002 | True |
| N4 | sim27 | furious - slightly annoyed (same event) | +31.2 [+23.1, +39.4] | 7 | 0.000 | 0.003 | True |
| N1 | sim28 | event only - calm (the feeling is inferred) | +16.0 [+9.1, +22.9] | 14 | 0.000 | 0.010 | True |
| N2 | sim28 | label only - calm (the feeling without a cause) | +28.5 [+22.2, +34.9] | 14 | 0.000 | 0.000 | True |
| N3 | sim28 | own anger - another person's anger | +21.1 [+11.2, +31.0] | 7 | 0.001 | 0.046 | True |
| N4 | sim28 | furious - slightly annoyed (same event) | +20.7 [+9.0, +32.4] | 7 | 0.002 | 0.087 | False |
| N1 | sim29 | event only - calm (the feeling is inferred) | +20.7 [+12.9, +28.5] | 14 | 0.000 | 0.003 | True |
| N2 | sim29 | label only - calm (the feeling without a cause) | +31.2 [+23.4, +39.1] | 14 | 0.000 | 0.000 | True |
| N3 | sim29 | own anger - another person's anger | +19.9 [+12.4, +27.5] | 7 | 0.000 | 0.018 | True |
| N4 | sim29 | furious - slightly annoyed (same event) | +10.9 [-0.0, +21.9] | 7 | 0.025 | 0.303 | False |
| N1 | sim3 | event only - calm (the feeling is inferred) | +18.8 [+8.3, +29.2] | 14 | 0.001 | 0.051 | False |
| N2 | sim3 | label only - calm (the feeling without a cause) | +17.2 [+6.3, +28.1] | 14 | 0.002 | 0.088 | False |
| N3 | sim3 | own anger - another person's anger | +32.4 [+19.7, +45.1] | 7 | 0.000 | 0.021 | True |
| N4 | sim3 | furious - slightly annoyed (same event) | +25.0 [+13.2, +36.8] | 7 | 0.001 | 0.046 | True |
| N1 | sim30 | event only - calm (the feeling is inferred) | +22.3 [+13.4, +31.1] | 14 | 0.000 | 0.005 | True |
| N2 | sim30 | label only - calm (the feeling without a cause) | +31.6 [+22.4, +40.9] | 14 | 0.000 | 0.000 | True |
| N3 | sim30 | own anger - another person's anger | +21.1 [+8.4, +33.8] | 7 | 0.003 | 0.094 | False |
| N4 | sim30 | furious - slightly annoyed (same event) | +28.9 [+19.8, +38.0] | 7 | 0.000 | 0.007 | True |
| N1 | sim31 | event only - calm (the feeling is inferred) | +5.9 [-4.6, +16.3] | 14 | 0.125 | 0.446 | False |
| N2 | sim31 | label only - calm (the feeling without a cause) | +23.0 [+13.7, +32.4] | 14 | 0.000 | 0.006 | True |
| N3 | sim31 | own anger - another person's anger | +19.9 [+5.7, +34.1] | 7 | 0.006 | 0.132 | False |
| N4 | sim31 | furious - slightly annoyed (same event) | +17.2 [+9.4, +25.0] | 7 | 0.001 | 0.042 | True |
| N1 | sim32 | event only - calm (the feeling is inferred) | +16.8 [+7.6, +26.0] | 14 | 0.001 | 0.046 | True |
| N2 | sim32 | label only - calm (the feeling without a cause) | +26.2 [+20.3, +32.0] | 14 | 0.000 | 0.000 | True |
| N3 | sim32 | own anger - another person's anger | +31.2 [+20.3, +42.2] | 7 | 0.000 | 0.013 | True |
| N4 | sim32 | furious - slightly annoyed (same event) | +28.1 [+20.6, +35.7] | 7 | 0.000 | 0.003 | True |
| N1 | sim33 | event only - calm (the feeling is inferred) | +17.6 [+7.6, +27.5] | 14 | 0.001 | 0.053 | False |
| N2 | sim33 | label only - calm (the feeling without a cause) | +31.2 [+22.0, +40.5] | 14 | 0.000 | 0.000 | True |
| N3 | sim33 | own anger - another person's anger | +29.3 [+17.6, +41.0] | 7 | 0.000 | 0.022 | True |
| N4 | sim33 | furious - slightly annoyed (same event) | +21.9 [+12.2, +31.5] | 7 | 0.001 | 0.037 | True |
| N1 | sim34 | event only - calm (the feeling is inferred) | +30.1 [+21.9, +38.3] | 14 | 0.000 | 0.000 | True |
| N2 | sim34 | label only - calm (the feeling without a cause) | +27.3 [+17.8, +36.9] | 14 | 0.000 | 0.002 | True |
| N3 | sim34 | own anger - another person's anger | +21.1 [-0.5, +42.7] | 7 | 0.027 | 0.303 | False |
| N4 | sim34 | furious - slightly annoyed (same event) | +10.2 [-5.9, +26.2] | 7 | 0.089 | 0.446 | False |
| N1 | sim35 | event only - calm (the feeling is inferred) | +7.8 [-1.1, +16.7] | 14 | 0.040 | 0.364 | False |
| N2 | sim35 | label only - calm (the feeling without a cause) | +14.1 [+6.4, +21.7] | 14 | 0.001 | 0.045 | True |
| N3 | sim35 | own anger - another person's anger | +13.7 [+6.5, +20.8] | 7 | 0.001 | 0.066 | False |
| N4 | sim35 | furious - slightly annoyed (same event) | +27.0 [+18.5, +35.4] | 7 | 0.000 | 0.007 | True |
| N1 | sim36 | event only - calm (the feeling is inferred) | +27.3 [+16.3, +38.4] | 14 | 0.000 | 0.006 | True |
| N2 | sim36 | label only - calm (the feeling without a cause) | +29.7 [+20.8, +38.6] | 14 | 0.000 | 0.000 | True |
| N3 | sim36 | own anger - another person's anger | +18.8 [+5.5, +32.0] | 7 | 0.006 | 0.132 | False |
| N4 | sim36 | furious - slightly annoyed (same event) | +11.7 [-3.4, +26.8] | 7 | 0.055 | 0.395 | False |
| N1 | sim37 | event only - calm (the feeling is inferred) | +25.8 [+13.9, +37.7] | 14 | 0.000 | 0.016 | True |
| N2 | sim37 | label only - calm (the feeling without a cause) | +30.5 [+20.8, +40.1] | 14 | 0.000 | 0.001 | True |
| N3 | sim37 | own anger - another person's anger | +18.0 [+4.3, +31.6] | 7 | 0.009 | 0.140 | False |
| N4 | sim37 | furious - slightly annoyed (same event) | +7.8 [-7.3, +22.9] | 7 | 0.131 | 0.446 | False |
| N1 | sim38 | event only - calm (the feeling is inferred) | +20.3 [+10.2, +30.4] | 14 | 0.000 | 0.027 | True |
| N2 | sim38 | label only - calm (the feeling without a cause) | +16.4 [+5.1, +27.7] | 14 | 0.004 | 0.106 | False |
| N3 | sim38 | own anger - another person's anger | +19.5 [+12.7, +26.4] | 7 | 0.000 | 0.013 | True |
| N4 | sim38 | furious - slightly annoyed (same event) | +13.7 [+4.5, +22.9] | 7 | 0.005 | 0.118 | False |
| N1 | sim39 | event only - calm (the feeling is inferred) | +20.7 [+11.3, +30.1] | 14 | 0.000 | 0.015 | True |
| N2 | sim39 | label only - calm (the feeling without a cause) | +28.1 [+17.3, +38.9] | 14 | 0.000 | 0.004 | True |
| N3 | sim39 | own anger - another person's anger | +18.7 [+13.1, +24.4] | 7 | 0.000 | 0.005 | True |
| N4 | sim39 | furious - slightly annoyed (same event) | +18.0 [+5.3, +30.6] | 7 | 0.006 | 0.132 | False |
| N1 | sim4 | event only - calm (the feeling is inferred) | +26.6 [+18.0, +35.1] | 14 | 0.000 | 0.001 | True |
| N2 | sim4 | label only - calm (the feeling without a cause) | +26.6 [+19.4, +33.7] | 14 | 0.000 | 0.000 | True |
| N3 | sim4 | own anger - another person's anger | +30.9 [+19.6, +42.1] | 7 | 0.000 | 0.015 | True |
| N4 | sim4 | furious - slightly annoyed (same event) | +21.5 [+9.5, +33.4] | 7 | 0.002 | 0.084 | False |
| N1 | sim5 | event only - calm (the feeling is inferred) | +18.4 [+6.8, +29.9] | 14 | 0.002 | 0.088 | False |
| N2 | sim5 | label only - calm (the feeling without a cause) | +25.4 [+16.8, +34.0] | 14 | 0.000 | 0.001 | True |
| N3 | sim5 | own anger - another person's anger | +39.1 [+32.3, +45.8] | 7 | 0.000 | 0.000 | True |
| N4 | sim5 | furious - slightly annoyed (same event) | +17.2 [+7.3, +27.1] | 7 | 0.002 | 0.088 | False |
| N1 | sim6 | event only - calm (the feeling is inferred) | +20.3 [+8.6, +32.0] | 14 | 0.001 | 0.057 | False |
| N2 | sim6 | label only - calm (the feeling without a cause) | +21.9 [+11.4, +32.4] | 14 | 0.000 | 0.021 | True |
| N3 | sim6 | own anger - another person's anger | +19.9 [+10.7, +29.1] | 7 | 0.001 | 0.044 | True |
| N4 | sim6 | furious - slightly annoyed (same event) | +20.3 [+11.8, +28.9] | 7 | 0.000 | 0.030 | True |
| N1 | sim7 | event only - calm (the feeling is inferred) | +22.7 [+14.5, +30.8] | 14 | 0.000 | 0.002 | True |
| N2 | sim7 | label only - calm (the feeling without a cause) | +16.0 [+7.4, +24.6] | 14 | 0.001 | 0.043 | True |
| N3 | sim7 | own anger - another person's anger | +24.2 [+17.4, +31.1] | 7 | 0.000 | 0.004 | True |
| N4 | sim7 | furious - slightly annoyed (same event) | +25.4 [+12.6, +38.1] | 7 | 0.001 | 0.056 | False |
| N1 | sim8 | event only - calm (the feeling is inferred) | +17.6 [+8.2, +26.9] | 14 | 0.001 | 0.041 | True |
| N2 | sim8 | label only - calm (the feeling without a cause) | +32.0 [+24.5, +39.6] | 14 | 0.000 | 0.000 | True |
| N3 | sim8 | own anger - another person's anger | +30.1 [+21.8, +38.4] | 7 | 0.000 | 0.003 | True |
| N4 | sim8 | furious - slightly annoyed (same event) | +30.1 [+21.5, +38.6] | 7 | 0.000 | 0.004 | True |
| N1 | sim9 | event only - calm (the feeling is inferred) | +25.8 [+14.4, +37.1] | 14 | 0.000 | 0.012 | True |
| N2 | sim9 | label only - calm (the feeling without a cause) | +36.3 [+28.3, +44.3] | 14 | 0.000 | 0.000 | True |
| N3 | sim9 | own anger - another person's anger | +23.0 [+14.5, +31.6] | 7 | 0.000 | 0.016 | True |
| N4 | sim9 | furious - slightly annoyed (same event) | +20.3 [+11.3, +29.3] | 7 | 0.001 | 0.038 | True |

Rejection (%) by condition:

| model | calm | event_only | full | label_only | mild | other_person |
|---|---|---|---|---|---|---|
| sim0 | 35.900 | 59.000 | 63.300 | 61.700 | 42.600 | 34.000 |
| sim1 | 35.900 | 59.000 | 55.500 | 58.600 | 47.700 | 44.100 |
| sim10 | 39.100 | 46.500 | 68.400 | 60.500 | 46.900 | 45.300 |
| sim11 | 34.400 | 52.300 | 68.000 | 52.000 | 50.400 | 44.900 |
| sim12 | 41.000 | 52.700 | 60.900 | 60.500 | 44.500 | 46.900 |
| sim13 | 35.500 | 53.900 | 68.800 | 52.700 | 41.400 | 37.500 |
| sim14 | 36.700 | 55.900 | 73.000 | 61.700 | 41.400 | 37.100 |
| sim15 | 32.400 | 50.800 | 66.000 | 65.200 | 50.000 | 43.400 |
| sim16 | 32.400 | 59.800 | 52.700 | 53.900 | 38.700 | 31.200 |
| sim17 | 35.200 | 60.200 | 61.300 | 68.400 | 47.300 | 37.900 |
| sim18 | 35.200 | 57.000 | 75.000 | 59.000 | 43.000 | 41.000 |
| sim19 | 37.900 | 49.600 | 71.100 | 59.000 | 39.800 | 35.200 |
| sim2 | 29.300 | 64.800 | 71.100 | 63.300 | 54.300 | 43.800 |
| sim20 | 38.700 | 57.800 | 59.800 | 64.500 | 49.200 | 31.600 |
| sim21 | 33.600 | 49.600 | 69.500 | 61.300 | 43.400 | 37.500 |
| sim22 | 34.800 | 53.100 | 60.200 | 58.200 | 52.700 | 35.500 |
| sim23 | 31.600 | 53.900 | 74.600 | 65.600 | 35.500 | 39.100 |
| sim24 | 43.000 | 54.700 | 62.100 | 59.400 | 49.200 | 41.400 |
| sim25 | 32.800 | 57.400 | 68.000 | 60.200 | 41.400 | 49.600 |
| sim26 | 33.600 | 48.000 | 68.400 | 58.600 | 45.700 | 34.400 |
| sim27 | 43.400 | 41.400 | 73.000 | 60.200 | 41.800 | 38.300 |
| sim28 | 38.300 | 54.300 | 64.100 | 66.800 | 43.400 | 43.000 |
| sim29 | 30.500 | 51.200 | 61.700 | 61.700 | 50.800 | 41.800 |
| sim3 | 36.700 | 55.500 | 64.800 | 53.900 | 39.800 | 32.400 |
| sim30 | 37.100 | 59.400 | 64.500 | 68.800 | 35.500 | 43.400 |
| sim31 | 40.600 | 46.500 | 58.600 | 63.700 | 41.400 | 38.700 |
| sim32 | 35.200 | 52.000 | 69.100 | 61.300 | 41.000 | 37.900 |
| sim33 | 37.100 | 54.700 | 66.800 | 68.400 | 44.900 | 37.500 |
| sim34 | 34.000 | 64.100 | 59.800 | 61.300 | 49.600 | 38.700 |
| sim35 | 36.300 | 44.100 | 59.400 | 50.400 | 32.400 | 45.700 |
| sim36 | 33.200 | 60.500 | 66.400 | 62.900 | 54.700 | 47.700 |
| sim37 | 35.900 | 61.700 | 54.300 | 66.400 | 46.500 | 36.300 |
| sim38 | 38.300 | 58.600 | 62.100 | 54.700 | 48.400 | 42.600 |
| sim39 | 33.200 | 53.900 | 62.500 | 61.300 | 44.500 | 43.800 |
| sim4 | 25.800 | 52.300 | 63.300 | 52.300 | 41.800 | 32.400 |
| sim5 | 31.600 | 50.000 | 67.600 | 57.000 | 50.400 | 28.500 |
| sim6 | 34.000 | 54.300 | 62.100 | 55.900 | 41.800 | 42.200 |
| sim7 | 33.200 | 55.900 | 65.200 | 49.200 | 39.800 | 41.000 |
| sim8 | 34.000 | 51.600 | 69.100 | 66.000 | 39.100 | 39.100 |
| sim9 | 32.000 | 57.800 | 68.000 | 68.400 | 47.700 | 44.900 |

Exploratory (two-sided):

| model | test | estimate [95% CI] | p |
|---|---|---|---|
| sim0 | full - calm (replication) | +27.3 [+21.1, +33.6] | 0.000 |
| sim0 | mild - calm | +6.6 [-1.9, +15.2] | 0.117 |
| sim0 | another person's anger - calm | -2.0 [-9.4, +5.5] | 0.582 |
| sim0 | full - event only (what the stated feeling adds) | +4.3 [-2.4, +11.0] | 0.175 |
| sim1 | full - calm (replication) | +19.5 [+10.5, +28.6] | 0.000 |
| sim1 | mild - calm | +11.7 [+1.9, +21.5] | 0.023 |
| sim1 | another person's anger - calm | +8.2 [-0.7, +17.1] | 0.068 |
| sim1 | full - event only (what the stated feeling adds) | -3.5 [-12.2, +5.2] | 0.372 |
| sim10 | full - calm (replication) | +29.3 [+20.6, +38.0] | 0.000 |
| sim10 | mild - calm | +7.8 [-1.2, +16.9] | 0.085 |
| sim10 | another person's anger - calm | +6.2 [-3.7, +16.2] | 0.198 |
| sim10 | full - event only (what the stated feeling adds) | +21.9 [+10.5, +33.2] | 0.003 |
| sim11 | full - calm (replication) | +33.6 [+21.1, +46.1] | 0.000 |
| sim11 | mild - calm | +16.0 [+1.5, +30.6] | 0.033 |
| sim11 | another person's anger - calm | +10.5 [-1.6, +22.7] | 0.084 |
| sim11 | full - event only (what the stated feeling adds) | +15.6 [+6.5, +24.7] | 0.005 |
| sim12 | full - calm (replication) | +19.9 [+12.3, +27.6] | 0.000 |
| sim12 | mild - calm | +3.5 [-4.0, +11.0] | 0.332 |
| sim12 | another person's anger - calm | +5.9 [-1.0, +12.8] | 0.090 |
| sim12 | full - event only (what the stated feeling adds) | +8.2 [-0.9, +17.3] | 0.070 |
| sim13 | full - calm (replication) | +33.2 [+22.0, +44.4] | 0.000 |
| sim13 | mild - calm | +5.9 [-4.5, +16.2] | 0.245 |
| sim13 | another person's anger - calm | +2.0 [-7.0, +10.9] | 0.647 |
| sim13 | full - event only (what the stated feeling adds) | +14.8 [+3.6, +26.1] | 0.017 |
| sim14 | full - calm (replication) | +36.3 [+28.4, +44.3] | 0.000 |
| sim14 | mild - calm | +4.7 [-2.3, +11.7] | 0.174 |
| sim14 | another person's anger - calm | +0.4 [-9.4, +10.2] | 0.933 |
| sim14 | full - event only (what the stated feeling adds) | +17.2 [+9.5, +24.9] | 0.001 |
| sim15 | full - calm (replication) | +33.6 [+24.2, +43.0] | 0.000 |
| sim15 | mild - calm | +17.6 [+5.6, +29.6] | 0.007 |
| sim15 | another person's anger - calm | +10.9 [-0.4, +22.3] | 0.058 |
| sim15 | full - event only (what the stated feeling adds) | +15.2 [+2.2, +28.2] | 0.028 |
| sim16 | full - calm (replication) | +20.3 [+15.2, +25.4] | 0.000 |
| sim16 | mild - calm | +6.2 [+0.9, +11.6] | 0.025 |
| sim16 | another person's anger - calm | -1.2 [-8.9, +6.5] | 0.748 |
| sim16 | full - event only (what the stated feeling adds) | -7.0 [-19.1, +5.0] | 0.211 |
| sim17 | full - calm (replication) | +26.2 [+16.0, +36.3] | 0.000 |
| sim17 | mild - calm | +12.1 [+1.1, +23.1] | 0.034 |
| sim17 | another person's anger - calm | +2.7 [-7.6, +13.0] | 0.579 |
| sim17 | full - event only (what the stated feeling adds) | +1.2 [-8.1, +10.5] | 0.775 |
| sim18 | full - calm (replication) | +39.8 [+31.9, +47.8] | 0.000 |
| sim18 | mild - calm | +7.8 [+0.4, +15.2] | 0.041 |
| sim18 | another person's anger - calm | +5.9 [-3.7, +15.4] | 0.209 |
| sim18 | full - event only (what the stated feeling adds) | +18.0 [+10.1, +25.9] | 0.001 |
| sim19 | full - calm (replication) | +33.2 [+24.5, +41.9] | 0.000 |
| sim19 | mild - calm | +2.0 [-7.2, +11.1] | 0.654 |
| sim19 | another person's anger - calm | -2.7 [-12.9, +7.4] | 0.573 |
| sim19 | full - event only (what the stated feeling adds) | +21.5 [+13.6, +29.4] | 0.000 |
| sim2 | full - calm (replication) | +41.8 [+32.0, +51.6] | 0.000 |
| sim2 | mild - calm | +25.0 [+17.2, +32.8] | 0.000 |
| sim2 | another person's anger - calm | +14.5 [+3.7, +25.2] | 0.012 |
| sim2 | full - event only (what the stated feeling adds) | +6.3 [-8.9, +21.4] | 0.363 |
| sim20 | full - calm (replication) | +21.1 [+9.8, +32.4] | 0.001 |
| sim20 | mild - calm | +10.5 [+0.8, +20.3] | 0.036 |
| sim20 | another person's anger - calm | -7.0 [-17.1, +3.1] | 0.158 |
| sim20 | full - event only (what the stated feeling adds) | +2.0 [-9.2, +13.1] | 0.691 |
| sim21 | full - calm (replication) | +35.9 [+23.7, +48.2] | 0.000 |
| sim21 | mild - calm | +9.8 [-1.7, +21.3] | 0.090 |
| sim21 | another person's anger - calm | +3.9 [-7.7, +15.5] | 0.482 |
| sim21 | full - event only (what the stated feeling adds) | +19.9 [+11.4, +28.5] | 0.001 |
| sim22 | full - calm (replication) | +25.4 [+11.0, +39.8] | 0.002 |
| sim22 | mild - calm | +18.0 [+4.3, +31.7] | 0.014 |
| sim22 | another person's anger - calm | +0.8 [-12.5, +14.1] | 0.901 |
| sim22 | full - event only (what the stated feeling adds) | +7.0 [-5.0, +19.1] | 0.211 |
| sim23 | full - calm (replication) | +43.0 [+35.0, +50.9] | 0.000 |
| sim23 | mild - calm | +3.9 [-6.6, +14.4] | 0.437 |
| sim23 | another person's anger - calm | +7.4 [-1.2, +16.1] | 0.087 |
| sim23 | full - event only (what the stated feeling adds) | +20.7 [+14.0, +27.4] | 0.000 |
| sim24 | full - calm (replication) | +19.1 [+9.8, +28.4] | 0.001 |
| sim24 | mild - calm | +6.2 [-2.1, +14.6] | 0.133 |
| sim24 | another person's anger - calm | -1.6 [-9.4, +6.3] | 0.675 |
| sim24 | full - event only (what the stated feeling adds) | +7.4 [-3.9, +18.7] | 0.165 |
| sim25 | full - calm (replication) | +35.2 [+26.0, +44.3] | 0.000 |
| sim25 | mild - calm | +8.6 [-1.8, +19.0] | 0.099 |
| sim25 | another person's anger - calm | +16.8 [+7.5, +26.1] | 0.002 |
| sim25 | full - event only (what the stated feeling adds) | +10.5 [+2.5, +18.6] | 0.017 |
| sim26 | full - calm (replication) | +34.8 [+23.6, +45.9] | 0.000 |
| sim26 | mild - calm | +12.1 [+4.6, +19.7] | 0.004 |
| sim26 | another person's anger - calm | +0.8 [-6.9, +8.4] | 0.830 |
| sim26 | full - event only (what the stated feeling adds) | +20.3 [+8.0, +32.6] | 0.006 |
| sim27 | full - calm (replication) | +29.7 [+22.5, +36.9] | 0.000 |
| sim27 | mild - calm | -1.6 [-11.1, +8.0] | 0.731 |
| sim27 | another person's anger - calm | -5.1 [-15.4, +5.2] | 0.309 |
| sim27 | full - event only (what the stated feeling adds) | +31.6 [+25.9, +37.3] | 0.000 |
| sim28 | full - calm (replication) | +25.8 [+18.4, +33.1] | 0.000 |
| sim28 | mild - calm | +5.1 [-5.9, +16.1] | 0.340 |
| sim28 | another person's anger - calm | +4.7 [-3.3, +12.7] | 0.231 |
| sim28 | full - event only (what the stated feeling adds) | +9.8 [+1.5, +18.0] | 0.026 |
| sim29 | full - calm (replication) | +31.2 [+22.2, +40.3] | 0.000 |
| sim29 | mild - calm | +20.3 [+8.9, +31.8] | 0.002 |
| sim29 | another person's anger - calm | +11.3 [+1.7, +20.9] | 0.024 |
| sim29 | full - event only (what the stated feeling adds) | +10.5 [+1.0, +20.1] | 0.034 |
| sim3 | full - calm (replication) | +28.1 [+16.5, +39.8] | 0.000 |
| sim3 | mild - calm | +3.1 [-6.8, +13.1] | 0.512 |
| sim3 | another person's anger - calm | -4.3 [-15.3, +6.7] | 0.416 |
| sim3 | full - event only (what the stated feeling adds) | +9.4 [+1.8, +16.9] | 0.022 |
| sim30 | full - calm (replication) | +27.3 [+19.0, +35.7] | 0.000 |
| sim30 | mild - calm | -1.6 [-9.3, +6.2] | 0.671 |
| sim30 | another person's anger - calm | +6.2 [-3.0, +15.5] | 0.171 |
| sim30 | full - event only (what the stated feeling adds) | +5.1 [-4.9, +15.1] | 0.270 |
| sim31 | full - calm (replication) | +18.0 [+7.5, +28.4] | 0.002 |
| sim31 | mild - calm | +0.8 [-11.3, +12.9] | 0.892 |
| sim31 | another person's anger - calm | -2.0 [-15.0, +11.1] | 0.754 |
| sim31 | full - event only (what the stated feeling adds) | +12.1 [-3.0, +27.3] | 0.101 |
| sim32 | full - calm (replication) | +34.0 [+25.7, +42.3] | 0.000 |
| sim32 | mild - calm | +5.9 [-0.8, +12.5] | 0.080 |
| sim32 | another person's anger - calm | +2.7 [-8.0, +13.5] | 0.594 |
| sim32 | full - event only (what the stated feeling adds) | +17.2 [+2.7, +31.7] | 0.027 |
| sim33 | full - calm (replication) | +29.7 [+20.7, +38.7] | 0.000 |
| sim33 | mild - calm | +7.8 [+0.7, +14.9] | 0.034 |
| sim33 | another person's anger - calm | +0.4 [-8.9, +9.6] | 0.929 |
| sim33 | full - event only (what the stated feeling adds) | +12.1 [-1.5, +25.7] | 0.073 |
| sim34 | full - calm (replication) | +25.8 [+15.6, +36.0] | 0.000 |
| sim34 | mild - calm | +15.6 [+6.8, +24.5] | 0.002 |
| sim34 | another person's anger - calm | +4.7 [-7.1, +16.5] | 0.407 |
| sim34 | full - event only (what the stated feeling adds) | -4.3 [-20.7, +12.1] | 0.556 |
| sim35 | full - calm (replication) | +23.0 [+13.8, +32.3] | 0.000 |
| sim35 | mild - calm | -3.9 [-11.4, +3.6] | 0.281 |
| sim35 | another person's anger - calm | +9.4 [+0.1, +18.7] | 0.048 |
| sim35 | full - event only (what the stated feeling adds) | +15.2 [+2.7, +27.8] | 0.024 |
| sim36 | full - calm (replication) | +33.2 [+22.9, +43.5] | 0.000 |
| sim36 | mild - calm | +21.5 [+10.8, +32.1] | 0.001 |
| sim36 | another person's anger - calm | +14.5 [+5.2, +23.7] | 0.005 |
| sim36 | full - event only (what the stated feeling adds) | +5.9 [-8.8, +20.6] | 0.377 |
| sim37 | full - calm (replication) | +18.4 [+7.6, +29.2] | 0.003 |
| sim37 | mild - calm | +10.5 [-1.3, +22.4] | 0.077 |
| sim37 | another person's anger - calm | +0.4 [-12.3, +13.1] | 0.948 |
| sim37 | full - event only (what the stated feeling adds) | -7.4 [-22.9, +8.1] | 0.295 |
| sim38 | full - calm (replication) | +23.8 [+14.4, +33.3] | 0.000 |
| sim38 | mild - calm | +10.2 [+1.3, +19.0] | 0.028 |
| sim38 | another person's anger - calm | +4.3 [-5.2, +13.8] | 0.349 |
| sim38 | full - event only (what the stated feeling adds) | +3.5 [-8.8, +15.9] | 0.523 |
| sim39 | full - calm (replication) | +29.3 [+20.1, +38.5] | 0.000 |
| sim39 | mild - calm | +11.3 [+0.9, +21.8] | 0.035 |
| sim39 | another person's anger - calm | +10.5 [+1.2, +19.9] | 0.030 |
| sim39 | full - event only (what the stated feeling adds) | +8.6 [+3.2, +14.0] | 0.007 |
| sim4 | full - calm (replication) | +37.5 [+31.7, +43.3] | 0.000 |
| sim4 | mild - calm | +16.0 [+8.0, +24.1] | 0.001 |
| sim4 | another person's anger - calm | +6.6 [-0.8, +14.1] | 0.077 |
| sim4 | full - event only (what the stated feeling adds) | +10.9 [+2.1, +19.8] | 0.023 |
| sim5 | full - calm (replication) | +35.9 [+28.5, +43.4] | 0.000 |
| sim5 | mild - calm | +18.7 [+9.9, +27.6] | 0.000 |
| sim5 | another person's anger - calm | -3.1 [-10.1, +3.8] | 0.351 |
| sim5 | full - event only (what the stated feeling adds) | +17.6 [+2.5, +32.6] | 0.028 |
| sim6 | full - calm (replication) | +28.1 [+18.0, +38.3] | 0.000 |
| sim6 | mild - calm | +7.8 [-1.2, +16.8] | 0.084 |
| sim6 | another person's anger - calm | +8.2 [-0.9, +17.3] | 0.073 |
| sim6 | full - event only (what the stated feeling adds) | +7.8 [-5.4, +21.0] | 0.204 |
| sim7 | full - calm (replication) | +32.0 [+25.4, +38.7] | 0.000 |
| sim7 | mild - calm | +6.6 [-2.7, +16.0] | 0.150 |
| sim7 | another person's anger - calm | +7.8 [+1.9, +13.8] | 0.014 |
| sim7 | full - event only (what the stated feeling adds) | +9.4 [+1.7, +17.1] | 0.024 |
| sim8 | full - calm (replication) | +35.2 [+27.3, +43.0] | 0.000 |
| sim8 | mild - calm | +5.1 [-2.2, +12.4] | 0.159 |
| sim8 | another person's anger - calm | +5.1 [-3.9, +14.1] | 0.246 |
| sim8 | full - event only (what the stated feeling adds) | +17.6 [+7.1, +28.1] | 0.005 |
| sim9 | full - calm (replication) | +35.9 [+28.4, +43.5] | 0.000 |
| sim9 | mild - calm | +15.6 [+6.1, +25.1] | 0.003 |
| sim9 | another person's anger - calm | +12.9 [+4.2, +21.6] | 0.007 |
| sim9 | full - event only (what the stated feeling adds) | +10.2 [-2.4, +22.7] | 0.097 |

Mood check: share answering "angry":

No data.
