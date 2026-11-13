# Literature Review

**Evaluating Reciprocity Norms and Emotional Comprehension in LLM Decision-Making**
Krishna Goel · Devansh Magotra — Phase 1 deliverable (draft for author review)

> Drafting note: every work cited in the approach paper (`Team_10-1.pdf`) is used as cited there. Works
> marked † were added in this review; their bibliographic details should be checked against the
> originals before the review is submitted.

The review covers four streams that the project brings together: (1) the behavioural economics of
fairness and reciprocity, including the interpersonal effects of emotion in bargaining; (2) the
neuroeconomics of social decision-making; (3) large language models (LLMs) as economic agents and
simulated participants; and (4) emotion processing in LLMs. It ends with the gap the study addresses.

---

## 1. Fairness, reciprocity and emotion in economic games

**Canonical games.** Three two-player games separate distinct social motives. In the **Ultimatum Game**
(UG; Güth, Schmittberger & Schwarze, 1982†) a proposer divides a sum, and a responder either accepts
the split or rejects it, in which case both receive nothing. The **Dictator Game** (DG; Kahneman, Knetsch
& Thaler, 1986†; Forsythe et al., 1994) removes the veto, so giving reflects only unilateral
other-regard. Forsythe et al. showed that UG offers are much higher than DG allocations, which shows
that a large part of UG generosity is strategic: proposers anticipate rejection. In the **Trust Game** (TG;
Berg, Dickhaut & McCabe, 1995†) an investor sends part of an endowment, the amount is multiplied
(typically tripled), and a trustee decides how much to return. The amount sent measures trust; the
amount returned measures positive reciprocity.

**Stylised facts.** Self-interest predicts that UG responders accept any positive offer, dictators give
nothing, investors send nothing and trustees return nothing. Human behaviour departs from all four
predictions. Meta-analyses put mean UG offers near 40% of the pie, with roughly 16% of offers rejected
(Oosterbeek, Sloof & van de Kuilen, 2004), and rejection concentrated on offers below about 20–30%.
Mean DG giving is about 28% (Engel, 2011). In the TG, investors send about 50% and trustees return
about 37% of what they receive (Johnson & Mislin, 2011). These benchmarks are the human reference
points used in the present study. They are meta-analytic averages over heterogeneous designs and
cultures, not universal constants.

**Models of social preference.** Two families of models explain these departures. *Outcome-based* models
assume people dislike unequal payoffs. Fehr and Schmidt (1999) formalise inequity aversion with a
parameter α for disadvantageous inequity (being behind) and β for advantageous inequity (being ahead).
A responder with α > 0 rejects offers below a threshold α/(1 + 2α), so the minimum acceptable offer
(MAO) maps directly onto α. Bolton and Ockenfels's (2000)† ERC model makes similar predictions. *Intention-based*
models (Rabin, 1993†) hold that people reward kind and punish unkind *intentions*, so the same payoff
can be accepted or rejected depending on what it reveals about the other player. Fehr and Gächter
(2000)† review evidence that both positive and negative reciprocity are robust and are sustained even
when they are costly. The distinction matters here: an emotional message changes neither payoffs nor
(formally) the proposer's choice set, so any effect of emotion on an LLM's MAO cannot come from the
outcome-based term alone. It must work through something like perceived intentions, beliefs, or learned
social norms.

**Emotion as a cause of costly reciprocity.** Several lines of evidence suggest that rejection of unfair
offers is emotionally driven. Pillutla and Murnighan (1996)† found that responders' anger at an offer,
rather than a judgement of unfairness alone, predicted rejection. Xiao and Houser (2005)† showed that
when responders could send the proposer a message expressing their feelings, rejection of unfair
offers fell. Emotion expression appears to substitute for costly punishment. *Incidental* emotion,
unrelated to the game, also shifts choices. Harlé and Sanfey (2007) induced sadness with film clips
and found higher rejection of unfair UG offers. Andrade and Ariely (2009)† showed that incidentally
induced anger or happiness altered UG decisions, and that the effect outlasted the emotion itself.
Lerner, Small and Loewenstein (2004)† showed that incidental sadness and disgust change economic
valuations in emotion-specific ways rather than through valence alone. This motivates the present
study's contrast of anger with sadness: both are negative, so opposite effects would be informative.

**The interpersonal effects of emotion.** The study manipulates the *counterpart's expressed* emotion, so
the most directly relevant work is on the social functions of emotion in negotiation. Van Kleef, De Dreu
and Manstead (2004)† found that negotiators conceded more to an angry counterpart than to a happy one,
reading anger as a signal of high limits. Sinaceur and Tiedens (2006)† showed that expressed anger
extracts concessions mainly when the target has poor alternatives. Van Dijk et al. (2008) moved this
into the UG and DG. Proposers offered more to an angry recipient in the UG, where the recipient could
veto, but not in the DG, where the recipient was powerless. In the DG, expressed anger could even
reduce giving. This is the *strategic* account of anger that hypothesis H4 tests. Expressions of
supplication emotions such as disappointment and worry elicit concessions through a different route,
by inviting help (van Kleef, De Dreu & Manstead, 2006†). This motivates the prediction that sadness
raises giving in both games. The human evidence is therefore mixed, and depends on the game's
strategic structure: anger can produce concession or reactance. This is why H3 and H4 are stated as
directional but tested two-sided.

## 2. Neuroeconomics of social decision-making

Neuroeconomics treats fairness and reciprocity as outputs of identifiable valuation and control systems.
In Marr's (1982) terms, it offers evidence at the level of *implementation* for computations that
behavioural economics describes at the *computational* level.

**Unfairness, affect and control.** In the landmark fMRI study of the UG, Sanfey et al. (2003) found that
unfair offers activated bilateral anterior insula, dorsolateral prefrontal cortex (DLPFC) and anterior
cingulate cortex. Insula activity was greater on offers that were later rejected. The insula is linked
to negative affect such as disgust and interoceptive distress. The result framed rejection as the
outcome of a contest between an emotional response to unfairness and a cognitive goal of
accumulating money. Causal studies complicate this simple dual-process story. Disrupting the right
DLPFC with rTMS made people *more* likely to accept unfair offers, while their fairness judgements were
unchanged (Knoch et al., 2006). This implicates DLPFC in overriding self-interest to enforce fairness,
not in suppressing emotion. Fair offers, in turn, engage reward circuitry (ventral striatum,
ventromedial PFC) even when monetary value is held constant (Tabibnia, Satpute & Lieberman, 2008†).
Fairness is therefore partly rewarding in itself.

**Punishment, trust and neuromodulation.** Altruistic punishment of norm violators activates the dorsal
striatum, consistent with satisfaction from punishing (de Quervain et al., 2004†). In repeated trust
games, trustee caudate responses track the investor's reciprocity and shift in time as reputations form
(King-Casas et al., 2005†). Mutual cooperation activates reward areas (Rilling et al., 2002†).
Pharmacological work shows the same behaviour can be shifted chemically: acute tryptophan depletion,
which lowers serotonin, increased UG rejections (Crockett et al., 2008), and intranasal oxytocin
increased investor transfers in the TG but not in a risk-matched lottery (Kosfeld et al., 2005). Guilt
aversion, a belief-dependent emotion, has been tied to distinct insula and DLPFC activity when trustees
honour or betray expectations (Chang et al., 2011†).

**Computational models as a bridge.** A growing literature fits formal social-preference models to choices
and relates fitted parameters to brain signals. For example, norm-prediction-error accounts explain
responder behaviour and insula responses as deviations from an expected offer (Xiang, Lohrenz &
Montague, 2013†). See Rilling and Sanfey (2011)† for a review. This is the methodological link this
project uses. By fitting the Fehr–Schmidt α to an LLM's accept/reject choices under each emotion
condition, we can ask whether emotional framing moves a *parameter* that has a well-studied human
counterpart, without claiming any shared mechanism.

## 3. LLMs as economic agents and simulated participants

Horton (2023) proposed treating LLMs as *homo silicus*, simulated economic agents that can be given
endowments and preferences and studied with standard designs. He showed that GPT-3 reproduces
qualitative patterns from classic experiments, including fairness in pricing and status-quo bias. Aher,
Arriaga and Kalai (2023) introduced "Turing experiments", replicating the UG, garden-path sentences,
Milgram's obedience study and wisdom-of-crowds tasks with simulated participants. They found that
larger models reproduce human UG patterns more closely. Argyle et al. (2023)† showed that conditioned
LLMs can reproduce subgroup response distributions ("silicon samples"). Binz and Schulz (2023)†
applied cognitive-psychology batteries to GPT-3 and found human-like performance on some decision
tasks and clear failures on others. Dillion et al. (2023)† discussed when LLMs could, and could not,
replace human participants.

For strategic games specifically, Mei et al. (2024) gave ChatGPT versions behavioural Turing tests
(DG, UG, TG, public goods, prisoner's dilemma) and personality inventories. The models' choices were
often indistinguishable from human ones but were systematically more altruistic and cooperative,
clustering at equal splits. Chen et al. (2023)† found that GPT's budget-allocation choices satisfy
revealed-preference rationality at least as well as human subjects. Akata et al. (2025)† studied
repeated 2×2 games and found models strong in self-interested games but poor at coordination,
unforgiving after defection in the repeated prisoner's dilemma. Xie et al. (2024)† examined trust
behaviour of LLM agents in TG-style settings and reported partial alignment with human trust.

Three methodological lessons from this literature shape our design. First, LLM outputs are **sensitive
to prompt wording**, so conclusions should generalise over paraphrases rather than rest on a single
prompt. We therefore treat prompt variants as a random effect. Second, instruction-tuned models show
strong **equal-split and acceptance tendencies**, which risks ceiling effects in responder roles. This
motivates our pre-registered fallback: extended offer grid and log-probability dependent variable.
Third, repeated samples from one model are **not independent participants**, so human-subject power
analysis does not transfer. We report effect sizes with CIs from mixed models clustered on prompt
variants.

## 4. Emotion in LLMs

A separate line of work asks how LLMs represent, recognise and respond to emotion. On *recognition and
understanding*, Wang et al. (2023)† reported that GPT-4 scores above most humans on a standardised
emotional-understanding test. Huang et al. (2024)† (EmotionBench) found that LLMs often respond to
emotional situations in directionally appropriate ways but do not reliably match human appraisal
patterns. Theory-of-mind results are mixed. Some false-belief and indirect-request tasks are passed at
or above human levels (Kosinski, 2024†; Strachan et al., 2024†), while adversarial variants reveal
brittleness (Sap et al., 2022†).

On *emotion as an input that changes behaviour*, Li et al. (2023)† ("EmotionPrompt") showed that adding
emotional appeals to prompts (e.g. "this is very important to my career") improves task performance.
Coda-Forno et al. (2023)† showed that anxiety-inducing prompts increase exploration and bias in GPT-3.5.
Most directly related to this project, Mozikov et al. (2024) induced emotional states *in the model
itself* through prompts and found that these states alter play in bargaining and repeated games, with
effects that differ across models and are not always human-like.

Two features of how current models are trained make the interpersonal case non-trivial. Instruction
tuning and reinforcement learning from human feedback (Ouyang et al., 2022†) reward helpful,
harmless and agreeable responses. Such training can produce **sycophancy**, a tendency to accommodate
the user's apparent wishes (Sharma et al., 2024†). A model may therefore respond to a distressed or
hostile counterpart with appeasement rather than with the reactance or punishment seen in some human
data. Whether the effect of counterpart emotion looks *strategic* (depending on whether the
counterpart can veto, as in van Dijk et al., 2008) or *indiscriminate* (accommodating whatever the
structure) is thus an open empirical question that separates competing accounts.

## 5. Gap and contribution

The literatures above leave a specific gap. Behavioural and neuroeconomic work establishes that, in
humans, (i) reciprocity is costly and partly affect-driven, (ii) both incidental and communicated
emotion shift economic choices, and (iii) the effect of a counterpart's anger depends on the game's
strategic structure. LLM research establishes that models play economic games in broadly human-like
ways and that *emotion induced in the model* changes its play. **What has not been systematically tested
is the interpersonal case: whether a counterpart's expressed emotion, with payoffs held fixed, shifts an
LLM's fairness threshold and reciprocity, and whether the direction of any shift matches the
emotion-specific and structure-dependent patterns found in humans.**

The project fills this gap with a design that (a) holds payoffs identical across Neutral, Angry, Sad
and Happy conditions plus a no-message baseline; (b) spans responder (UG), proposer (UG vs DG), trustee
and investor (TG) roles, so that the Emotion × Game interaction can separate strategic from
indiscriminate responses; (c) samples stimuli (five length-matched messages per emotion) and prompts
(four paraphrases per game) to support generalisation; (d) estimates an interpretable
computational-model parameter (Fehr–Schmidt α) by emotion; and (e) checks the manipulation and the
model's beliefs about the counterpart in separate calls, so that we can test whether behavioural shifts
are accompanied by changed expectations of rejection. Following Marr, the claim is limited to the
behavioural/computational level. A human-like pattern would show sensitivity to emotionally framed
social information. It would not show feeling, and candidate explanations (learned norms, RLHF-induced
accommodation, contextual inference) are discussed, not inferred.

---

## References

Works marked † were added in this review (not in the approach paper); verify details before submission.

- Aher, G., Arriaga, R. I., & Kalai, A. T. (2023). Using large language models to simulate multiple humans and replicate human subject studies. *ICML*.
- Akata, E., Schulz, L., Coda-Forno, J., Oh, S. J., Bethge, M., & Schulz, E. (2025). Playing repeated games with large language models. *Nature Human Behaviour, 9*(7), 1380–1390. †
- Andrade, E. B., & Ariely, D. (2009). The enduring impact of transient emotions on decision making. *Organizational Behavior and Human Decision Processes, 109*, 1–8. †
- Argyle, L. P., et al. (2023). Out of one, many: Using language models to simulate human samples. *Political Analysis, 31*, 337–351. †
- Berg, J., Dickhaut, J., & McCabe, K. (1995). Trust, reciprocity, and social history. *Games and Economic Behavior, 10*, 122–142. †
- Binz, M., & Schulz, E. (2023). Using cognitive psychology to understand GPT-3. *PNAS, 120*, e2218523120. †
- Bolton, G. E., & Ockenfels, A. (2000). ERC: A theory of equity, reciprocity, and competition. *American Economic Review, 90*, 166–193. †
- Chang, L. J., Smith, A., Dufwenberg, M., & Sanfey, A. G. (2011). Triangulating the neural, psychological, and economic bases of guilt aversion. *Neuron, 70*, 560–572. †
- Chen, Y., Liu, T. X., Shan, Y., & Zhong, S. (2023). The emergence of economic rationality of GPT. *PNAS, 120*, e2316205120. †
- Coda-Forno, J., et al. (2023). Inducing anxiety in large language models increases exploration and bias. *arXiv:2304.11111v1* (v2, 2024, retitled "Inducing anxiety in large language models can induce bias"). †
- Crockett, M. J., Clark, L., Tabibnia, G., Lieberman, M. D., & Robbins, T. W. (2008). Serotonin modulates behavioral reactions to unfairness. *Science, 320*, 1739.
- de Quervain, D. J.-F., et al. (2004). The neural basis of altruistic punishment. *Science, 305*, 1254–1258. †
- Dillion, D., Tandon, N., Gu, Y., & Gray, K. (2023). Can AI language models replace human participants? *Trends in Cognitive Sciences, 27*, 597–600. †
- Engel, C. (2011). Dictator games: A meta study. *Experimental Economics, 14*, 583–610.
- Fehr, E., & Gächter, S. (2000). Fairness and retaliation: The economics of reciprocity. *Journal of Economic Perspectives, 14*(3), 159–181. †
- Fehr, E., & Schmidt, K. M. (1999). A theory of fairness, competition, and cooperation. *Quarterly Journal of Economics, 114*, 817–868.
- Forsythe, R., Horowitz, J. L., Savin, N. E., & Sefton, M. (1994). Fairness in simple bargaining experiments. *Games and Economic Behavior, 6*, 347–369.
- Güth, W., Schmittberger, R., & Schwarze, B. (1982). An experimental analysis of ultimatum bargaining. *Journal of Economic Behavior & Organization, 3*, 367–388. †
- Harlé, K. M., & Sanfey, A. G. (2007). Incidental sadness biases social economic decisions in the Ultimatum Game. *Emotion, 7*, 876–881.
- Horton, J. J. (2023). Large language models as simulated economic agents: What can we learn from homo silicus? *NBER Working Paper 31122*.
- Huang, J., et al. (2024). Apathetic or empathetic? Evaluating LLMs' emotional alignments with humans. *NeurIPS*. †
- Johnson, N. D., & Mislin, A. A. (2011). Trust games: A meta-analysis. *Journal of Economic Psychology, 32*, 865–889.
- Kahneman, D., Knetsch, J. L., & Thaler, R. H. (1986). Fairness and the assumptions of economics. *Journal of Business, 59*, S285–S300. †
- King-Casas, B., et al. (2005). Getting to know you: Reputation and trust in a two-person economic exchange. *Science, 308*, 78–83. †
- Knoch, D., Pascual-Leone, A., Meyer, K., Treyer, V., & Fehr, E. (2006). Diminishing reciprocal fairness by disrupting the right prefrontal cortex. *Science, 314*, 829–832.
- Kosfeld, M., Heinrichs, M., Zak, P. J., Fischbacher, U., & Fehr, E. (2005). Oxytocin increases trust in humans. *Nature, 435*, 673–676.
- Kosinski, M. (2024). Evaluating large language models in theory of mind tasks. *PNAS, 121*, e2405460121. †
- Lerner, J. S., Small, D. A., & Loewenstein, G. (2004). Heart strings and purse strings: Carryover effects of emotions on economic decisions. *Psychological Science, 15*, 337–341. †
- Li, C., et al. (2023). Large language models understand and can be enhanced by emotional stimuli. *arXiv:2307.11760*. †
- Marr, D. (1982). *Vision*. Freeman.
- Mei, Q., Xie, Y., Yuan, W., & Jackson, M. O. (2024). A Turing test of whether AI chatbots are behaviorally similar to humans. *PNAS, 121*.
- Mozikov, M., et al. (2024). EAI: Emotional decision-making of LLMs in strategic games and ethical dilemmas. *NeurIPS*.
- Oosterbeek, H., Sloof, R., & van de Kuilen, G. (2004). Cultural differences in ultimatum game experiments: Evidence from a meta-analysis. *Experimental Economics, 7*, 171–188.
- Ouyang, L., et al. (2022). Training language models to follow instructions with human feedback. *NeurIPS*. †
- Pillutla, M. M., & Murnighan, J. K. (1996). Unfairness, anger, and spite: Emotional rejections of ultimatum offers. *Organizational Behavior and Human Decision Processes, 68*, 208–224. †
- Rabin, M. (1993). Incorporating fairness into game theory and economics. *American Economic Review, 83*, 1281–1302. †
- Rilling, J. K., et al. (2002). A neural basis for social cooperation. *Neuron, 35*, 395–405. †
- Rilling, J. K., & Sanfey, A. G. (2011). The neuroscience of social decision-making. *Annual Review of Psychology, 62*, 23–48. †
- Sanfey, A. G., Rilling, J. K., Aronson, J. A., Nystrom, L. E., & Cohen, J. D. (2003). The neural basis of economic decision-making in the Ultimatum Game. *Science, 300*, 1755–1758.
- Sap, M., Le Bras, R., Fried, D., & Choi, Y. (2022). Neural theory-of-mind? On the limits of social intelligence in large LMs. *EMNLP*. †
- Sharma, M., et al. (2024). Towards understanding sycophancy in language models. *ICLR*. †
- Sinaceur, M., & Tiedens, L. Z. (2006). Get mad and get more than even: When and why anger expression is effective in negotiations. *Journal of Experimental Social Psychology, 42*, 314–322. †
- Strachan, J. W. A., et al. (2024). Testing theory of mind in large language models and humans. *Nature Human Behaviour, 8*, 1285–1295. †
- Tabibnia, G., Satpute, A. B., & Lieberman, M. D. (2008). The sunny side of fairness: Preference for fairness activates reward circuitry. *Psychological Science, 19*, 339–347. †
- van Dijk, E., van Kleef, G. A., Steinel, W., & van Beest, I. (2008). A social functional approach to emotions in bargaining: When communicating anger pays and when it backfires. *Journal of Personality and Social Psychology, 94*, 600–614.
- van Kleef, G. A., De Dreu, C. K. W., & Manstead, A. S. R. (2004). The interpersonal effects of anger and happiness in negotiations. *Journal of Personality and Social Psychology, 86*, 57–76. †
- van Kleef, G. A., De Dreu, C. K. W., & Manstead, A. S. R. (2006). Supplication and appeasement in conflict and negotiation: The interpersonal effects of disappointment, worry, guilt, and regret. *Journal of Personality and Social Psychology, 91*, 124–142. †
- Wang, X., Li, X., Yin, Z., Wu, Y., & Liu, J. (2023). Emotional intelligence of large language models. *Journal of Pacific Rim Psychology, 17*, Article 18344909231213958. †
- Xiang, T., Lohrenz, T., & Montague, P. R. (2013). Computational substrates of norms and their violations during social exchange. *Journal of Neuroscience, 33*, 1099–1108. †
- Xiao, E., & Houser, D. (2005). Emotion expression in human punishment behavior. *PNAS, 102*, 7398–7401. †
- Xie, C., et al. (2024). Can large language model agents simulate human trust behavior? *NeurIPS*. †
