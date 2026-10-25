#!/usr/bin/env python3
"""Find candidate instances of the six hard-to-read constructions in a .tex, .md or .txt file.

The six constructions come from Clark, Martin and Mahowald (2026), "Why is AI-generated language so hard to
understand?" (arXiv 2610.29162). This script only proposes places to look. A person or a model must judge each
candidate, because many matches are fine in context and many real instances are not matched at all. It never
judges rare word combinations, which need a large reference corpus.

The script always runs pattern heuristics. If spaCy and its en_core_web_sm model are installed, it adds checks on
the dependency parse (long arcs, object relatives and complement clauses without "that", compound chains, subjects
of animate verbs). On a 2,900-word systems-paper section with 36 verified findings of the five kinds it targets,
the patterns alone flagged 39 sentences and covered 27 findings; with spaCy it flagged 63 sentences and covered 30.

Usage:
    python3 find_candidates.py FILE [--json] [--max-words 30] [--no-spacy]
"""
import argparse
import json
import re
import sys

# ---------------------------------------------------------------- text extraction

TEXT_CMDS = r"(?:textit|textbf|emph|textsc|textup|texttt|underline|mbox|text|added|footnote|caption|title|section|subsection|subsubsection|paragraph)"


def strip_latex_line(line):
    line = re.sub(r"(?<!\\)%.*$", "", line)                       # comments
    if re.match(r"\s*\\(begin|end)\{", line) and not re.search(r"\\caption", line):
        return ""
    line = re.sub(r"\\deleted\{(?:[^{}]|\{[^{}]*\})*\}", "", line)   # tracked deletions do not print
    line = re.sub(r"\\(?:label|includegraphics|vspace|hspace|bibliographystyle|bibliography|input|include)(?:\[[^\]]*\])?\{[^}]*\}", "", line)
    line = re.sub(r"~?\\(?:cite[tp]?|citet|citep|citeauthor)\{[^}]*\}", " [cite]", line)
    line = re.sub(r"\\S\\ref\{[^}]*\}|\\(?:auto|eq|page)?ref\{[^}]*\}", "§X", line)
    for _ in range(3):
        line = re.sub(r"\\" + TEXT_CMDS + r"\*?(?:\[[^\]]*\])?\{([^{}]*)\}", r"\1", line)
    line = re.sub(r"\\([A-Za-z]+)\{\}", r"\1", line)                  # \SystemName{} -> SystemName
    line = re.sub(r"\\stepcirc\{\d+\}|\\stepmark\{\d+\}", "", line)
    line = re.sub(r"\\[A-Za-z]+\*?(?:\[[^\]]*\])?", "", line)        # other commands
    line = line.replace("~", " ").replace("{", "").replace("}", "").replace("\\", "")
    line = re.sub(r"\$[^$]*\$", "X", line)
    return line


def strip_md_line(line, state):
    if line.strip().startswith("```"):
        state["code"] = not state["code"]
        return ""
    if state["code"]:
        return ""
    line = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", line)
    line = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", line)
    line = re.sub(r"^\s{0,3}(#+|>|[-*+]|\d+\.)\s+", "", line)
    line = re.sub(r"[*_]{1,3}([^*_]+)[*_]{1,3}", r"\1", line)
    if re.match(r"^\s*\|", line):            # tables: keep cells as text
        line = line.replace("|", ". ")
    return line


def extract(path):
    raw = open(path, encoding="utf-8").read().split("\n")
    kind = "tex" if path.endswith(".tex") else "md" if path.endswith((".md", ".markdown")) else "txt"
    state = {"code": False}
    pieces = []  # (start offset, line number)
    text = ""
    for n, line in enumerate(raw, 1):
        clean = strip_latex_line(line) if kind == "tex" else strip_md_line(line, state) if kind == "md" else line
        if not clean.strip():
            text += "\n\n" if text and not text.endswith("\n\n") else ""
            continue
        pieces.append((len(text), n))
        text += clean.strip() + " "
    return text, pieces


ABBREV = r"(?:e\.g|i\.e|et al|etc|Fig|Figs|Sec|Secs|Eq|Eqs|vs|cf|approx|resp|No|Dr|Mr|Ms|Prof)\."


def sentences(text, pieces):
    starts = [p[0] for p in pieces]
    out = []
    for para_m in re.finditer(r"[^\n]+", text):
        para, base = para_m.group(0), para_m.start()
        protected = re.sub(ABBREV, lambda m: m.group(0).replace(".", "\u2024"), para)
        pos = 0
        for m in re.finditer(r"(?<=[.!?])[\"')\]]*\s+(?=[A-Z(\[\"'`§0-9])", protected):
            out.append((base + pos, protected[pos:m.start()].strip()))
            pos = m.end()
        if protected[pos:].strip():
            out.append((base + pos, protected[pos:].strip()))
    res = []
    for off, s in out:
        s = s.replace("\u2024", ".")
        if len(s.split()) < 3:
            continue
        i = max(0, next((k for k in range(len(starts) - 1, -1, -1) if starts[k] <= off), 0))
        res.append((pieces[i][1] if pieces else 1, s))
    return res

# ---------------------------------------------------------------- heuristics (no parser)

HUMAN = set("""i we you he she they me us him her them people person persons user users author authors reader readers
reviewer reviewers operator operators administrator administrators admin admins developer developers engineer engineers
student students teacher teachers customer customers team teams researcher researchers writer writers someone anyone
everyone nobody participant participants annotator annotators human humans driver drivers manager managers""".split())

ANIMATE = """know knows knew sees see saw seen learn learns learned understand understands understood decide decides decided
want wants wanted believe believes believed think thinks thought ask asks asked tell tells told claim claims claimed insist
insists cares care worry worries worried hate hates hated love loves loved like likes prefer prefers preferred swallow
swallows swallowed bite bites bit complain complains complained argue argues argued promise promises promised expect expects
notice notices noticed remember remembers remembered forget forgets forgot realize realizes realized assume assumes assumed
trust trusts trusted hide hides hid lie lies fight fights hunt hunts chase chases eat eats eaten breathe breathes sleep sleeps
wake wakes feel feels felt hear hears heard watch watches pretend pretends refuses-to-believe tolerate tolerates forgive
forgives punish punishes reward rewards demand demands begs beg wishes wish fear fears dislikes dislike""".split()
ANIMATE_RE = "|".join(sorted(set(ANIMATE), key=len, reverse=True))

COMP_VERBS = r"(?:show|shows|showed|shown|mean|means|meant|assume|assumes|assumed|believe|believes|believed|think|thinks|know|knows|knew|note|notes|noted|ensure|ensures|ensured|claim|claims|claimed|find|finds|found|suggest|suggests|suggested|argue|argues|argued|say|says|said|confirm|confirms|confirmed|guarantee|guarantees|verify|verifies|verified|realize|realizes|realized|expect|expects|expected|indicate|indicates|indicated|demonstrate|demonstrates|demonstrated|reveal|reveals|revealed|predict|predicts|predicted|observe|observes|observed|report|reports|reported|require|requires|required)"
FINITE = r"(?:is|are|was|were|has|have|had|can|cannot|could|will|would|must|should|may|might|does|do|did|helps|works|fails|holds|matters|runs|scales|improves|reduces|increases|returns|keeps|stays|needs|depends|differs|exceeds|outperforms|[a-z]+ed)"
DET = r"(?:the|a|an|this|these|those|it|we|they|he|she|our|its|their|each|every|most|many|all|no|some|any)"

DENOMINAL = r"(?:calendar|footnote|ticket|spreadsheet|bucket|timebox|sunset|greenlight|dogfood|workshop|whiteboard|slack|screenshot|bookend|sandwich|backlog|roadmap|journal|diary|memo|bullet|sticky-note|pressure-test|loop|action|task|surface|gate|scope|unblock|productionize|operationalize|socialize|evidence|spec|template|architect|parent|friend|gift|interview|chapter|paragraph|asterisk|asset|budget|calendarize)"
OBJ = r"(?:it|them|this|that|these|those|the|a|an|our|your|their|his|her|him|me|us|everything|something)"

NOUN_SUFFIX = re.compile(r"(?:tion|sion|ment|ness|ity|ance|ence|ancy|ency|ure|age|ship|ism|ist|ics|ogy|ery|er|or)s?$")
COMMON_NOUNS = set("""data file files system systems user users model models memory cache network server servers policy budget
time cost costs rate risk task tasks call calls code test tests key keys log logs path paths rule rules state table page word
job queue disk link port host node team plan fund funds market money price value load request requests response session
token tokens batch query queries index thread process kernel device storage bandwidth latency throughput window error
errors failure failures change changes object objects firewall route routes gpu cpu api sdk ui app apps service services
feature features reader readers patience budget suite pipeline workflow cluster driver library module packet message
agent agents client clients component components event events content element elements argument arguments latency policy
fund funds market markets phone image images container containers account accounts""".split())
NOT_NOUNS = set("""wider larger smaller faster slower lower higher newer older earlier later other under over after never ever
rather whether either neither together further former latter inner outer upper proper per however covers cover exists exist
delivers deliver offers offer considers consider renders render triggers trigger orders answers registers enters alters gathers
lowers powers suffers transfers refers prefers differs recovers remembers wonders matters requires uses runs works holds keeps
needs makes takes gives shows means depends includes contains supports returns saves writes reads sends gets sets lets puts
legacy major minor clever proper sober eager bitter""".split())
ADJ_HYPHEN = re.compile(r"-(?:specific|based|safe|local|aware|free|level|wide|like|style|grade|ready|friendly|bound|driven|oriented|related|sensitive|critical|heavy|intensive|only|time|term|scale|class|tier|facing|native|agnostic)$")
FUNCTION_WORDS = set("""a an the and or but nor so yet for of to in on at by with from into onto over under about after before
between through during without within against among per via than then that which who whom whose this these those it its
is are was were be been being has have had do does did can could will would must should may might shall not no only also
very more most less least each every all any some such both either neither one two three first second new old same other
own just even still already as if when while where because although though since unless once whether how what why up out
off down back here there we you they he she i our your their his her my me us them him""".split())


def nounish(w):
    lw = w.lower().strip(".,;:()\"'")
    if not lw or lw in FUNCTION_WORDS or not re.match(r"^[a-z][a-z0-9-]*$", lw):
        return False
    if lw.endswith(("ly", "ing", "ed", "ous", "ive", "ful", "less", "able", "ible")) or lw in NOT_NOUNS or ADJ_HYPHEN.search(lw):
        return False
    return lw in COMMON_NOUNS or ("-" in lw and len(lw) > 5) or bool(NOUN_SUFFIX.search(lw))


def heuristic(line, s, max_words):
    found = []
    words = s.split()
    if len(words) > max_words:
        found.append(("long-dependency", f"long sentence ({len(words)} words)"))
    m = re.match(r"^(?:If|When|Because|Although|Though|Before|After|While|Since|Unless|Once|Even if|Even though)\b([^,]*),", s)
    if m and len(m.group(1).split()) >= 14:
        found.append(("long-dependency", f"long fronted clause ({len(m.group(1).split())} words) before the main clause"))
    if re.match(r"^[A-Z][^,.;:]{2,60},\s[^,.;:]{3,80},\s(?:" + FINITE + r"|[a-z]+s)\b", s):
        found.append(("long-dependency", "subject separated from its verb by an inserted phrase"))
    body = re.sub(r"^(?:For example|For instance|In this case|In that case|Thus|However|Similarly|Then|Instead|Otherwise|In practice|In short),\s+", "", s)
    m = re.match(r"^(?:The|A|An|Every|Each|Any|No|a|an|the)\s+(?:\S+\s+){0,2}?(?:that|which|who)\s+((?:\S+\s+){4,}?)(?:" + FINITE + r"|[a-z]{3,}s)\b", body)
    if m:
        found.append(("long-dependency", "subject with a relative clause before the main verb"))
    if re.search(r",\s(?:such as|including|like|for example|e\.g\.)\s[^,.;]{2,50},\s(?:to|into|from|with|for|in|on|as)\b", s):
        found.append(("long-dependency", "inserted example splits a verb from its complement"))
    if re.search(r",\s(?:unlike|as|like|however|whatever|whichever|even)\s[^,.;]{2,70},\s(?:and|so|but|or|such as)\b", s):
        found.append(("long-dependency", "inserted phrase between two clauses or before an example"))
    if re.search(r",\s(?:not|rather than|instead of)\s[^,.;]{3,80},\s(?:because|since|so|as)\b", s) or (len(words) >= 22 and re.search(r",\s(?:because|since)\s[^,.;]{15,}[.?!]?$", s) and s.count(",") >= 2):
        found.append(("long-dependency", "the reason comes only at the end of a long sentence"))
    if re.search(r"\b(?:that|which)\s[^,.;]{6,60},\s(?:and|or)\s(?:the|a|an)\s", s) and len(words) >= 18:
        found.append(("long-dependency", "a list continues after a relative clause; check what the item attaches to"))
    for m in re.finditer(r"\b(?:the|a|an|each|every|any|no|this|these|those|some)\s+(?:[a-z][a-z-]+\s+){0,2}([a-z][a-z-]+)\s+(I|you|we|they|he|she|it|someone|people)\s+([a-z]+)\b", s):
        if m.group(1) not in FUNCTION_WORDS and m.group(3) not in ("and", "or", "to", "of"):
            found.append(("dropped-that", f"possible object relative without \"that\": \"{m.group(0)}\""))
    for m in re.finditer(r"\b(nothing|something|anything|everything|whatever)\s+(?:the\s+|a\s+)?([A-Za-z][\w-]*)\s+([a-z]+(?:s|ed))\b", s):
        found.append(("dropped-that", f"possible object relative without \"that\": \"{m.group(0)}\""))
    for m in re.finditer(r"\b" + COMP_VERBS + r"\s+(?!that\b|how\b|what\b|why\b|whether\b|if\b|when\b|where\b|which\b|who\b|to\b)" + DET + r"\s+(?:[\w-]+\s+){0,3}?" + FINITE + r"\b", s, re.I):
        found.append(("dropped-that", f"possible complement clause without \"that\": \"{m.group(0)}\""))
    for m in re.finditer(r"\b" + COMP_VERBS + r"\s+(?:the|a|an|this|our|its|their)\s+([a-z][a-z-]+)\s+([a-z]{3,}(?:s|ed))\b", s, re.I):
        third = m.group(2).lower()
        if third not in COMMON_NOUNS and not third.endswith(("ss", "us", "is")) and nounish(m.group(1)):
            found.append(("dropped-that", f"possible complement clause without \"that\": \"{m.group(0)}\""))
    run = []
    for w in words + ["."]:
        if nounish(w) and not re.search(r"[.,;:)]$", w):
            run.append(w)
            continue
        if nounish(w):
            run.append(w)
        if len(run) >= 3:
            found.append(("noun-stack", f"possible noun stack: \"{' '.join(run).strip('.,;:')}\""))
        run = []
    for m in re.finditer(r"\b" + DENOMINAL + r"(?:s|ed|d|ing)?\s+" + OBJ + r"\b", s, re.I):
        pre = s[max(0, m.start() - 12):m.start()].lower()
        if re.search(r"\b(the|a|an|this|that|our|your|their|its|of|per)\s*$", pre):
            continue  # used as a noun
        found.append(("noun-as-verb", f"possible noun used as a verb: \"{m.group(0)}\""))
    for m in re.finditer(r"(?:^|\b|(?<=\s))((?i:the|a|an|this|that|its|our|each|every|any|no)\s+(?:[\w-]+\s+){0,2}[\w-]+|`[^`]+`|[\w.]+\(\)|It|This|That)\s+(?:also\s+|then\s+|already\s+|only\s+|never\s+|still\s+|now\s+|cannot\s+|can\s+|will\s+|does\s+not\s+|doesn't\s+)?(" + ANIMATE_RE + r")\b", s):
        head = m.group(1).split()[-1].lower()
        if head in HUMAN or head in ("agent", "agents", "model", "models"):
            continue
        found.append(("animate-verb", f"possible inanimate subject with an animate verb: \"{m.group(0)}\""))
    return found

# ---------------------------------------------------------------- spaCy rules (optional)


def compounds(t):
    """All compound modifiers under a noun, at any depth ("brokerage" -> "money" -> "market" -> "funds")."""
    out = []
    for c in t.lefts:
        if c.dep_ == "compound":
            out += compounds(c) + [c]
    return out


def spacy_checks(nlp, line, s, max_words, long_arc=18, subject_gap=12):
    found = []
    doc = nlp(s)
    arcs = [abs(t.i - t.head.i) for t in doc if t.head is not t and not t.is_punct]
    words = [t for t in doc if not t.is_punct]
    if len(words) > max_words:
        found.append(("long-dependency", f"long sentence ({len(words)} words)"))
    if arcs and max(arcs) >= long_arc:
        t = max((t for t in doc if t.head is not t), key=lambda t: abs(t.i - t.head.i))
        found.append(("long-dependency", f"long dependency ({abs(t.i - t.head.i)} words) between \"{t.text}\" and \"{t.head.text}\""))
    for t in doc:
        if t.dep_ == "nsubj" and t.head.pos_ in ("VERB", "AUX") and t.i < t.head.i and t.head.i - t.i >= subject_gap:
            found.append(("long-dependency", f"subject \"{t.text}\" is {t.head.i - t.i} words from its verb \"{t.head.text}\""))
        if t.dep_ == "relcl":
            rel = [c for c in t.children if c.tag_ in ("WDT", "WP", "WP$") or c.lower_ == "that"]
            subj = [c for c in t.children if c.dep_ in ("nsubj", "nsubjpass")]
            if not rel and subj and subj[0].lower_ not in ("that", "which", "who"):
                found.append(("dropped-that", f"object relative without \"that\": \"{t.head.text} ... {doc[t.left_edge.i:t.i + 1].text}\""))
        if t.dep_ == "ccomp" and t.head.lemma_ in ("show", "mean", "assume", "believe", "think", "know", "note", "ensure", "claim", "find", "suggest", "argue", "say", "confirm", "guarantee", "verify", "realize", "expect", "indicate", "demonstrate", "reveal", "predict", "observe", "report"):
            if not any(c.dep_ == "mark" and c.lower_ == "that" for c in t.children) and t.i > t.head.i:
                found.append(("dropped-that", f"complement clause without \"that\" after \"{t.head.text}\""))
        if t.pos_ in ("NOUN", "PROPN") and t.dep_ != "compound":
            chain = compounds(t)
            if len(chain) >= 2:
                first = min(c.i for c in chain)
                found.append(("noun-stack", f"noun stack: \"{doc[first:t.i + 1].text}\""))
        if t.pos_ == "VERB" and re.fullmatch(DENOMINAL, t.lemma_.lower()):
            found.append(("noun-as-verb", f"possible noun used as a verb: \"{t.text}\""))
        if t.dep_ == "nsubj" and t.head.lemma_.lower() in ANIMATE:
            if t.lower_ not in HUMAN and t.ent_type_ not in ("PERSON", "NORP", "ORG") and t.lemma_.lower() not in HUMAN | {"agent", "model"}:
                found.append(("animate-verb", f"inanimate subject \"{t.text}\" with animate verb \"{t.head.text}\""))
    return found

# ---------------------------------------------------------------- main


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file")
    ap.add_argument("--json", action="store_true", help="print JSON instead of text")
    ap.add_argument("--max-words", type=int, default=30, help="flag sentences longer than this (default 30)")
    ap.add_argument("--no-spacy", action="store_true", help="use the heuristics even if spaCy is installed")
    ap.add_argument("--long-arc", type=int, default=18, help="spaCy: flag a dependency at least this many words long (default 18)")
    ap.add_argument("--subject-gap", type=int, default=12, help="spaCy: flag a subject this many words before its verb (default 12)")
    a = ap.parse_args()

    nlp = None
    if not a.no_spacy:
        try:
            import spacy
            try:
                nlp = spacy.load("en_core_web_sm")
            except Exception:
                # Some Python builds fail to read the model's tokenizer rules; the default English tokenizer works.
                nlp = spacy.load("en_core_web_sm", exclude=["tokenizer"])
        except Exception:
            nlp = None
    text, pieces = extract(a.file)
    results = []
    for line, s in sentences(text, pieces):
        found = heuristic(line, s, a.max_words)
        if nlp:  # the parse and the patterns each catch cases the other misses, so use both
            found = spacy_checks(nlp, line, s, a.max_words, a.long_arc, a.subject_gap) + [f for f in found if not f[1].startswith("long sentence")]
        seen = set()
        for kind, note in found:
            if (kind, note) in seen:
                continue
            seen.add((kind, note))
            results.append({"line": line, "construction": kind, "note": note, "sentence": s})

    if a.json:
        print(json.dumps({"mode": "spacy" if nlp else "heuristic", "candidates": results}, indent=1))
        return
    order = ["long-dependency", "dropped-that", "noun-stack", "noun-as-verb", "animate-verb"]
    names = {"long-dependency": "Long dependencies", "dropped-that": "Dropped \"that\"", "noun-stack": "Stacked noun compounds",
             "noun-as-verb": "Nouns used as verbs", "animate-verb": "Inanimate subjects with animate verbs"}
    print(f"# Candidates in {a.file} ({'spaCy parse plus pattern heuristics' if nlp else 'pattern heuristics only; spaCy with en_core_web_sm adds parse-based checks'})")
    print("# These are places to look, not verdicts. Read every sentence too: rare word combinations are never flagged,")
    print("# and many long dependencies and figurative verbs are missed.\n")
    for k in order:
        groups = {}
        for r in results:
            if r["construction"] == k:
                groups.setdefault((r["line"], r["sentence"]), []).append(r["note"])
        print(f"## {names[k]}: {len(groups)} sentences")
        for (line, sent), notes in groups.items():
            sent = sent if len(sent) <= 220 else sent[:217] + "..."
            print(f"  line {line}: {'; '.join(notes)}\n      {sent}")
        print()
    print("## Rare word combinations: not checked automatically; read for them.")


if __name__ == "__main__":
    main()
