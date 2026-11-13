# Plan update and deviations from the approach paper (28 Oct 2026)

The design (cells, stimuli, sampling depth, analyses) is unchanged from `Team_10-1.pdf`. What changed is
**where** and **with which models** it runs, plus one parser correction. All changes are reported in the
write-up as deviations.

| # | Paper / earlier plan | Now | Why |
|---|---|---|---|
| P1 | Local model on a laptop (`llama.cpp`) | **Llama-3.1-8B-Instruct Q4_K_M via Ollama v0.40.11 on the IIIT-H Ada cluster** (GTX 1080 Ti, the whole model on the GPU). The run was submitted from the gateway; see `ada/`. | On the laptop (GTX 1650 4 GB, only 16/33 layers on the GPU, CPU shared with other work) a call took 40–90 s, about 70 h for the run. On Ada it ran at 57–140 calls/min. |
| P2 | Closed API model: Gemini, then Groq `gpt-oss-120b` | xAI Grok planned (client in `run/clients.py`), then replaced: see P8 | The xAI key is valid, but the team has no credits. |
| P3 | Two models (1 open + 1 closed) | **Three models:** Llama-3.1-8B (Meta) + **Qwen2.5-7B-Instruct** (Alibaba; second open-weight family, same runtime and quantisation) + Mistral Large 4 (API; see P8) | Lets H5 (cross-model robustness) be tested now without waiting on the API key. Each model gets the identical scenario bank. Model enters H5 as a fixed factor. |
| P4 | Temperature 0.7 robustness "if time allows" | **Run for S1 on both open models** (tag `temp07`, 2,400 calls per model) | Cheap on Ada. |
| P5 | Graded DV from logprobs only if the pilot shows ceiling/floor | Logprobs are **collected for all S1 trials** regardless; the D11 rule still decides whether the 5%/45% cells are added | Costs nothing extra on Ada, and the Llama discrete curve turned out flat, so the graded DV was needed. |
| P6 | — | **Parser correction:** the first Llama S1 run read P(accept) from the token *before* the decision word. Those values are discarded (`analysis/common.py`). S1 was re-run with the same prompts and seeds under tag `main_lp`, with the corrected parser and the raw decision-token alternatives saved. The decisions reproduced 100%. | Bug fix, disclosed. |
| P8 | Closed API model (xAI Grok) | **Mistral Large 4** (`mistral-large-4-0`, ~1T-parameter MoE; weights published 29 Oct 2026, so open-weight but API-only in practice) via Mistral's free tier, `reasoning_effort="low"` | The xAI account has no credits (HTTP 403). On Mistral's free tier the closed models (Medium, Small) are at 0 requests/min, and no free option gives a closed model. Large 4 **always reasons** (≈ 650–1,450 hidden thinking tokens per call; it can't be turned off). H5 contrasts therefore bundle family, scale **and** deliberate reasoning, and are reported that way. Thinking text is logged per call (`thinking`) for the qualitative analysis. No logprobs. |
| P9 | Manipulation checks on ~400 calls per model | Mistral: **106 of 468** checks valid; Mistral's free budget ran out ("API budget exhausted", HTTP 402) during the checks, after all 6,240 decisions had completed | Free-tier quota. Every condition is still represented (n = 14–30 per emotion), and recognition is 100%. The runner can fill in the rest after the quota resets (same command; only missing trials run). |
| P10 | Fallback cells only if the pilot shows ceiling | Mistral's pilot hit ceiling (P(reject \| 10%) = 0), so the 5%/45% S1 cells (+960 trials, +72 checks) were run for **all three** models (Ada jobs 56379/56380 for Llama/Qwen) | D11: apply the fallback to every model to keep the designs identical. |
| P11 | — | **Pre-registered follow-up** with event-free messages (Llama, Qwen; 7,680 decisions), frozen and pushed to GitHub before data collection (12 Nov) | Tests the emotion vs life-event confound. F2 (anger → less trust) replicated; F1 (sadness → less rejection) did not. Mistral not run (budget). |
| P12 | Random intercept per prompt variant (variant_id = paraphrase × message) | **Added analysis (12 Nov):** every emotion test refitted with message as a random factor: `+ C(paraphrase) + (1\|message) + (1\|message:paraphrase)`, t-tests with df = #messages − #emotions (`analysis/message_re.py`, `results/*/message_re.md`) | Emotion varies *between* messages (5 per emotion), so message is the unit of generalisation. Holm survivors 5 → 4 (Mistral DG sad/angry, S3a happy/sad); Qwen S3b angry and Mistral S3a angry drop to FDR-only. Confirmatory F1/F2 unchanged (F2 Holm p = .003). The original models are kept as reported; this is the more conservative analysis. |
| P13 | Pre-registration: both authors approve before any follow-up data are collected | Frozen and pushed with Krishna's approval; follow-up data collected; Devansh signed off afterwards (12 Nov 2026) on the unchanged document | Disclosed as a procedural deviation. The hypotheses, analysis plan and decision rules were fixed and public (commit 3e61f16) before data collection, so the confirmatory tests are unaffected, but the two-author rule was not met in time. |
| P14 | Significance tests only | **Added analysis (12 Nov):** equivalence tests (TOST) for every emotion effect, and a pooled main + follow-up estimate (10 messages per emotion) for Llama/Qwen (`analysis/equivalence.py`, `results/main/equivalence.md`) | Distinguishes "no effect" from "too noisy to tell". The smallest effects of interest (±5 pp / OR 1.5; lenient ±10 pp / OR 2) were chosen after the results were known, so both are reported. Secondary analysis, not pre-registered. |
| P15 | — | **Pre-registered extension 2** (13 Nov): Qwen2.5-3B/14B full main bank + checks, Qwen2.5-7B Q8 (S1, S3b), comprehension items for 4 models; 23,000+ new decisions, all valid | Run exactly as pre-registered; no deviation. Ada job 74806 (Q8) is listed as FAILED by SLURM only because the end-of-job `kill` of the already-stopped Ollama server returned 1; its log shows the run completed (3,840/3,840). X1–X3 all replicated; E3 TOST inconclusive; Llama C1–C3 = 100% (preference). |
| P7 | Data collection Oct 4–17 | Llama and Qwen completed 28 Oct; extension cells 3 Nov; Mistral 3–4 Nov | Schedule slip. The presentation date (Nov 10) is unchanged. |

## Pilot and fallback decisions (D11)

- Llama-3.1-8B pilot (Ada): P(reject | 10%) = 0.70, P(accept | 50%) = 0.45, so neither ceiling nor floor, and **no 5%/45% cells were added**.
  However, the full S1 data show an almost **flat** discrete offer curve (an outcome the paper's fallback does not cover).
  It is analysed with the graded log-prob DV, and the MAO is reported only where it is identified.
- Qwen2.5-7B: decided by its own pilot (`data/FALLBACK_DECISION_qwen25_7b.txt`). If its fallback fires, the extension cells
  are also run for Llama, to keep the designs identical.

## Still open (needs the team)

1. (Optional) Top up xAI credits to add a genuinely closed model; the code is ready (`--model grok`).
2. Peer rating of the messages (~10 raters). The current freeze is provisional, but every model saw the same 20 messages, so the comparisons remain valid.
3. Qualitative coding by both authors (`python -m analysis.qualitative sheet` / `kappa`).
4. Joint sign-off on `docs/protocol_decisions.md`. The † citations in `docs/literature_review.md` were checked against DOI/Crossref/publisher records on 13 Nov (3 fixed: Akata volume/pages, Coda-Forno arXiv version, Wang article number; the other 37 are correct); one author should still spot-check them before submission.
