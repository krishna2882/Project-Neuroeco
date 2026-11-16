# Extension 6: probing and steering (DEVELOPMENT RUN, not analysed)

Design: `docs/preregistration_extension6.md`. Estimates in percentage points (steering: change per unit of steering strength k; k = 1 adds the mean angry - neutral difference once). p = rank of the anger direction among random directions of the same norm (one-sided); Holm over M1-M3 within a model.

## Confirmatory tests

| id | game | test | est | null_mean | null_lo | null_hi | p | n_random | k_used | baseline | at_max_k | unablated | valid_anger | model | p_holm | supported |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| M1 | S3b | anger direction lowers share sent | 3.716 | 0.848 | -2.197 | 4.681 | 0.800 | 4 | [1.0, 2.0, 4.0] | 27.656 | 41.625 |  |  | dev_qwen25_05b | 1.000 | False |
| M2 | S1 | anger direction raises P(reject) | -1.273 | -1.872 | -6.124 | 2.381 | 0.600 | 4 | [1.0, 2.0, 4.0] | 87.549 | 82.633 |  |  | dev_qwen25_05b | 1.000 | False |
| M3 | S3b | ablating the anger direction shrinks the anger effect | -4.631 | 2.536 | 1.023 | 4.052 | 0.200 | 4 |  |  |  | 2.956 | 0.938 | dev_qwen25_05b | 0.600 | False |

## Does the Hugging Face model show the behavioural effects? (unsteered)

| game | contrast | est | lo | hi | p | baseline | model |
|---|---|---|---|---|---|---|---|
| S3b | angry - neutral message | -0.728 | -5.916 | 4.460 | 0.771 | 22.941 | dev_qwen25_05b |
| S3b | angry - calm mood | 0.219 | -2.165 | 2.603 | 0.846 | 21.672 | dev_qwen25_05b |

## Other directions at the steering layer (exploratory)

| game | direction | slope_pp_per_k | p_two_sided | model |
|---|---|---|---|---|
| S3b | sad | 3.109 | 0.800 | dev_qwen25_05b |
| S3b | happy | 0.661 | 1.000 | dev_qwen25_05b |
| S3b | own_anger | 1.315 | 0.800 | dev_qwen25_05b |
| S1 | sad | 1.316 | 0.800 | dev_qwen25_05b |
| S1 | happy | -0.649 | 0.800 | dev_qwen25_05b |
| S1 | own_anger | -3.282 | 0.800 | dev_qwen25_05b |

## Layer sweep (exploratory): steering slope of each layer's anger direction vs 10 random directions

| model | layer | game | anger_slope | random_min | random_max | valid |
|---|---|---|---|---|---|---|
| dev_qwen25_05b | 2 | S1 | 0.286 | 0.079 | 0.079 | 0.999 |
| dev_qwen25_05b | 2 | S3b | 0.008 | 0.179 | 0.179 | 1.000 |
| dev_qwen25_05b | 4 | S1 | 0.876 | -0.507 | -0.507 | 0.999 |
| dev_qwen25_05b | 4 | S3b | -0.228 | 0.091 | 0.091 | 1.000 |
| dev_qwen25_05b | 6 | S1 | 0.227 | 0.631 | 0.631 | 0.999 |
| dev_qwen25_05b | 6 | S3b | -0.402 | -0.731 | -0.731 | 1.000 |
| dev_qwen25_05b | 8 | S1 | -1.053 | 1.129 | 1.129 | 0.999 |
| dev_qwen25_05b | 8 | S3b | 1.009 | -0.321 | -0.321 | 1.000 |
| dev_qwen25_05b | 10 | S1 | -1.082 | 2.109 | 2.109 | 0.998 |
| dev_qwen25_05b | 10 | S3b | 2.321 | 1.197 | 1.197 | 1.000 |
| dev_qwen25_05b | 12 | S1 | -1.273 | -4.470 | -4.470 | 0.998 |
| dev_qwen25_05b | 12 | S3b | 3.716 | 0.586 | 0.586 | 1.000 |
| dev_qwen25_05b | 14 | S1 | 0.899 | -10.468 | -10.468 | 0.998 |
| dev_qwen25_05b | 14 | S3b | -0.856 | -4.913 | -4.913 | 1.000 |
| dev_qwen25_05b | 16 | S1 | 2.373 | -5.282 | -5.282 | 0.998 |
| dev_qwen25_05b | 16 | S3b | -6.419 | 7.311 | 7.311 | 1.000 |
| dev_qwen25_05b | 18 | S1 | -9.704 | -8.247 | -8.247 | 0.995 |
| dev_qwen25_05b | 18 | S3b | -3.669 | -0.104 | -0.104 | 1.000 |
| dev_qwen25_05b | 20 | S1 | -7.319 | -14.712 | -14.712 | 0.996 |
| dev_qwen25_05b | 20 | S3b | -2.707 | -1.494 | -1.494 | 1.000 |
| dev_qwen25_05b | 22 | S1 | 2.189 | -2.772 | -2.772 | 0.996 |
| dev_qwen25_05b | 22 | S3b | -1.689 | 0.097 | 0.097 | 1.000 |
| dev_qwen25_05b | 24 | S1 | 2.042 | -20.328 | -20.328 | 0.769 |
| dev_qwen25_05b | 24 | S3b | -7.387 | 2.882 | 2.882 | 0.760 |

## Probes by layer

| layer | acc_emotion4 | acc_shuffled | transfer_msg_to_mood_auc | transfer_mood_to_msg_auc | cos_msg_mood | norm_anger_dir | norm_resid | model | steer_layer |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 0.250 | 0.108 | 0.500 | 0.500 | 0.000 | 0.000 | 0.604 | dev_qwen25_05b | 12 |
| 1 | 0.638 | 0.196 | 0.484 | 0.555 | 0.511 | 0.021 | 3.564 | dev_qwen25_05b | 12 |
| 2 | 0.675 | 0.183 | 0.730 | 0.752 | 0.597 | 0.036 | 6.731 | dev_qwen25_05b | 12 |
| 3 | 0.662 | 0.173 | 0.708 | 0.791 | 0.575 | 0.050 | 8.127 | dev_qwen25_05b | 12 |
| 4 | 0.762 | 0.294 | 0.813 | 0.902 | 0.566 | 0.073 | 9.515 | dev_qwen25_05b | 12 |
| 5 | 0.762 | 0.215 | 0.925 | 0.881 | 0.598 | 0.091 | 9.660 | dev_qwen25_05b | 12 |
| 6 | 0.794 | 0.300 | 0.910 | 0.934 | 0.603 | 0.097 | 10.250 | dev_qwen25_05b | 12 |
| 7 | 0.750 | 0.221 | 0.879 | 0.967 | 0.496 | 0.110 | 10.893 | dev_qwen25_05b | 12 |
| 8 | 0.781 | 0.146 | 0.981 | 0.838 | 0.349 | 0.132 | 12.266 | dev_qwen25_05b | 12 |
| 9 | 0.725 | 0.244 | 0.896 | 0.694 | 0.262 | 0.186 | 12.393 | dev_qwen25_05b | 12 |
| 10 | 0.762 | 0.242 | 0.823 | 0.682 | 0.327 | 0.207 | 12.090 | dev_qwen25_05b | 12 |
| 11 | 0.856 | 0.181 | 0.826 | 0.736 | 0.363 | 0.310 | 13.072 | dev_qwen25_05b | 12 |
| 12 | 0.906 | 0.233 | 0.842 | 0.884 | 0.333 | 0.492 | 14.647 | dev_qwen25_05b | 12 |
| 13 | 0.912 | 0.242 | 0.869 | 0.631 | 0.093 | 0.819 | 15.137 | dev_qwen25_05b | 12 |
| 14 | 0.869 | 0.296 | 0.843 | 0.745 | 0.087 | 0.912 | 14.255 | dev_qwen25_05b | 12 |
| 15 | 0.988 | 0.256 | 1.000 | 0.978 | 0.581 | 2.188 | 15.419 | dev_qwen25_05b | 12 |
| 16 | 0.975 | 0.215 | 1.000 | 0.958 | 0.686 | 2.872 | 18.525 | dev_qwen25_05b | 12 |
| 17 | 0.938 | 0.246 | 0.998 | 0.903 | 0.632 | 3.586 | 19.709 | dev_qwen25_05b | 12 |
| 18 | 0.969 | 0.212 | 0.994 | 0.906 | 0.628 | 4.087 | 24.714 | dev_qwen25_05b | 12 |
| 19 | 0.950 | 0.223 | 0.993 | 0.826 | 0.642 | 4.637 | 29.598 | dev_qwen25_05b | 12 |
| 20 | 0.956 | 0.237 | 0.974 | 0.769 | 0.604 | 5.083 | 33.551 | dev_qwen25_05b | 12 |
| 21 | 0.962 | 0.206 | 0.990 | 0.786 | 0.570 | 5.412 | 45.009 | dev_qwen25_05b | 12 |
| 22 | 0.962 | 0.235 | 0.966 | 0.777 | 0.582 | 5.956 | 60.182 | dev_qwen25_05b | 12 |
| 23 | 0.938 | 0.185 | 0.964 | 0.798 | 0.564 | 6.955 | 67.305 | dev_qwen25_05b | 12 |
| 24 | 0.925 | 0.267 | 0.981 | 0.868 | 0.436 | 27.063 | 184.574 | dev_qwen25_05b | 12 |
