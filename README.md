# readable-prose

A Claude skill that finds and fixes the sentence constructions that make AI-written or AI-edited English hard to read, without dumbing the text down.

Text from language models is often grammatical and still slow to read. A 2026 psycholinguistic study (Clark, Martin and Mahowald, arXiv 2610.29162) traced this to six constructions that readers are known to process slowly, and found that frontier models use them more than human writers do:

1. rare word combinations ("the cache pays rent only for hot keys")
2. long dependencies between a subject and its verb, or a verb and its object
3. a dropped "that" in object relative and complement clauses ("the policy you are considering")
4. stacked noun compounds ("user session timeout configuration file")
5. nouns used as verbs ("can you calendar it")
6. inanimate subjects with animate verbs ("the linter hates trailing commas")

The skill checks a text for these, decides which instances actually cost the reader, and fixes each with the smallest change that keeps the meaning, the claims and the register. It leaves clean sentences, established terms and literal technical verbs alone. Its report scales to the task, so a short message gets a short reply.

## What's in it

```
readable-prose/
├── SKILL.md                    # the procedure and the judgement rules
├── references/
│   ├── paper.md                # the study, its measures and its caveats
│   ├── examples.md             # before-and-after pairs, and fixes that made things worse
│   ├── tracked-changes.md      # showing edits as tracked changes (LaTeX, Markdown, Word)
│   └── large-documents.md      # sweeping a long document with parallel finders
├── scripts/
│   ├── find_candidates.py      # flags candidate sentences for review
│   └── mark_changes.py         # applies fixes as tracked changes, accepts or rejects them
└── evals/                      # test cases with graders
```

## Install

Copy the folder into your skills directory, for example `~/.claude/skills/readable-prose`. The skill works without the scripts. `find_candidates.py` needs Python 3. It works better with spaCy (`pip install spacy && python -m spacy download en_core_web_sm`) and falls back to simpler heuristics without it.

## License

MIT
