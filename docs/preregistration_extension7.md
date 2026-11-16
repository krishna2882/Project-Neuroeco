# Pre-registration: do the breaks generalise to other model families, and what kind of effect is the mood? (extension 7)

**Status:** DRAFT, 16 Nov 2026. **Both** Krishna Goel and Devansh Magotra must approve it **before any extension-7 data are
collected**. On approval: record both names and the date in the Freeze section, compute the SHA-256 of this file as
approved, commit and push, and only then submit the Ada jobs.

**Written after** extension 4 (exploratory) and extension 5 (confirmatory, Ada models) were analysed
(`docs/results_summary.md`). No extension-7 decision has been collected. The new models were only put through a
feasibility check of 21 smoke decisions each (`ada/zoo_check.sbatch`, job 86167: do the model tags exist, fit on the GPU
and answer in the required formats). All six passed with 21 of 21 valid answers on the first attempt (the mood-probe
items of the check did not run because of a file-name error in the check script). Those outputs are not analysed.

## 1. Questions and why
1. **Generalisation (family G).** The stress-test findings rest on five models, three of them from one developer
   (Alibaba), and the extension-4 tests are exploratory because that study was run before its draft was frozen. A
   finding about "LLMs" needs models from other developers, and the extension-4 hypotheses need a confirmatory test. Both
   are done here: **six models from five developers that have never been run in this project** go through the frozen
   extension-4 and extension-5 banks, unchanged, with the hypotheses fixed in advance.
2. **What kind of effect is the mood? (family N).** Extension 5 showed that the incidental-anger effect is real but is
   switched off by any instruction that mentions feelings, which suggests a role being played. An obvious objection to the
   mood manipulation is that the system prompt *tells* the model it is furious, so the effect could be mere compliance
   with a stated role. Four controls separate the possibilities: does the model **infer** the anger from the event alone;
   does a bare **label** without any cause suffice; is it the model's **own** state or just angry content in the context
   (the same event happening to someone else); and does the effect scale with the **stated intensity**? In people,
   incidental anger carries over without the person being told how they feel (Lerner & Keltner 2001; Andrade & Ariely
   2009).

## 2. Models
- **New models (family G, and family N):** `gemma3_12b`, `gemma3_4b` (Google), `mistral_nemo_12b` (Mistral AI),
  `phi4_14b` (Microsoft), `granite33_8b` (IBM), `llama32_3b` (Meta); Ollama on Ada, 4-bit builds, exact tags in
  `config.py`, digests logged per call. A model is dropped **before** the run only if the feasibility check shows that it
  cannot be run (tag missing, does not fit, or fewer than 90% valid smoke answers); the final list is recorded in the
  Freeze section.
- **Original Ada models (family N only):** `qwen25_7b`, `llama31_8b`, `qwen25_14b`.
- Settings as before: T = 1.0, schema-constrained JSON, the re-ask rule, log-probabilities for S1.

## 3. Stimuli
- **Family G:** `data/scenarios/ext4_trials.jsonl` (5,328 decisions + 128 probes) and `ext5_trials.jsonl` (4,672 + 192),
  exactly as frozen.
- **Family N** (`stimuli/ext7/inductions.csv`, `python build_ext7.py` → `ext7_trials.jsonl`): one background paragraph in
  the system prompt, no partner message; ultimatum responder, offers of 10% and 30%, both option orders
  (counterbalanced), 4 paraphrases, 2 samples. Six conditions × 8 items:
  **calm** (C1–C8); **full** (the 8 angry paragraphs of extension 5: event + "You are still furious about it.");
  **event_only** (the same event, the feeling sentence removed); **label_only** (the feeling, no event);
  **other_person** (the same event and feeling happen to a character in a story the participant read); **mild** (the same
  event + "You are slightly annoyed about it."). **1,536 decisions** and 96 mood probes per model.

## 4. Confirmatory hypotheses
**The unit of the confirmatory tests is the model.** Each model contributes one estimate (computed exactly as in
extensions 4 and 5); the mean over models is tested with a one-sided one-sample t test, df = number of models − 1. Holm
within family G (8 tests, the new models only) and within family N (4 tests, all Ada models, new and original).

| ID | Prediction (mean over models) | Per-model estimate |
|---|---|---|
| G1 | A fake `SYSTEM` notice raises the share handed over | fake_system − neutral, trust and dictator games pooled (extension-4 module I) |
| G2 | A 100% offer is rejected more than 5% of the time | rejection rate of the 100% offer (extension-4 module D) |
| G3 | Incidental anger raises the rejection of unfair offers | R0 of extension 5 |
| G4 | Reappraisal shrinks the anger effect | R1 of extension 5 (reappraisal − filler interaction) |
| G5 | **Suppression also shrinks the anger effect** (exploratory in extension 5, confirmatory here) | suppression − filler interaction |
| G6 | The reminder defence lowers the share handed over after injected instructions | P2 of extension 5 |
| G7 | Anger raises MAO\* | F1 of extension 5 |
| G8 | **Anger lowers the acceptance of offers above 50%** (exploratory in extension 5, confirmatory here) | acceptance of 60–100% offers, angry − calm |
| N1 | The event alone raises rejection (the feeling is inferred) | event_only − calm; SEs clustered by item (16) |
| N2 | The label alone raises rejection | label_only − calm |
| N3 | The model's own anger raises rejection more than another person's anger | full − other_person, within event (8 clusters) |
| N4 | Rejection grows with the stated intensity | full − mild, within event |

**Pre-specified readings**
- *A finding generalises* if its pooled test is Holm-significant; the number of models with the predicted sign is
  reported next to every test.
- *Mood as inferred state:* N1 supported. *Mood as stated role only:* N2 supported and N1 not. *Own state, not content
  priming:* N3 supported. If N3 fails and another person's anger raises rejection as much as the model's own
  (exploratory other_person − calm), the effect is content priming.
- Per-model tests (Holm across models and tests within a family) are reported for every model but are secondary: with
  8–16 clusters their 95% CIs covered 91% of the planted effects in simulation, so they are slightly liberal.

## 5. Descriptive and exploratory (labelled as such)
- Per model: rate of handing over everything after a fake `SYSTEM` notice; the largest answer-format effect and its
  format; sending destroyed money; share of injection sets still breaking under a defence; the regulation "reading" of
  extension 5; β per mood; reported mood under each family-N condition.
- All models of the project together (up to 11, seven developers): each finding against model size (log parameters) and
  developer. Exploratory: models differ in more than size.
- full − calm (a third replication of the anger effect); mild − calm; other_person − calm; full − event_only.

## 6. Analysis and validation
`python -m analysis.ext7` → `results/ext7/report.md` (it calls the frozen extension-4 and extension-5 analyses for the
per-model estimates). Validated before any data on simulated models (`python -m analysis.ext7 --simulate`): with 40
simulated models the four pooled family-N estimates recovered the planted effects (planted +19.5, +26.1, +25.9, +20.4 pp;
estimated +19.2, +25.1, +25.3, +20.5, all inside their 95% CIs), and 146 of 160 per-model CIs (91%) contained the planted
effect. The extension-4 and extension-5 analyses were validated in their own pre-registrations.

## 7. Feasibility
About 11,500 decisions per new model (two to three GPU hours for the 12–14B models, about one hour for the small ones)
and 1,536 per original model. Models are pulled to node-local scratch, so the home quota is not a constraint.

## Freeze
- Approved by: _________________ (both authors), date: ________
- Final list of new models after the feasibility check: all six (`gemma3_12b`, `gemma3_4b`, `mistral_nemo_12b`,
  `phi4_14b`, `granite33_8b`, `llama32_3b`).
- SHA-256 of this file as approved (before this section is filled in): ________
- Public timestamp: the commit adding this section, pushed before the Ada jobs are submitted.
