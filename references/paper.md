# The study behind this skill

Thomas Hikaru Clark (New York University), Matias B. Martin and Kyle Mahowald (The University of Texas at Austin).
"Why is AI-generated language so hard to understand?" arXiv:2610.29162v1, 21 October 2026.
https://arxiv.org/abs/2610.29162

## Contents
1. Question and design
2. The six measures and their results
3. Why each construction costs a reader
4. Differences between models
5. The length-penalty experiment
6. Explanation the authors propose
7. Limitations
8. How to cite

## 1. Question and design
Readers often find frontier-model prose hard to follow even when it is correct. The paper asks which syntactic and lexical features cause this, and whether post-training explains them.

- **Models.** Nine frontier and near-frontier models: Claude Sonnet 5, Opus 5, Opus 5.5 and Fable 5; GPT-5.6 Luna, Terra and Sol; and the open-weight GLM-5 and Kimi K2.5. Smaller Llama 3.1 8B and Olmo 3 7B variants serve as comparisons.
- **Domains.** Chat, coding, and single-prompt essays.
- **Round-trip baseline.** Each model sentence is translated from English to Japanese and back with NLLB-200. The round trip keeps the meaning and changes the wording, so a feature that drops after it is one the model chose over an available alternative.
- **Human reference.** OpenSubtitles for chat, StackExchange for coding, PERSUADE 2.0 student essays for essays, and Wikipedia as an extra reference.

## 2. The six measures and their results
| Construction | How the paper measures it | Result |
|---|---|---|
| Rare word combinations | Unattested bigrams per 1,000 pairs against a reference corpus, and trigram perplexity from a KenLM model | Almost all frontier models have more unattested bigrams and higher perplexity than their paraphrases, and all nine use more low-frequency n-grams than human text |
| Long dependencies | Mean dependency arc length, standardized for sentence length | Longer than paraphrase in conversation for most models; unchanged or slightly longer in essays |
| Object relative clauses | Rate of object relatives with and without a relativizer ("that", "which") | Reduced object relatives over-used and full ones under-used against paraphrase |
| Stacked noun compounds | Rate of three or more nouns in a modifier chain, from the dependency parse | Over-used in conversation by most models; significant in essays for only two |
| Denominal verbs | Verbs whose lemma is mostly a noun in human text, judged by an automated classifier | Largely over-used against paraphrase, with smaller effects in essays |
| Inanimate subjects with animate verbs | Inanimate, pronoun or code-span subjects of active verbs, judged by the same classifier | Over-used against both paraphrase and human text by all nine models |

Effects are generally smaller in essays than in chat and coding.

Examples the paper quotes from model output: "the cell phone policy you are considering" (reduced object relative), "brokerage money market funds" (noun stack), "categorize movies as speed-runnable or not" (denominal verb), "`is_file()` swallows that and returns False", "Puzzle patterns where this asymmetry bites" and "A song doesn't ask you to turn melancholy into a calendar item" (inanimate subjects with animate verbs).

## 3. Why each construction costs a reader
The paper grounds each measure in psycholinguistic work.
- **Predictability.** Readers process unexpected words more slowly (surprisal; Levy 2008; Smith and Levy 2013).
- **Dependency length.** Holding an unfinished dependency in memory costs effort, and longer distances cost more (Gibson 1998, 2000; Grodner and Gibson 2005; Futrell et al. 2015).
- **Object relative clauses.** Object relatives are harder than subject relatives (Staub 2010; Mak et al. 2006; Reali and Christiansen 2007). The paper frames dropping the relativizer as skipping an optional word, tied to work on uniform information density.
- **Noun compounds.** The relation between the nouns must be inferred, and longer stacks have many possible bracketings (Lauer 1995; Nakov and Hearst 2005; Staub et al. 2007; Cohen and Staub 2014).
- **Denominal verbs.** An innovative verb must be interpreted from context (Clark and Clark 1979), and a word in an unexpected category slows reading (Thierry et al. 2008; Federmeier et al. 2000; Frazier and Rayner 1987).
- **Animacy.** Verbs select for animate subjects, and a violation slows or disrupts processing (Chomsky 1965; Trueswell et al. 1994; Kim and Osterhout 2005; Kuperberg 2007).

## 4. Differences between models
Claude Opus 5.5 is lower than Opus 5 on nearly every difficulty-linked measure in every setting, 19 of 21 comparisons, with non-overlapping intervals in eight. The Llama models and the Olmo base and Instruct models change least under round-trip translation. Olmo Think, trained with reasoning post-training, patterns with the frontier models.

## 5. The length-penalty experiment
The authors fine-tuned Qwen2.5-1.5B-Instruct with GRPO to turn JSON event descriptions into English sentences, with a length penalty and an optional KL term toward the base model.
- The trained alternations were the dative, the object relative with "that", and the complement clause with "that". A particle alternation with no length difference served as a control.
- Preference for the shorter variant rose with the length penalty. Without KL regularization, both "that" alternations were over 98% short at every penalty above zero.
- The preference transferred to held-out near alternations ("sure (that)", "so (that)"). Among far alternations it transferred only to the genitive, and only without KL.
- The authors present this as a proof of concept, not a demonstration of the mechanism in frontier models.

## 6. Explanation the authors propose
Human language balances ease of production against ease of comprehension, and readers benefit when information is spread evenly (uniform information density). Post-training with verifiable rewards (math, code, reasoning) rewards correct answers rather than clear ones, and limited context windows reward compression. Together these may push models toward information-dense constructions that cost readers. Human-feedback training tends to reward longer outputs, so the authors think compression pressure more plausibly comes from verifiable-reward training. They suggest that model developers reward effective communication, for example with preference optimization based on uniform information density.

## 7. Limitations
- A subset of models, and English only.
- A limited number of conversation seeds (chat topics and code repositories).
- No causal claim about frontier models, because their post-training cannot be studied directly. The fine-tuning experiment is a proxy at small scale.
- The paper describes model output. It does not give writers a style guide, and it does not show that every instance of a construction hurts. This skill turns its measures into a checklist, and the judgement about which instances to fix is the skill's, not the paper's.

## 8. How to cite
```bibtex
@misc{clark2026hard,
  title         = {Why is {AI}-generated language so hard to understand?},
  author        = {Clark, Thomas Hikaru and Martin, Matias B. and Mahowald, Kyle},
  year          = {2026},
  eprint        = {2610.29162},
  archivePrefix = {arXiv},
  url           = {https://arxiv.org/abs/2610.29162}
}
```
