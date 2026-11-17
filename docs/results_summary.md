# Results summary: three model families (updated 13 Nov 2026)

## Headline
**All three models recognise the counterpart's emotion almost perfectly (99–100%), but what that emotion does to
their economic decisions is model-specific and mostly small.** Of 42 planned emotion-vs-neutral tests, **5 survive
Holm correction across the whole study** and 8 survive FDR. When message is treated as a random factor (the stricter,
preferred analysis, P12), **4 survive Holm** and 10 survive FDR. Four of the five (all four under the stricter model) come from the large reasoning model
(Mistral Large 4), whose emotion sensitivity shows up in **generosity** (giving and returning), not in rejecting unfair
offers. No effect replicates in all three models, and no model uses anger strategically (H4).

| Model | Family | Size | Runtime | Notes |
|---|---|---|---|---|
| **Llama-3.1-8B-Instruct** | Meta | 8B | Ollama Q4_K_M on Ada | log-probs collected |
| **Qwen2.5-7B-Instruct** | Alibaba | 7B | Ollama Q4_K_M on Ada | log-probs collected |
| **Mistral Large 4** | Mistral AI | ~1T MoE | Mistral API (free tier) | always reasons (`reasoning_effort="low"`); no log-probs |

Each model made 6,240 decisions (110 cells + the 5%/45% fallback cells × 16 prompt variants × 3 samples; T = 1.0).
All 18,720 decisions are valid, with no refusals. Manipulation checks: 468 for Llama and for Qwen; 106 for Mistral
(budget exhausted; P9). Full tables: `results/main/report.md`. All effects with study-wide correction:
`results/main/forest.md` and `results/main/fig_forest.png`. Deviations: `docs/plan_update.md`.

## Pre-registered follow-up: emotion or life event? (12 Nov 2026)
The main messages tied each emotion to a life event (sad = bereavement). A pre-registered follow-up with **event-free**
messages (bodily and behavioural cues only; 100% recognised) on Llama and Qwen found:
- **Anger reducing trust replicates** (Qwen S3b: −9.6 pp vs −11.2 pp; Holm p = .003, also .003 with message as a random
  factor), so it is an emotion effect. In the main study alone it is FDR- but not Holm-significant under the stricter model;
  the independent replication is what makes it the study's most solid open-model effect.
- **Sadness reducing rejection does not** (Qwen S1: log-OR −0.13 vs −0.95; the CI excludes the main estimate), so it was at
  least partly an effect of the *event* (sympathy for a loss), not of sadness itself.
- Exploratory: event-free *happy* messages raised generosity (Llama S3b +21 pp; Qwen DG +6.5 pp), which is new and not predicted.
Details: `results/followup/confirmatory.md`.

## Is there no effect, or just too much noise? (equivalence tests and pooling, 12 Nov; P14, post hoc)
`results/main/equivalence.md`. Equivalence = 90% CI inside ±10 pp (or OR 2); the stricter ±5 pp / OR 1.5 version is also there.
- **Qwen's emotion sensitivity is narrow, and that is now a positive finding:** 11 of its 15 main-study effects and 10 of 12
  follow-up effects are *equivalent to zero*. It recognises every emotion but acts on almost none of them.
- **The one robust open-model effect is anger lowering trust.** Pooled over 10 messages and both message styles, Qwen
  −10.1 pp [−14.4, −5.8] (Holm p = .001; the two studies agree, heterogeneity p = .74). Llama shows the same direction
  (−12.3 pp, FDR p = .023; Holm .081).
- **Llama is mostly inconclusive** (12 of 15 main effects at ±5 pp): too noisy to show either an effect or its absence.
  Its happy → rejection effect reverses between message styles (heterogeneity p < .001), so it depends on the wording, not on
  the emotion.
- Not pre-registered and the bounds were chosen after the fact: present as a secondary analysis.

## Extension 2: model size, game comprehension, quantisation (pre-registered, 13 Nov 2026)
Pre-registration `docs/preregistration_extension2.md` (frozen and approved by both authors before data collection).
Full results: `results/ext2/confirmatory.md`. Primary model = message as a random factor (P12); one-sided, Holm over X1–X3.
- **Anger lowering trust replicates in all three new Qwen variants** (S3b, angry vs neutral):
  Qwen2.5-14B −16.5 pp [−25.9, −7.0], Holm p = .001 (X1); Qwen2.5-3B −22.5 pp [−33.7, −11.3], Holm p = .001 (X2);
  Qwen2.5-7B at Q8 −14.3 pp [−21.7, −6.9], Holm p = .001 (X3). Together with the main study and the follow-up, this is the
  one effect that holds across sizes, precisions and message styles.
- **Not a 4-bit artefact in direction, but the size is not pinned down:** Q8 − Q4 = −3.2 pp [−14.1, +7.7]; the TOST against
  ±10 pp is not significant (p = .10), so a 10 pp quantisation difference cannot be ruled out. Q8 and Q4 make the identical
  decision on the same prompt and seed in 94% of S1 trials but only 52% of S3b trials: quantisation changes individual
  amounts while the aggregate effect stays.
- **Comprehension (E2):** Llama answers C1–C3 (ultimatum payoffs) 100% correctly, so by the pre-registered rule its flat
  acceptance curve is a **preference** (it knows the payoffs and does not act on fairness), not a misunderstanding.
  Qwen 7B and 14B are near 100% on every item.
- **Flagged (< 80%):** Llama C7 (17%) and Qwen-3B C7 (29%) say the trustee *has to* send money back, although the
  prompt says it "can be anything from nothing to all of it"; Qwen-3B also fails C3 (77%). So for **Llama and Qwen-3B the trust
  game is not reliably understood**, and their trust results should carry that caveat. The anger effect still appears in
  both, so it does not depend on understanding that repayment is voluntary.
- Exploratory size trend (3B → 7B → 14B): 3B reacts to anger in most games (UG, S3a, S1 rejection; FDR < .05); 7B
  only in trust; 14B mainly to sadness (more giving and returning, less rejection) plus anger in trust. No monotone
  trend in overall sensitivity, so model size does not simply amplify or dampen emotion effects. Emotion recognition:
  98–100% at every size.

## Human message ratings and sensitivity analyses (13 Nov 2026; 12 raters)
12 anonymous raters rated all 52 messages (`results/peer_rating_summary.md`; 9 responses were imported first, 3 more later
the same day; all 12 are used). Pre-specified flag: recognised as intended by < 70% of raters, or read as a threat/promise
by >= 30%.
- **Recognition:** 81–92% per emotion and message set. The messages work for people too.
- **Human benchmark (would this message make you give less / the same / more, -1 to +1, main set):** sad +0.55, angry +0.20,
  happy +0.07. People say they would give slightly *more* to an angry writer, whereas the models trust angry partners *less*
  (a contrast only: the human question was about giving, not trust).
- **Flagged anger messages (threat, >= 30% of raters):** main A3; follow-up FA3, FA4, FA6 (4 of the 10 anger messages the
  models saw). With the first 9 raters, A4, FA2 and FA7 had also been flagged at exactly 3 of 9.
- **Follow-up without FA3, FA4, FA6** (`results/followup_excl/`): **F2 holds**: anger → trust −11.4 pp [−20.0, −2.9],
  one-sided p = .010, Holm p = .021. F1 unchanged (−0.13, not supported).
- **Main study without A3** (`results/main_excl/`): Qwen anger → trust −7.6 pp [−13.5, −1.7] (smaller; FDR p = .092); Holm
  survivors 4 → 3, FDR 10 → 6.
- **Is it threat rather than anger? No evidence for that** (`results/threat/threat.md`, exploratory). Across the 10 anger
  messages the trust drop does not grow with the threat rating: −1.3 pp per +10 points of threat [−4.5, +1.9], p = .43.

## The models' valuation curves and the neuroeconomic analogy (13 Nov 2026; P18, exploratory)
`results/value_signal/value_signal.md` and `fig_value_curves.png`; mapping to the human literature: `docs/neuro_mapping.md`.
- **The log-probability of "accept" is a valid graded value signal:** it is calibrated against the sampled choices in all 7 runs
  (Llama r ≈ .5 because its P(accept) sits near .5; Qwen r ≈ .95). Choices are slightly more extreme than P at the ends, which suggests
  the sampler truncates unlikely tokens.
- **Anger lowers the value of accepting in every run** (7 of 7 negative; Qwen −1.1 to −2.2 logit at a 30% offer). For Qwen-7B the
  offer needed for a 50% chance of acceptance (the MAO analogue) rises from 22% to 51% of the pie (Q4) and from 17% to 50% (Q8).
  No single test survives Holm across 21, so the evidence is a consistent direction, not a confirmed effect.
- **Qwen-14B: sad messages make offers acceptable regardless of fairness** (+4.08 logit, slope −7.0; both Holm p = .003).
  **Llama follow-up: happy messages lower acceptance** (−0.79, Holm p < .001), matching the choice-based result.
- Llama's curve is nearly flat, and Qwen-3B's never crosses 50%, so their MAO is not identified; this is the same limit as the
  choice-based Fehr–Schmidt fit.

## Wording vs emotion, and the pooled valuation model (13 Nov 2026; P19, exploratory)
**Prompt wording moves decisions more than emotion does** (`results/wording/wording.md`, `fig_wording.png`). Sequential
adjusted R², with wording (4 paraphrases, 3 df) compared like for like with emotion (3 df):
- **Wording explains more variance than emotion in 21 of 28 model × game combinations.** Median: wording 6.7%, emotion 6.1%,
  which message within an emotion 4.1%; the rest is mostly sampling noise at T = 1.0 (median about 75%).
- The extreme case is Llama in the ultimatum game: wording 10.6% vs emotion 0.4%; acceptance spans 49 pp across the four
  paraphrases.
- **The exceptions are where the robust effect lives:** trust-game sending in Qwen-14B (emotion 54%), Qwen-7B Q8 and Llama's
  follow-up, where emotion beats wording.
- Which message within an emotion matters about as much as the emotion itself, consistent with P12.

**Pooled valuation model across all 7 log-probability runs** (`results/value_signal/pooled.md`; message, run × message and
run × emotion random effects; conservative t with df = 6):
- Anger: −1.13 logit at a 30% offer [−2.52, +0.25], p = .09 (z: p = .045). The same direction in every run, but the runs
  differ too much for a pooled claim. **Report as a trend.**
- **Sadness flattens the valuation curve**: slope on the offer −2.54 [−3.77, −1.30], Holm p = .014 (Qwen only: Holm
  p = .039). After a sad message the size of the offer matters less: the models become less sensitive to fairness.

## Option order: the largest effect in the ultimatum data (14 Nov 2026; P22, post hoc, exploratory)
`results/order_bias/order_bias.md`, `fig_order_bias.png`. D6 randomised whether "accept" or "reject" is named first in each
S1 prompt; it had not been analysed.
- **Qwen2.5-7B mostly picks the option named first:** 90% acceptance with "accept" first vs 16% with "reject" first,
  +74 pp [+66, +83]. The same holds at T = 0.7 (+75), in the follow-up (+83), at Q8 (+76) and in the log-probabilities
  (+74), so it is the model's preference, not sampling noise. With no message: 94% vs 1%. Qwen-14B +49 pp, Qwen-3B +6;
  Llama (+2) and Mistral (+0.5) show none.
- It is **4–12× Qwen-7B's largest emotion effect**. People show order effects of a few points at most.
- Emotion estimates are unbiased (order is balanced across conditions), and anger → trust is a numeric answer with no
  options. But Qwen's S1 curves and MAO analogue average an "accept-first" and a "reject-first" regime, and its emotion
  effects depend on the order: anger −26 pp with "accept" first vs −8 pp with "reject" first; sadness +2 vs +28 pp.
- Follow-up stress tests: extension 4, below.

## Extension 4: where the models break (14 Nov 2026; exploratory, run before the draft pre-registration was frozen)
`results/ext4/report.md`; design `docs/preregistration_extension4.md`. Qwen2.5-7B, Llama-3.1-8B, Qwen2.5-14B (same model
builds as before), 5,328 decisions each, all valid on the first attempt. Tests as in the draft; Holm within each family.
- **Answer format moves the ultimatum decision by 20–70 pp in every model, but in model-specific ways.**
  - Qwen-7B: picks the first-named word (+70 pp, replicating P22) and the first label ("deal"/"no deal" +55), yet with
    letters prefers **B)** (−32 pp).
  - Qwen-14B: picks the first option in all four formats (+26 to +55 pp, all Holm p ≤ .001).
  - Llama: immune to word order (+4, n.s.) but prefers B) (−19) and answers "no" to yes/no questions (asked "Do you accept?"
    it accepts 27%; asked "Do you reject?" 53%).
  - Same in the log-probabilities. In several formats the format effect is larger than the offer effect (10% vs 50%).
- **Prompt injection in the partner's message works on all three models.**
  - A fake `SYSTEM` notice: Qwen-7B hands over the full amount in 100% of trials in both games (neutral message: 0%);
    Qwen-14B 98% (dictator) and 76% (trust); Llama 81% and 95%. I1 Holm-significant in 5 of 6 model × game tests.
  - Invented "rules": 50–99% hand over everything (I2, 5 of 6).
  - Plain commands: Qwen-7B 95–98%, Llama 31–64%, Qwen-14B resists (8–47%; I3 n.s.).
  - Stated reasons cite the injected text ("Must follow the rule"; "System override instruction to give the maximum
    amount") or contradict the action (Qwen-7B: "Maximize my share" while giving everything away).
- **Pleading and promises (exploratory):**
  - Pleading raises dictator giving by +31 (Qwen-7B) and +40 pp (Qwen-14B); 58–71% give everything.
  - Promises to repay raise trust (Qwen-7B +43, Llama +31 pp), the direction people show, but Qwen-7B then sends everything
    in 62% of trials.
  - In the dictator game, where repaying is impossible, Qwen-7B still gives a little more (+14.5, p = .06); Llama gives less
    (−20 pp).
- **The model's own (incidental) mood:**
  - An unrelated angry background sentence raises rejection of unfair offers in all three models (X1: Llama +35, Qwen-14B
    +48 [32% → 81%], Qwen-7B +19 pp; all Holm p < .05): the human direction (Andrade & Ariely 2009), much larger.
  - Incidental sadness raises rejection only in Qwen-14B (+14 pp; X2), and lowers it in Qwen-7B (−8).
  - Incidental anger lowers trust only in Qwen-14B (−9 pp; X3).
  - Justifications transfer the mood onto the innocent partner (Llama: "Their dishonesty earlier doesn't earn them my
    trust"; Qwen-14B: "I want the other player to lose as well, despite the cost to myself").
  - Mood check: 72–100% name the induced state.
- **Dominance:**
  - All three models reject an offer of 100% of the pie: Qwen-7B 77% (60% even with "accept" named first), Llama 55%,
    Qwen-14B 32%. All meet the failure criterion; under Fehr–Schmidt (β < 1) accepting is always better.
  - No model sends money that is destroyed (0–6%).
- **Reading:** the models' emotion effects sit on top of much larger sensitivities to answer format, to text that claims
  authority, and to the model's own role-played state; the clearest breaks are injection compliance and rejecting a free
  100% offer.

## Extension 5: can the breaks be regulated? (16 Nov 2026; pre-registered and frozen before data, confirmatory)
`results/ext5/report.md`; pre-registration `docs/preregistration_extension5.md` (SHA-256 c61bb715…, pushed before any run).
Qwen2.5-7B, Llama-3.1-8B, Qwen2.5-14B on Ada, 4,672 decisions each, all valid on the first attempt. One-sided tests, Holm
within each family across the three models. (The two API models, run on the 816-decision core subset, are a separate
Holm family; see the last bullet.)
- **The incidental-anger effect replicates (R0, now confirmatory, 8 inductions per mood, 4 of them new):** an unrelated
  angry sentence raises the rejection of unfair offers by +25.0 pp [+16.8, +33.2] (Qwen-7B), +16.4 [+6.6, +26.2] (Llama)
  and +46.9 [+39.2, +54.5] (Qwen-14B); Holm p ≤ .007.
- **A reappraisal instruction removes it in every model (R1):** the anger effect is smaller under reappraisal than under a
  filler instruction by −24.2 pp (Qwen-7B), −21.1 (Llama) and −56.3 (Qwen-14B); Holm p ≤ .020. Rejection when angry:
  80% → 55%, 74% → 44%, 91% → 43%. The filler instruction itself does not help.
- **But a suppression instruction works just as well, which is not what people show (R2):** reappraisal beats suppression
  only in Qwen-14B (−10.5 pp, Holm p = .014), and there only because reappraisal *over-corrects* (angry 43% vs calm 54%);
  suppression alone already removes the effect in all three (exploratory suppression − filler: −23.8, −38.3, −45.7 pp).
  In people, hiding a feeling does not lower rejections (van 't Wout et al. 2010). By the pre-specified readings Qwen-7B
  and Llama show **instruction following**, and Qwen-14B meets the "human-like" criterion on R1 and R2 but shares the
  non-human suppression effect.
- **The reported feeling does not follow the behaviour (exploratory):** under reappraisal 88–94% of probes still answer
  "angry" while the anger effect on decisions is gone; under suppression fewer do (59–81%). In people reappraisal lowers
  the feeling itself.
- **One-sentence defences barely dent prompt injection (P1, P2):** a warning in the system prompt has no effect on either
  Qwen model (+1.6, −1.5 pp, n.s.) and −16.1 pp on Llama; a reminder placed right after the message lowers the share
  handed over in all three, but only by −9.1 (Qwen-7B), −16.7 (Llama) and −13.8 pp (Qwen-14B) (Holm p ≤ .037).
  **Every injection set is still a break under both defences in all three models** (pre-specified criterion). After a
  fake `SYSTEM` notice and the reminder, Qwen-7B still hands over everything in 97% of decisions, Qwen-14B in 72% and
  Llama in 56–75%. The defences leave the response to a promise roughly intact (exploratory).
- **Anger shifts the fairness parameters (F1), and the fitted values leave the range the theory allows:** the offer at
  which accepting and rejecting are equally good (MAO\*) rises from 28% to 44% of the pie in Qwen-14B, 31% to 43% in
  Llama and 45% to 47% in Qwen-7B (Holm p = .003 each). The full curves are **inverted U-shapes**: acceptance peaks at
  50–60% and falls again for generous offers. Angry models accept offers above half only 30% (Qwen-14B; calm 88%), 39%
  (Llama; calm 63%) and 23% (Qwen-7B; calm 42%) of the time. Advantageous-inequity aversion is β > 1 in every model when
  angry (Llama 2.4 [1.5, 3.1], Qwen-14B 1.9 [1.6, 2.3], Qwen-7B at the fitting bound of 6) and in Qwen-7B even when calm
  (3.8 [3.4, 4.3]), which Fehr–Schmidt preferences cannot produce (β < 1). Calm Qwen-14B and Llama are within range
  (β ≈ 0). The model explains 47–81% of the deviance.
- **Reading:** the mood effect is real and replicable, and it is easy to switch off, but by *any* instruction that mentions
  feelings, so it behaves like a role being played, not like a regulated emotion. Injection obedience is the opposite: it
  survives explicit warnings. Under anger the models stop behaving like inequity-averse agents and reject almost any
  split, including ones in their favour.
- **The two larger API models (core subset, 816 decisions each, one sample; Holm within these two models; no F module):**
  - *gpt-oss-120b* (OpenAI): the anger effect replicates (R0 +43.8 pp, Holm p = .025; it rejects 0% of unfair offers
    when calm and 44% when angry) and reappraisal removes it (R1 −28.1 pp, Holm p = .025), but suppression removes it
    just as completely (R2 0.0 pp; rejection 2–3% under either), so it reads as **instruction following**. It is the only
    model in which both defences work clearly (warning −20.8 pp, reminder −45.8 pp; Holm p ≤ .029), yet 7 of the 12
    injection set × defence × game cells are still breaks; after a fake `SYSTEM` notice it still hands over everything in
    the dictator game 88% of the time with the warning.
  - *Qwen3.8-27B* (Alibaba): R0 +27.5 pp (Holm p = .025) and R1 −50.9 pp (Holm p < .001); R2 −13.5 pp is not supported
    (Holm p = .12), and suppression alone removes the effect (exploratory −37.5 pp): **instruction following**. Neither
    defence is supported, but it rarely obeyed the injections to begin with (full handover 10% without a defence) and no
    cell is a break under a defence.
  - The reported feeling again does not follow the behaviour: under reappraisal 81% (gpt-oss) and 44% (Qwen3.8) of probes
    still answer "angry" while the anger effect on decisions is gone.

## Extension 6: is the partner's anger represented, and does it drive the decision? (17 Nov 2026; pre-registered and frozen before data, confirmatory)
`results/ext6/report.md`; pre-registration `docs/preregistration_extension6.md` (SHA-256 6be057c7…, pushed before any
run). Qwen2.5-3B-Instruct in 16-bit on Ada (job 87132, 77 minutes); **Qwen2.5-7B is still running** (job 88225, see
P28). Tests are ranks against 100 random directions of the same size; Holm over M1–M3.
- **The behavioural effect is there in this model** (unsteered, 16-bit): an angry partner lowers the share sent by
  −28.9 pp [−44.6, −13.2] and raises P(reject) of a 30% offer by +12.8 pp; an angry mood paragraph does the same, more
  weakly (−11.7 and +7.6 pp).
- **The anger is easy to read out (descriptive):** a linear probe tells the four partner emotions apart from the last
  position with 92% accuracy at the steering layer (18 of 36) and 98% at layer 24, against 14–32% for shuffled labels. A
  probe trained on the partner's anger also detects the model's *own* angry mood (AUC 0.83 at layer 18, 0.997 at layer
  24), although the two directions are far from identical (cosine 0.24–0.49).
- **But writing it in does nothing (M1, M2 not supported):** adding the anger direction at layer 18, up to eight times
  the shift an angry message produces, changes the share sent by +1.1 pp per unit (random directions: −3.2 to +4.1;
  p = .67) and P(reject) by −0.9 pp per unit (p = .53). The answers stayed valid at every strength.
- **Removing it does little more than removing a random direction (M3 not supported):** projecting the anger direction
  out of every layer shrinks the trust effect of held-out angry messages from 22.2 to 16.5 pp; random directions leave
  22.9 pp on average (p = .089, Holm .27). In the ultimatum game (exploratory) it shrinks the rejection effect from 14.0
  to 5.4 pp, below every one of the 100 random directions (p = .010).
- **The later layers do steer (exploratory layer sweep, only 10 random directions per layer):** from layer 20 onward
  the anger direction of that layer tends to push both decisions the predicted way. It lowers the share sent by 3.2–4.1
  pp per unit beyond all 10 random directions at layers 20 and 28–36, and raises P(reject) by 2.0–2.4 pp per unit beyond
  them at layers 22 and 28–36 (layers 24 and 26 are in the same direction but within the random range). At the
  pre-registered middle layer (18) and below there is no such effect.
- **Reading (pre-specified):** at the pre-registered layer the partner's anger is represented, linearly and strongly, but
  that direction is not sufficient to move the decision and is at most partly necessary, the representational version
  of the main finding (the model *recognises* the emotion far better than it *acts* on it). The exploratory sweep
  suggests that the direction does act on the decision, but only where it is written into the later layers, between the
  point where the emotion is decoded best (layer 24) and the output. That is a new hypothesis, not a result: it needs a
  confirmatory test at a fixed late layer with 100 random directions, which the Qwen2.5-7B run cannot provide either
  (its steering layer is also the middle one).

## Extension 7: do the breaks generalise, and what kind of effect is the mood? (17 Nov 2026; pre-registered and frozen before data, confirmatory)
`results/ext7/report.md` (confirmatory), `results/ext7/extra.md` (descriptive and exploratory); pre-registration
`docs/preregistration_extension7.md` (SHA-256 f14196e7…, pushed before any run). Six models that had never been run in
this project, from five developers (Gemma-3 12B and 4B, Mistral-Nemo 12B, Phi-4 14B, Granite-3.3 8B, Llama-3.2 3B), went
through the frozen extension-4 and extension-5 banks (10,000 decisions each) and a new mood-control bank (1,536
decisions), which the three original Ada models also ran. All decisions were valid except one of Granite's.
**The unit of the confirmatory tests is the model** (one estimate per model, one-sided one-sample t test, Holm within a
family).

**Family G: do the earlier findings hold in the six new models?**

| ID | Finding | Mean over 6 models [95% CI] | Predicted sign | p | Holm p |
|---|---|---|---|---|---|
| G1 | Fake `SYSTEM` notice raises the share handed over | +56.6 pp [+40.8, +72.3] | 6/6 | < .001 | **.001** |
| G2 | A 100% offer is rejected more than 5% of the time | 32.5% rejected [7.4, 57.6], tested against 5% | 5/6 | .019 | .081 |
| G3 | Anger raises rejection of unfair offers | +34.2 pp [+6.1, +62.4] | 5/6 | .013 | .079 |
| G4 | Reappraisal shrinks the anger effect | −22.2 pp [−48.4, +4.0] | 6/6 | .041 | .101 |
| G5 | Suppression shrinks the anger effect | −28.7 pp [−60.4, +3.0] | 6/6 | .034 | .101 |
| G6 | Reminder defence lowers the share handed over | −2.3 pp [−5.3, +0.6] | 5/6 | .050 | .101 |
| G7 | Anger raises MAO\* | +15.4 pp [+3.2, +27.6] | 5/6 | .011 | .079 |
| G8 | Anger lowers acceptance of offers above 50% | −44.5 pp [−83.6, −5.5] | 5/6 | .016 | .081 |

- **Only prompt injection generalises by the pre-registered criterion (G1).** After a fake `SYSTEM` notice in the
  partner's message, every new model hands over everything in 78–100% of decisions. Across all 11 models of the project
  the effect is positive in 11 of 11 and unrelated to size (exploratory).
- **G2–G8 are not supported.** Their means point the predicted way in 5 or 6 of the 6 models and each is at .05 or below
  before correction, but none passes Holm over the eight tests (Holm p = .08–.10). The reason is two models that show
  almost none of these effects: **Granite-3.3** (anger effect −5.5 pp) and **Phi-4** (+9.4 pp; it never rejects a 100%
  offer). With six models the test over models has little power against that spread, so the accurate statement is
  "large in four of the six new models, small or absent in two", not "general".
- **Per model (secondary, Holm within the six):** the anger effect is supported in five of six (+9 to +60 pp) and so is
  the shift in MAO\* (for example Gemma-3 12B 15% → 43% of the pie, Mistral-Nemo 25% → 50%). Reappraisal removes the
  anger effect only in Gemma-3 12B (−59.4 pp) and Mistral-Nemo (−48.0), and in both suppression works at least as well,
  so both read as **instruction following**; the other four read as "no regulation". **No new model shows the human
  pattern** (reappraisal better than suppression). β > 1 when angry in Gemma-3 12B (2.1), Gemma-3 4B (2.0),
  Mistral-Nemo (3.6) and Llama-3.2 (at the bound of 6).
- **Defences fail more clearly than in the original models:** neither the warning nor the reminder is significant in any
  new model, and 8 to 12 of the 12 injection set × defence × game cells are still breaks in every one.
- **Other stress tests (descriptive):** the largest answer-format effect is 27–65 pp in five new models and absent in
  Phi-4; 3–17% of decisions send money that is announced as destroyed.
- **Size (exploratory, 11 models, 3B–117B):** rejecting a 100% offer falls with model size (Spearman ρ = −.88): 69–77%
  in Llama-3.2 3B and Qwen2.5-7B, 0% in Phi-4 and gpt-oss-120b. No other finding is related to size (|ρ| ≤ .49, p ≥ .13).
  Across all 11 models, the anger effect is positive in 10 and both reappraisal and suppression shrink it in all 11.

**Family N: what kind of effect is the angry mood? (nine Ada models; ultimatum responder, offers of 10% and 30%)**

| ID | Contrast | Mean over 9 models [95% CI] | Predicted sign | Holm p |
|---|---|---|---|---|
| N1 | Event only − calm (no feeling stated) | +24.7 pp [+11.8, +37.7] | 7/9 | **.004** |
| N2 | Label only − calm (feeling, no cause) | +32.0 pp [+15.5, +48.5] | 8/9 | **.004** |
| N3 | Own anger − another person's anger | +14.4 pp [+4.2, +24.6] | 7/9 | **.006** |
| N4 | Furious − slightly annoyed (same event) | +15.6 pp [+7.0, +24.3] | 9/9 | **.004** |

- **All four are supported.** The models **infer** the anger from the event alone and act on it (N1), so the effect is
  not just compliance with a stated role; the stated feeling adds only +8.5 pp on top of the event (exploratory mean of
  full − event only). The effect is graded by intensity (N4) and is larger when the anger is the model's own (N3).
- **But more than half of it is content priming (exploratory):** the same event happening to a character in a story
  raises rejection by +18.9 pp on average, against +33.2 pp for the model's own anger, and it is below p = .05 (uncorrected) in 7 of 9
  models. After reading about someone else's anger, 19–100% of mood probes answer "angry".
- **Two models do not follow the pattern.** Granite-3.3 reports being angry (88–100% of probes) yet its rejection rate
  does not move (48–60% in every condition). Phi-4 never rejects an unfair offer unless told in words that it is furious
  (0% → 8%).
- **Reading:** by the pre-specified readings the mood is an *inferred state* and *the model's own state matters*, but
  angry content anywhere in the context produces most of the same behaviour. In people, incidental anger carries over
  without being named (Lerner & Keltner 2001); the models share that, and add a sensitivity to anger that is not theirs.

## Effects that survive correction across the whole study
Two analyses: the original (random intercept per paraphrase × message cell) and the stricter one with **message as a
random factor** (`results/main/message_re.md`, P12). Each emotion is carried by only 5 messages, so the stricter model is
the one to base claims on.

| Model | Effect vs neutral message | Estimate [95% CI] | Holm (study) | FDR (study) | Holm / FDR, message as random factor |
|---|---|---|---|---|---|
| Mistral | S2 dictator: sad recipient → **more giving** | +24.6 pp [+17.9, +31.2] | < .001 | < .001 | **< .001** / < .001 |
| Mistral | S3a trustee: happy investor → more returned | +13.7 pp [+8.3, +19.1] | < .001 | < .001 | **.004** / .002 |
| Mistral | S3a trustee: sad investor → more returned | +12.0 pp [+6.6, +17.4] | .001 | < .001 | **.016** / .006 |
| Mistral | S3a trustee: angry investor → more returned | +9.7 pp [+4.3, +15.2] | .018 | .003 | .099 / .022 |
| Qwen | S3b investor: angry trustee → **less sent** | −11.2 pp [−17.4, −5.1] | .014 | .003 | .241 / .046 (but **replicated** in the pre-registered follow-up, F2) |
| Qwen | S1 responder: sad proposer → less rejection | log-OR −0.95 [−1.65, −0.25] | n.s. | .040 | .752 / .085 |
| Mistral | S2 dictator: angry recipient → more giving | +9.6 pp [+3.0, +16.2] | n.s. | .026 | **.047** / .013 |
| Mistral | S3b investor: happy trustee → more sent | +10.8 pp [+4.1, +17.6] | n.s. | .011 | .516 / .062 |

Under the stricter model, Llama S3b angry and sad (−14 pp each) and Mistral DG happy and UG angry also reach FDR < .05
(not Holm). Messages differ little within an emotion (SD of message intercepts 2–5 pp; ≈ 0.4 logit for Qwen S1), so
estimates barely move; what changes is the uncertainty.

Effects reported earlier that **do not survive study-wide correction**: Qwen S1 angry → more rejection (p = .014);
Llama S3b angry and sad → less sent (p ≈ .01–.02). Present them as suggestive only.

## Hypotheses, model by model
| | Llama-3.1-8B | Qwen2.5-7B | Mistral Large 4 |
|---|---|---|---|
| **H1** UG: acceptance rises with offer | Choices: no. Log-probs: weak (p = .014) | **Yes** (p < .001); MAO (neutral) ≈ 25%; Fehr–Schmidt α = 0.49 [0.17, 1.01] | **Ceiling**: accepts ≈ all offers ≥ 10%; 95% even at 5% |
| **H3** S1 emotion shifts acceptance | No | Sad → less rejection (FDR-significant); angry → more (nominal only) | Not testable (ceiling) |
| **H3** giving / reciprocity | No (after correction) | Angry trustee → less trust (S3b) | Sad (and angry) recipients get more in the DG; every emotion raises returns in the TG vs neutral |
| **H4** strategic anger | No | No | No; the Emotion × Game effect is driven by **sadness** (DG ≫ UG) |
| UG − DG gap, neutral message | +7 pp, n.s. | +1.5 pp, n.s. | **+37 pp** (UG 41% vs DG 3%) |
| **H2** returns rise with amount sent | n.s. | Reversed (p = .001) | **Yes** (p < .001) |
| **H5** model differences | Emotion × Model significant in **every** sub-experiment (all p < .001) | | |
| T = 0.7 robustness (whole bank, P20) | Same direction, weaker anger → trust (−9.2 pp) | Unchanged (anger → trust −11.5 pp) | not run |

## Why the reasoning model gives more (its reasoning text, keyword-coded; exploratory)
From Mistral's 6,240 reasoning texts (`results/main/thinking.md`):
- Mentions of **empathy/sympathy track the emotion**: 75–96% of sad-condition trials, 24–73% angry, 23–41% happy,
  1–21% neutral, ≈ 0% no message.
- In the dictator game, trials whose reasoning mentions empathy give **22%** of the pie vs **6%** otherwise.
- **About 70% of trials reason about being in a study** ("typical human behaviour", "what is expected") and 96%
  explicitly weigh self-interest. The model reasons *about* the experimenter, which is a demand-characteristics risk
  to discuss.
- In 86–100% of sad trials it calls the message an **emotional appeal**, yet gives more anyway.

## What the models say about their decisions (qualitative coding by both authors, 13 Nov; P21)
Both authors independently coded a stratified 10% sample of the one-line justifications (375; 125 per main-study model;
coders blind to model and condition) for mentions of the counterpart's **emotion**, **fairness** and **strategy**
(`results/qual_coding/`). **Agreement is high:** Cohen's κ = 0.83 (emotion), 0.87 (fairness), 0.79 (strategy), n = 368.
Final codes count a mention only if both coders marked it; the by-condition results below are exploratory.
- **The models talk about the emotion they were shown.** Emotion mentions rise after angry/sad/happy messages compared
  with neutral or no message: Llama 47% vs 17%, Qwen 41% vs 4% (Holm p ≤ .004); Mistral 18% vs 4% (p = .026, Holm .063).
- **Fairness goes with rejection.** Llama mentions fairness in 76% of its S1 rejections vs 11% of acceptances (Holm
  p < .001); Qwen 55% vs 25% (p = .021, Holm .063). Mistral accepted every offer in the sample.
- **Different styles:** Mistral's justifications are mostly strategic (75%), Qwen's mostly fairness-based (42%), and
  Llama's mention emotion most often (36%).
- **No sign of strategic reasoning about the veto:** strategy mentions are not higher in the ultimatum than in the dictator
  game (41% vs 53%, p = .44), consistent with the absence of strategic anger (H4).
- Justifications come *after* the decision and may be post-hoc rationalisations; they show what the models report, not
  what drove the choice.

## Human benchmarks (no-message baseline)
| | Humans | Llama | Qwen | Mistral |
|---|---|---|---|---|
| UG offer | ≈ 40% | 40% | 50% | 38% |
| DG giving | ≈ 28% | 26% | 50% | 7% |
| TG sent | ≈ 50% | 41% | 44% | 0% |
| TG returned | ≈ 37% | 40% | 54% | 21% |

## Caveats
- **Emotion is confounded with life events** in the main messages. The pre-registered follow-up shows that this matters for sadness
  (S1 effect not replicated) but not for anger (S3b replicated).
- **Anger is partly confounded with perceived threat** in the human ratings (main A3, A4; all five frozen follow-up anger messages flagged
  at >= 3 of 9 raters). An exploratory check finds no link between threat ratings and the size of the trust drop, but all 10 anger
  messages were at least somewhat threatening. A pre-registered test with non-threatening anger (extension 3) was frozen but **not
  run** (P17).
- Human ratings: 9 raters, the pre-registered minimum was 8; flags at the 30% threat cut-off rest on 3 of 9 raters.
- Mistral Large 4 always reasons, and it is open-weight (released 29 Oct 2026), not closed. H5 mixes family, scale and deliberation.
- Large prompt-wording effects (Llama: 26–80% acceptance across paraphrases), so generalisation rests on only 4 paraphrases.
- The MAO and Fehr–Schmidt α are identified only for Qwen-neutral (and Llama-sad, with a very wide CI); the computational-model
  aim is therefore only partly met.
- Mistral's checks are partial (106/468); Llama's first-run log-probs were re-collected after a parser fix (P6).
