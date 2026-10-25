# readable-prose

A skill that finds and fixes the sentences that make AI-written English hard to read.

## Install

Copy the folder into your skills directory, for example `~/.claude/skills/readable-prose`. The skill works without the scripts. `find_candidates.py` needs Python 3. It works better with spaCy (`pip install spacy && python -m spacy download en_core_web_sm`) and falls back to simpler heuristics without it.

## Acknowledge
Text from language models is often grammatical and still slow to read. 
A 2026 psycholinguistic study ([Clark, Martin and Mahowald, arXiv 2610.29162, "Why is AI-generated language so hard to understand?"](https://arxiv.org/pdf/2610.29162v1)) traced this to six constructions that readers are known to process slowly, and found that frontier models use them more than human writers do:

1. rare word combinations ("the cache pays rent only for hot keys")
2. long dependencies between a subject and its verb, or a verb and its object
3. a dropped "that" in object relative and complement clauses ("the policy you are considering")
4. stacked noun compounds ("user session timeout configuration file")
5. nouns used as verbs ("can you calendar it")
6. inanimate subjects with animate verbs ("the linter hates trailing commas")

The skill checks and fixes a text for these.

## License

MIT
