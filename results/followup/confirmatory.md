# Follow-up (event-free messages): pre-registered confirmatory results

Pre-registration: `docs/preregistration_followup.md` (frozen 12 Nov 2026, SHA-256 6c276f85…, commit 3e61f16 (originally c219da2; history rewritten on 12 Nov 2026 to edit commit messages only, file contents and dates unchanged), before data
collection; approved by Krishna before collection, by Devansh afterwards on the unchanged document, see P13). Models run: Llama-3.1-8B and Qwen2.5-7B (Mistral not run, its free budget is exhausted, so F3/F4 were not tested).
3,840 decisions + 320 checks per model, all valid on the first attempt.

**Manipulation check:** event-free messages recognised as the intended emotion in 100% of checks, for every emotion and
both models, so the effects are interpretable.

| ID | Prediction (Qwen) | Main study | Follow-up (event-free) [95% CI] | One-sided p (Holm) | Outcome |
|---|---|---|---|---|---|
| F1 | S1: sad proposer lowers rejection (log-OR < 0) | −0.95 | −0.13 [−0.55, +0.29] | .27 | **Not replicated.** The CI excludes the main estimate, so the effect is reliably smaller without life events: the main-study sadness effect was at least partly **event-driven** |
| F2 | S3b: angry trustee lowers share sent | −11.2 pp | −9.6 pp [−15.9, −3.3] | .003 | **Replicated.** Similar size, so the effect is driven by the expressed **emotion** |

**Exploratory (not pre-registered; treat as hypotheses):** with event-free messages, *happy* counterparts raised generosity:
Llama investor sends +20.9 pp to a happy trustee (Holm across the follow-up p = .002); Qwen dictator gives +6.5 pp to a happy
recipient (p = .045). Neither was seen in the main study. Full tables: `results/followup/report.md`, `forest.md`.

**Robustness: message as a random factor (P12, `results/followup/message_re.md`).** Refitting with
`+ C(paraphrase) + (1|message) + (1|message:paraphrase)` and t-tests (df = 16) leaves both conclusions unchanged:
F1 −0.13 [−0.51, +0.25], one-sided p = .26 (CI still excludes the main estimate, −0.91 under the same model);
F2 −9.6 pp [−15.0, −4.2], one-sided p = .002, Holm p = .003. Of the exploratory effects, Llama S3b happy (+20.5 pp) is
FDR- but no longer Holm-significant (.118). Llama S1 happy → *more* rejection (log-OR +0.71 [+0.43, +1.00]) becomes
Holm-significant (.004); it is exploratory and was not seen in the main study.
