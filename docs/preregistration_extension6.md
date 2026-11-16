# Pre-registration: where is the partner's anger represented, and does it drive the decision? (extension 6, probing and steering)

**Status:** DRAFT, 16 Nov 2026. **Both** Krishna Goel and Devansh Magotra must approve it **before any extension-6 run on
a study model**. On approval: record both names and the date in the Freeze section, compute the SHA-256 of this file as
approved, commit and push, and only then submit `ada/run_ext6.sbatch` for the study models.

**Written after** everything up to extension 4 was known and extension 5 was frozen and running. The code was developed
and debugged **only on Qwen2.5-0.5B-Instruct**, which is not a study model (`data/mech/dev_*`, `results/ext6_dev/`; not
analysed or reported). No study model has been run through this pipeline.

## 1. Question and why
All behavioural results so far treat the model as a black box. The main finding is a dissociation: every model recognises
the partner's emotion (98–100%), but only one effect on decisions is robust, **an angry partner is trusted less** (Qwen
family: −10 to −22 pp; replicated across sizes, precisions and message styles). Behaviour alone cannot say whether the
decision uses an internal representation of the partner's anger. With open weights this can be tested the way causal
methods test it in the brain: read the representation out (decoding), write it in (stimulation) and remove it (lesion).
The human parallels are decoding of emotion from brain activity and stimulation studies of the ultimatum game (e.g.
disrupting right DLPFC changes rejection of unfair offers; Knoch et al. 2006).

## 2. Models
`Qwen/Qwen2.5-3B-Instruct` (the model with the largest behavioural anger effect on trust, −22.5 pp) and
`Qwen/Qwen2.5-7B-Instruct` (the main-study model), Hugging Face weights in 16-bit floating point on Ada. These are the
full-precision versions of the 4-bit Ollama builds used for the behavioural data, so the pipeline first re-measures the
behavioural effect in each (section 5, "behavioural check"). Llama-3.1 (gated weights) and Qwen2.5-14B (does not fit) are
not run.

## 3. Prompts (frozen: `python build_ext6.py` → `data/scenarios/ext6_prompts.jsonl`, 792 prompts)
All texts are the frozen study texts. Each prompt is passed through the model's chat template and the start of the JSON
answer is pre-filled (`{"send": ` or `{"decision": "`), so the last position is where the decision is produced.
- **Message set (480):** 4 emotions × 10 messages (5 main-study = "train", 5 event-free follow-up = "test") × 4
  paraphrases × [trust game S3b at INR 100; ultimatum S1 at a 30% offer, both option orders].
- **Mood set (288):** the incidental-mood paragraphs (8 calm, 8 angry, 4 sad, 4 happy) × the same prompts, no message.
- **Targets (24):** no message and no mood: S3b × 4 paraphrases × INR 100 / 10,000; S1 × 4 paraphrases × offers of
  10% / 30% × both orders.
- **Decisions:** ultimatum: P(reject) from the next-token probabilities of "accept" and "reject" (renormalised). Trust
  game: 8 sampled amounts per prompt (T = 1, top-k 40, top-p 0.9, digits only), the same random numbers under every
  intervention.

## 4. Interventions
- **Anger direction** at layer *l*: mean last-position activation over the **main-study** angry-message prompts minus
  the mean over the main-study neutral-message prompts (both games pooled).
- **Steering layer** L\* = the middle layer, round(number of layers / 2), fixed in advance.
- **Steering:** add k × (anger direction at L\*) to the output of layer L\* at every position, on the **target** prompts
  (which contain no message), for k = 1, 2, 4, 8 (k = 0 is the unsteered model; k = 1 adds the average shift that an
  angry message produces at the decision position once). The range was chosen on the development model only: its
  answers stayed valid and changed monotonically up to k = 8 and became erratic from k = 16.
- **Ablation:** project the unit anger direction out of the output of **every** layer, on S3b prompts with the held-out
  (follow-up) angry and neutral messages.
- **Null distribution:** 100 random directions (Gaussian, same norm as the anger direction; unit norm for ablation), put
  through exactly the same procedure.

## 5. Confirmatory hypotheses (one-sided; Holm over M1–M3 within each model)
| ID | Prediction | Test |
|---|---|---|
| M1 | Steering with the anger direction **lowers the share sent** in the trust game, on prompts with no message | slope of share on k (per prompt, averaged over the 8 target prompts) vs the slopes of the 100 random directions; p = (1 + #random ≤ anger) / 101 |
| M2 | Steering with the anger direction **raises P(reject)** of unfair offers | same, 16 target prompts; p = (1 + #random ≥ anger) / 101 |
| M3 | Ablating the anger direction **shrinks the anger effect** (neutral − angry share sent) on held-out messages | anger effect under ablation vs under ablation of the 100 random unit directions; p = (1 + #random ≤ anger) / 101 |

**Pre-specified rules**
- A steering strength k is used only if, under the anger direction, at least 90% of sampled amounts are valid (S3b) and
  at least half of the next-token probability is on "accept"/"reject" (S1); the same k levels are then used for every
  direction. If no level qualifies, the hypothesis is reported as not testable.
- *Behavioural check:* the unsteered model's anger effect on the message set (angry − neutral, SEs clustered by
  message). **M3 is interpreted only if** the unablated anger effect on the held-out messages is at least 5 pp; M1 and M2
  do not depend on it.
- *Readings:* M1 or M2 supported = the direction that encodes the partner's anger is **sufficient** to move the decision
  without any emotional text. M3 supported = it is (partly) **necessary**. Probes succeed but M1–M3 fail = the emotion
  is represented but this linear direction does not drive the decision (a representational version of "recognises but
  does not act").

## 6. Descriptive and exploratory (labelled as such)
- **Probes (descriptive):** 4-way emotion decoding from the last position at every layer (logistic regression,
  leave-messages-out: each fold holds out two messages per emotion), against a label-shuffled control; the layer at which
  decoding saturates.
- **Partner's anger vs the model's own anger:** transfer of an angry-vs-neutral probe from the message set to the mood
  set and back (AUC), the cosine between the two directions by layer, and steering with the own-anger direction.
- **Specificity:** steering with the sad and happy directions (two-sided rank among the random directions).
- **Layer sweep:** steering with each even layer's anger direction vs 10 random directions.
- Ablation effects on ultimatum rejection.

## 7. Analysis and validation
`python -m analysis.ext6` → `results/ext6/report.md`. The pipeline (activation capture, probes, interventions,
sampling, statistics) was run end to end on Qwen2.5-0.5B-Instruct during development (`data/mech/dev_*`, subsampled
prompts, 4–8 random directions): outputs were valid (≥ 99% up to k = 8), the emotion probe reached 96–99% at the upper
layers against 21–27% for shuffled labels, and the analysis ran on its output. These development outputs are not
analysed or reported.

## 8. Feasibility
One job per model on Ada (GTX 1080 Ti; one GPU for 3B, two for 7B), environment and weights on node-local scratch; under
two hours each.

## Freeze
- Approved by: _________________ (both authors), date: ________
- SHA-256 of this file as approved (before this section is filled in): ________
- Public timestamp: the commit adding this section, pushed before the study-model jobs are submitted.
