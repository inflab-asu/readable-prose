# Sweeping a long or high-stakes document

A single read through a long text misses instances, and the reader who wrote or edited the text is the worst judge of it. For a paper section, a proposal or anything over about 2,000 words, split the work: separate finders for each construction, then independent verifiers.

## Contents
1. The pattern
2. What it found on one paper section
3. Running it with subagents
4. A workflow template

## 1. The pattern
1. **Freeze the text.** Copy the file, so every agent reads the same version and the exact spans stay valid.
2. **Write a brief.** Give the six definitions (from SKILL.md), the register, the house style or writing rules, the document's defined terms, and the judgement rules for the genre, such as which component-as-actor verbs are normal.
3. **Find, one construction per finder.** Six finders each read every sentence for one construction only. Each returns exact old spans, a minimal fix, the sentence, why it costs a reader, a severity, and the borderline cases it chose not to flag. A finder that looks for one thing reads differently from one that looks for everything.
4. **Merge.** Merge findings with identical spans, and keep both fixes when two finders disagree.
5. **Verify from three angles.** Three verifiers each judge every finding, independently, and answer three questions: is it an instance, is it worth fixing, and is the fix acceptable. Each can also propose a better fix.
   - A **linguist** checks that the finding fits the definition, that it costs a reader, and that the fix is the smallest one.
   - A **technical checker** checks that the fix keeps the meaning, every claim and every defined term, and it may veto.
   - A **register and house-style reader** checks that the fix keeps the genre's register, obeys the author's rules and adds no needless length.
   Keep a finding when at least two verifiers say yes to all three questions and the technical checker does not veto it.
6. **Merge overlapping fixes per sentence.** Several kept findings often touch one sentence, and these need one combined wording. Prefer a verifier's improved fix where one exists.
7. **Apply and check.** Apply the fixes with `scripts/mark_changes.py` if the user wants tracked changes, then build or render the document and reread the changed sentences.

## 2. What it found on one paper section
A 2,900-word design section of a systems paper, drafted with AI help:

| Construction | Findings | Kept |
|---|---|---|
| Long dependencies | 22 | 19 |
| Inanimate subjects with animate verbs | 14 | 14 |
| Rare word combinations | 14 | 12 |
| Dropped "that" | 4 | 3 |
| Nouns used as verbs | 1 | 0 |
| Stacked noun compounds | 0 | 0 |

The kept findings merged into 29 edits. The verifiers rejected replacing a phrase with a synonym that collided with one of the paper's defined terms. They also rejected changing "the controller decides", which is standard systems phrasing. Technical prose is dominated by the first three constructions. Chat and code explanations may show more noun stacks and nouns used as verbs.

## 3. Running it with subagents
With an agent tool, launch the six finders in one message so they run in parallel. Give each the brief, the frozen file and its one construction, and ask for structured output. Then launch the three verifiers in one message, each with the merged list. Without subagents, do the same passes yourself in sequence: one read per construction, then one read per verifier lens. This is slower, but still better than a single combined read.

## 4. A workflow template
For an environment with a Workflow tool, and only when the user has opted into multi-agent orchestration, this script runs the sweep. Adapt the paths, the brief, and the lens texts to the document.

```javascript
export const meta = {
  name: 'readable-prose-sweep',
  description: 'Find the six hard-to-read constructions in a document, then verify every finding from three angles',
  phases: [{ title: 'Find' }, { title: 'Verify' }],
}
const FILE = args.file, BRIEF = args.brief          // a frozen copy of the text and a brief file
const KINDS = ['rare word combinations', 'long dependencies', 'dropped "that" in object relative and complement clauses',
  'stacked noun compounds', 'nouns used as verbs', 'inanimate subjects with animate verbs']
const FIND = { type: 'object', properties: { findings: { type: 'array', items: { type: 'object', properties: {
  old: { type: 'string' }, new: { type: 'string' }, sentence: { type: 'string' }, why: { type: 'string' },
  severity: { type: 'string', enum: ['high', 'medium', 'low'] } }, required: ['old', 'new', 'sentence', 'why', 'severity'] } },
  checked_but_fine: { type: 'array', items: { type: 'string' } } }, required: ['findings', 'checked_but_fine'] }
phase('Find')
const found = await parallel(KINDS.map(k => () => agent(
  `Read ${BRIEF}. Then read ${FILE} sentence by sentence and find every instance of: ${k}. Give the exact old span (unique, copied character for character), a minimal fix, the sentence, why it costs a reader, and a severity. List borderline cases you left alone. Do not edit files.`,
  { label: `find:${k.split(' ')[0]}`, phase: 'Find', schema: FIND }).then(r => (r?.findings || []).map(f => ({ ...f, kind: k })))))
const byOld = new Map()
for (const f of found.filter(Boolean).flat()) {
  const key = f.old.replace(/\s+/g, ' ').trim()
  if (!byOld.has(key)) byOld.set(key, { ...f, kinds: [f.kind], alternatives: [] })
  else { const g = byOld.get(key); g.kinds.push(f.kind); if (f.new !== g.new) g.alternatives.push(f.new) }
}
const items = [...byOld.values()].map((f, i) => ({ id: `F${i + 1}`, ...f }))
const VER = { type: 'object', properties: { verdicts: { type: 'array', items: { type: 'object', properties: {
  id: { type: 'string' }, is_instance: { type: 'boolean' }, worth_fixing: { type: 'boolean' }, fix_ok: { type: 'boolean' },
  better_new: { type: 'string' }, reason: { type: 'string' } }, required: ['id', 'is_instance', 'worth_fixing', 'fix_ok', 'better_new', 'reason'] } } }, required: ['verdicts'] }
const LENSES = {
  linguist: 'Judge as a psycholinguist: is each finding the named construction, does it cost a reader, is the fix minimal?',
  accuracy: 'Judge as the technical checker: does each fix keep the meaning, every claim and every defined term? Mark fix_ok false if not.',
  register: 'Judge as a reader of this genre with the author\'s style rules: does each fix keep the register and the rules, without needless length?',
}
phase('Verify')
const verdicts = await parallel(Object.entries(LENSES).map(([lens, text]) => () => agent(
  `Read ${BRIEF}. ${text} Source: ${FILE}. Judge every finding independently: ${JSON.stringify(items)}`,
  { label: `verify:${lens}`, phase: 'Verify', schema: VER }).then(r => ({ lens, verdicts: r?.verdicts || [] }))))
return { items, verdicts }
```
After it returns, count the votes per finding, keep the ones with at least two yes votes and no accuracy veto, merge the overlapping fixes per sentence, and apply them.
