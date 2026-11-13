# Related-work and novelty check (13 Nov 2026)

Searched: web, arXiv API, Crossref DOIs; full text read for EAI and Aher et al. (Semantic Scholar was rate-limited, so
coverage is broad but not exhaustive). Every entry below was matched to an arXiv, NeurIPS or Crossref record.

## Closest work and how we differ
| Work | What they did | Difference from this project |
|---|---|---|
| Mozikov et al. (2024). EAI: Emotional decision-making of LLMs in strategic games and ethical dilemmas. NeurIPS 37, doi 10.52202/079017-1709 (cited) | Emotion put into the **model's own** prompt (incl. a "co-player-based" variant); Dictator, UG, repeated PD, Battle of the Sexes; GPT, Claude, LLaMA-2 and others | No counterpart message, no Trust game, no manipulation check of recognition, no message/paraphrase sampling, no pre-registration |
| Luca, Singh & Lepri (2026). Deal me maybe: The role of emotions in multi-agent negotiation. arXiv:2608.06922 (preprint; add) | Buyer and seller agents each given an emotion; free-form price negotiation; angry buyers almost never close deals but extract the steepest concessions | Emotion only implicit in dialogue, both sides conditioned, payoffs not fixed, no inferential tests or pre-registration |
| Aher, Arriaga & Kalai (2023). ICML; arXiv:2208.10264 (cited) | UG replication; reads acceptance as P("accept") vs P("reject") | **Precedent for our log-probability value signal** (P18): credit them; new here is P(accept) by counterpart emotion |
| Shin et al. (2026). arXiv:2608.27465 (preprint; add) | User-expressed distress makes models endorse risky decisions more (d = 0.51) | Counterpart emotion shifts outputs, but in advice, not economic games |
| Liu et al. (2025). Outraged AI. arXiv:2510.17880 (preprint; optional) | Model's self-reported emotion drives third-party punishment | Model's own emotion; different game |
| Yan, Zhu & Zhu (2026). arXiv:2602.00769; Ou et al. (2025). arXiv:2505.17053 (preprints; optional) | Trust-game priors and personas | No emotion manipulation |
| Xie et al. (2024). NeurIPS (cited) | LLM agents and human trust behaviour | No emotion manipulation |

Not used: Long et al. (2025, arXiv:2509.04310, EvoEmo), because a reported detail could not be confirmed in the paper;
Murashige & Ito (2025), because the content could not be read.

## Novelty statement (for the report)
> Prior work has shown that emotions induced in the model itself, including emotions directed at a co-player (Mozikov et
> al., 2024), or emotions assigned to both agents in free-form price negotiation (Luca et al., 2026), change LLM play. To
> our knowledge, this is the first study to hold payoffs fixed and vary only the emotion that the *counterpart* expresses,
> across Ultimatum, Dictator and Trust-game roles, with open-weight models, manipulation checks and pre-registered
> replications. Its most robust result, that a counterpart's anger lowers the amount an LLM entrusts, has not been
> reported before, to our knowledge.

Nothing found pre-empts or contradicts the anger → trust result.
