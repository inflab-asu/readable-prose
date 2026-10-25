---
name: readable-prose
description: Find and fix the six sentence constructions that make AI-written or AI-edited English hard for people to read. The six are rare word combinations, long dependencies, dropped "that" in object relative and complement clauses, stacked noun compounds, nouns used as verbs, and inanimate subjects with animate verbs. Use this skill whenever the user asks to make text clearer, easier to read, less dense, or less AI-sounding; mentions cognitive load, processing difficulty or readability; asks to review, polish or proofread a paper, proposal, report, README, design doc, email or post that was drafted or edited with an AI model; or wants tracked changes for such fixes. Also use it as a last pass on any long prose you wrote yourself. It keeps the register (scientific, legal, technical) and never dumbs the text down.
---

# Readable prose

Frontier models write English that readers find harder to process than human writing, even when every sentence is correct. A 2026 psycholinguistic study traced this to six constructions that are known to slow readers down (`references/paper.md`). Nine frontier models used them more than human writers did, and more than paraphrases of the models' own text that keep the meaning but change the wording. The likely cause is pressure toward short, information-dense output during post-training. The study's own small experiment shows that a length penalty alone teaches a model to drop optional words such as "that".

The cost falls on the reader. Each construction makes the reader hold something in memory, guess at a structure, or reread. A reviewer who rereads a sentence thinks less of the paper.

This skill is a check-and-fix pass with judgement. It finds instances of the six constructions, decides which ones actually cost the reader, and fixes them with the smallest change that keeps the meaning and the register. It does not rewrite a text into plain or chatty English. For the study, its measures and its caveats, read `references/paper.md`.

## The six constructions

### 1. Rare word combinations
A pair of words that rarely or never occur together in ordinary writing, so the reader cannot predict the second from the first. Models coin these when they compress: a verb paired with an object it does not usually take, an adjective on a noun it does not fit, a metaphor nobody uses.
- Spot it by asking whether a careful human writer in this field would put these two words together. "An open session can outlive a change", "the refused rows of the table", "a model of the command" (meaning what the command does), "de-risk the onboarding surface".
- Fix it with the ordinary collocation that means the same: "survive a change", "the refused requests in the table".
- Leave it when it is a defined term of the document or a standard term of the field, even if outsiders find it odd. Change a defined term only if the document uses it inconsistently.

### 2. Long dependencies
A long distance between words that depend on each other: a subject far from its verb, a verb far from its object or complement, or a long clause before the main clause starts. The reader has to hold the open part in working memory (dependency locality, Gibson 1998).
- Spot it in sentences over about 30 words, in a subject that carries a relative clause or an inserted phrase ("A process that the command leaves running, the other case of challenge 3, stays ..."), in a "because" or "so" clause that arrives only at the end of a long sentence, and in a "not X but Y" or "X, unlike Y, and Z" chain.
- Fix it by moving the heavy part after the verb, splitting the sentence at its second idea, or stating the reason first: "Each worker reports its progress before it takes the next task, so the scheduler preempts within milliseconds" rather than "The scheduler preempts within milliseconds, not after seconds as a batch queue does, because each worker reports its progress before it takes the next task."
- Leave it when the sentence is long but each dependency is short, such as a list of parallel clauses each with its subject next to its verb.

### 3. Dropped "that"
An object relative clause without its relativizer ("the policy you are considering", "nothing the system covers"), or a complement clause without its complementizer after a verb of saying, showing or knowing ("The results show the cache helps"). Dropping the optional word saves a token and costs the reader a moment of misparsing. The study's length-penalty experiment trained exactly these two alternations.
- Spot it as a noun followed directly by a new subject and its verb, or as a verb such as show, mean, note, find, assume or ensure followed directly by a clause.
- Fix it by putting "that" (or "which") back: "the policy that you are considering", "show that the cache helps".
- Leave it in very short, informal clauses where "that" sounds stiff ("the book I read"), and in quoted speech.

### 4. Stacked noun compounds
Three or more nouns in a row, each modifying the next: "brokerage money market funds", "reader-patience budget", "GPU memory fragmentation mitigation strategy". The reader has to work out how the nouns relate, and there are many possible bracketings.
- Spot it as a run of nouns before a head noun, including hyphenated nouns used as modifiers.
- Fix it by turning modifiers into a prepositional phrase or a clause: "money market funds at a brokerage", "how much patience the reader has", "a strategy to reduce fragmentation of GPU memory".
- Leave established terms alone: "network interface card", "write-ahead log", "solid state drive", "money market fund". The test is whether a reader in the field has met the whole phrase as one term, or whether the document defines it.
- Watch for the garden path that noun stacks invite: a verb that first reads as one more noun in the compound. "The benchmark times each stage" first parses "benchmark times" as a noun phrase, and "as its peak memory and CPU need" reads "CPU need" as a noun. Rephrase so the verb cannot be read as a noun ("The benchmark measures the time of each stage"). The same trap appears when a verb collides with a key noun of the document, such as "the documentation fixes the names" in a paper about fixes.

### 5. Nouns used as verbs
A noun turned into a verb on the spot: "calendar it", "footnote it", "ticket this", "spreadsheet the results", "categorize movies as speed-runnable". The reader must work out what action the writer means (Clark and Clark 1979).
- Spot it as a word you know as a noun in a verb position, usually with an object right after it.
- Fix it with a verb that names the action: "put it on the calendar", "mention it in a footnote", "file a ticket for this".
- Leave established denominal verbs alone: email, text, google, bottle, cache, log, host, script, version (in software). The paper counts as costly only the ad hoc ones a reader has not met as verbs.

### 6. Inanimate subjects with animate verbs
A thing as the subject of a verb that normally needs a person, so the sentence reads as a metaphor: "is_file() swallows that and returns False", "puzzle patterns where this asymmetry bites", "the kernel already knows which file", "the worker learns of a change", "the policy decides on the object". Every model in the study over-used this one, against both human text and paraphrase.
- Spot it as a verb of perception, cognition, intention, speech or emotion (sees, knows, learns, decides, wants, asks, tells, claims, cares, swallows, bites) whose subject is software, a document, an abstraction or an object.
- Fix it with the literal verb that says what happens: "is_file() catches the exception", "the kernel has already resolved which file", "the worker receives the system call", "the policy checks the object".
- Leave literal agentive verbs alone. In technical writing, components act: "the scheduler preempts the task", "the server rejects the request", "the controller rolls the deploy back", "the filter drops the packet". Leave verbs of reporting on documents ("the reply lists", "Table 2 shows"), and organizations as agents ("the company announced").

## Judgement

Most of the work is deciding what not to change. Apply these principles to every candidate.

- **Keep the register.** A scientific, legal or technical text stays one. Readability here means the reader parses each sentence once. It does not mean short words, chatty phrasing or a lower level of precision. If the user writes in a formal style, every fix stays formal.
- **Keep the meaning and every claim.** A fix must not add, drop or weaken a claim, change a number or a term, or change who does what. If the clearer sentence would say something slightly different, flag it and leave the choice to the author.
- **Keep the document's terms.** A defined term stays as defined everywhere. A fix that swaps one term for a synonym creates a new problem.
- **Leave clean sentences alone.** A sentence with none of the six constructions stays exactly as it is, even if you would have phrased it differently. Do not reorder paragraphs, merge sentences, delete sentences or add new claims unless the user asked for a broader edit. A readability pass that rewrites everything is hard to review, and every extra change risks the meaning.
- **A fix must read naturally in its genre.** Choose the plain verb that a careful writer in the field would use ("the scheduler chooses the replica", not "the scheduler bases its decision on the replica"). In casual genres such as email, chat and informal docs, restore "that" only where the clause is long or could be misread; "the quote we budgeted" is fine in an email. If your fix sounds stiffer than the original, rephrase the sentence another way or leave it.
- **Prefer the smallest fix.** Insert "that", move one phrase, replace one verb, split one sentence. Rewrite a sentence only when smaller fixes would not remove the cost.
- **Do not make the text longer than it needs to be.** Restoring "that" or splitting a sentence adds a word or two, which is fine. Adding explanation is not part of this pass.
- **Check the fix for new problems.** A split can create a dangling "this", and a replacement verb can form a new rare combination. Reread the fixed sentence with its neighbors.
- **Respect the author's own deliberate choices.** If a sentence matters to the author, such as a title or a key-insight sentence, offer the fix rather than applying it silently.

## Procedure

1. **Establish scope and register.** Note the genre (paper, proposal, docs, email), the audience and the house style. If the user has a style guide or a writing skill, such as a paper-writing skill, load it too and obey its rules in every fix.
2. **Get a candidate list** for anything longer than about 300 words. For a shorter text, such as a message, an email or one paragraph, skip the script and the reference files unless you are unsure about a case; reading every sentence is faster and enough. Otherwise run `python3 <this skill>/scripts/find_candidates.py FILE` on a .tex, .md or .txt file (add `--json` for machine-readable output). It strips LaTeX or Markdown markup, splits sentences, and reports candidates by construction with line numbers. It always runs pattern checks, and adds checks on spaCy's dependency parse when spaCy and `en_core_web_sm` are installed (`pip install spacy && python -m spacy download en_core_web_sm`). On a 2,900-word paper section with 36 verified findings of the five kinds it targets, the patterns flagged 39 sentences and covered 27 findings, and spaCy raised that to 63 sentences and 30 findings. So treat the output as places to look, not as verdicts. The script never judges rare word combinations, and it misses some long dependencies and figurative verbs.
3. **Read every sentence.** Go sentence by sentence through the scope and check each one against all six constructions, whether or not the script flagged it. This step finds most of the real problems. On one systems paper, long dependencies, figurative verbs and rare combinations made up nearly all findings.
4. **Judge each instance** against the Judgement principles. Record the ones you leave alone and why, because the author may ask.
5. **Write the minimal fix,** then reread it in context.
6. **Deliver, scaled to the task.** The report should cost the reader less time than the edit saved them.
   - **A message, an email or a paragraph** (under about 300 words): give the revised text, then two to four short bullets on what changed. Use no table and no counts. Mention something you left alone only if the user would expect a change there.
   - **A section or a whole document:** give a one-line summary with counts by construction, then a table with columns Location, Construction, Before, After and Why, then the revised text or the applied edits. Merge repeats into one row, such as five restored "that"s.
   - **Tracked changes in a LaTeX file:** read `references/tracked-changes.md` and use `scripts/mark_changes.py`, which marks only the changed words and checks that accepting the changes gives the new text and rejecting them gives the original. For Word files, use the docx skill's tracked changes.
   - In every case, name any fix that the author should confirm because it depends on how you read an ambiguous sentence.
7. **For a long document or a high-stakes text** (a paper section, a proposal), read `references/large-documents.md`. It describes a sweep with one finder per construction and independent verifiers, which found 55 candidates in one 2,900-word paper section and kept 48.

For before-and-after pairs from papers, docs and email, and for borderline cases, read `references/examples.md`.

## When you write new text

The same six points apply when you draft. Keep "that" in relative and complement clauses. Put the subject next to its verb, and the reason before the consequence. Explain a noun stack the first time, or avoid it. Use a noun as a verb only if the verb is established. Give software and objects literal verbs. Prefer the phrasing a careful writer in the field would use over a compressed coinage.

## Reference files

- `references/paper.md`: the study, its measures, results by construction and model, the psycholinguistic evidence with citations, the length-penalty experiment, its limitations, and a BibTeX entry. Read it when the user asks about the evidence or wants to cite it.
- `references/examples.md`: before-and-after pairs for each construction, drawn from technical papers, documentation, code comments and email, plus cases to leave alone. Read it when unsure whether something counts or how to fix it.
- `references/tracked-changes.md`: LaTeX macros for blue added and struck deleted text, and how to use `scripts/mark_changes.py` to apply, check, accept or reject them.
- `references/large-documents.md`: the multi-pass sweep for long texts, with a workflow template.
