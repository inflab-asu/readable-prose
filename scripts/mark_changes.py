#!/usr/bin/env python3
"""Apply readability fixes to a LaTeX file as tracked changes, or accept or reject them later.

mark:    python3 mark_changes.py mark FILE FIXES.json [--write] [--added added] [--deleted deleted]
         FIXES.json is a list of {"old": ..., "new": ...}. Each "old" must occur exactly once in FILE.
         The script diffs each pair word by word and wraps only the changed words in \\added{...} and
         \\deleted{...}. Before writing, it checks every span: accepting the changes must give "new",
         rejecting them must give "old", and no space may come before a period or comma. Without --write
         it prints the markup for review.
resolve: python3 mark_changes.py resolve FILE (--accept | --reject) [--write]
         Removes the markup, keeping the new text (--accept) or the old text (--reject).

The macros themselves are in references/tracked-changes.md of the readable-prose skill.
"""
import argparse
import difflib
import json
import re
import sys


def toks(s):
    out = []
    for m in re.finditer(r"(\s*)(\S+)", s):
        ws, w = m.group(1), m.group(2)
        mm = re.match(r"^(.*?)([.,;:]+)$", w)
        if mm and mm.group(1) and mm.group(1).count("{") == mm.group(1).count("}"):
            out.append((ws, mm.group(1)))
            out.append(("", mm.group(2)))
        else:
            out.append((ws, w))
    return out, re.search(r"(\s*)$", s).group(1)


def balanced(ts):
    t = "".join(ws + w for ws, w in ts).replace("\\{", "").replace("\\}", "")
    return t.count("{") == t.count("}")


def joined(ts):
    return "".join(ws + w for ws, w in ts).lstrip()


def raw(ts):
    return "".join(ws + w for ws, w in ts)


def mark(old, new, A, D):
    o, otrail = toks(old)
    n, ntrail = toks(new)
    lead = re.match(r"^(\s*)", old).group(1)
    sm = difflib.SequenceMatcher(None, [w for _, w in o], [w for _, w in n], autojunk=False)
    parts = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            parts.append(raw(o[i1:i2]))
            continue
        if not balanced(o[i1:i2]) or not balanced(n[j1:j2]):
            return None
        if tag == "insert":
            parts.append(f"\\{A}{{" + raw(n[j1:j2]) + "}")
        elif tag == "delete":
            parts.append(f"\\{D}{{" + raw(o[i1:i2]) + "}")
        elif o[i1][0] == n[j1][0]:
            parts.append(o[i1][0] + f"\\{D}{{" + joined(o[i1:i2]) + "}" + f"\\{A}{{" + joined(n[j1:j2]) + "}")
        else:
            parts.append(f"\\{D}{{" + raw(o[i1:i2]) + "}" + f"\\{A}{{" + raw(n[j1:j2]) + "}")
    res = "".join(parts)
    if not res.startswith(lead):
        res = lead + res.lstrip()
    return res + (ntrail if ntrail else otrail)


def whole(old, new, A, D):
    lead = re.match(r"^(\s*)", old).group(1)
    return lead + f"\\{D}{{" + old.strip() + "}" + f"\\{A}{{" + new.strip() + "}" + ("\n" if old.endswith("\n") else "")


def render(t, accept, A="added", D="deleted"):
    out, i = [], 0
    cmds = (f"\\{A}{{", f"\\{D}{{")
    while i < len(t):
        hit = next((c for c in cmds if t.startswith(c, i)), None)
        if not hit:
            out.append(t[i])
            i += 1
            continue
        j, depth = i + len(hit), 1
        while depth:
            if j >= len(t):
                raise ValueError(f"unbalanced braces after {hit} at offset {i}")
            if t[j] == "\\" and j + 1 < len(t) and t[j + 1] in "{}":
                j += 2
                continue
            depth += {"{": 1, "}": -1}.get(t[j], 0)
            j += 1
        body = t[i + len(hit):j - 1]
        keep = (hit == cmds[0]) == accept
        out.append(render(body, accept, A, D) if keep else "")
        i = j
    return "".join(out)


def norm(t):
    return re.sub(r" ([.,;:])", r"\1", re.sub(r"\s+", " ", t).strip())


def cmd_mark(a):
    text = open(a.file, encoding="utf-8").read()
    fixes = json.load(open(a.fixes, encoding="utf-8"))
    problems, previews = [], []
    for k, f in enumerate(fixes, 1):
        old, new = f["old"], f["new"]
        c = text.count(old)
        if c != 1:
            problems.append(f"fix {k}: old text occurs {c} times (must be exactly once): {old[:70]!r}")
            continue
        m = mark(old, new, a.added, a.deleted)
        how = "words"
        if m is None:
            m, how = whole(old, new, a.added, a.deleted), "whole span"
        if norm(render(m, True, a.added, a.deleted)) != norm(new):
            problems.append(f"fix {k}: accepting the markup does not give the new text")
        if norm(render(m, False, a.added, a.deleted)) != norm(old):
            problems.append(f"fix {k}: rejecting the markup does not give the old text")
        if re.search(r"\w [.,]", re.sub(r"\s+", " ", render(m, True, a.added, a.deleted)).replace("et al .", "")):
            problems.append(f"fix {k}: the accepted text has a space before a period or comma")
        previews.append((k, how, m))
        text = text.replace(old, m)
    for k, how, m in previews:
        print(f"===== fix {k} ({how})\n{m}")
    if problems:
        print("\nNOT WRITTEN. Problems:\n  " + "\n  ".join(problems), file=sys.stderr)
        sys.exit(1)
    if a.write:
        open(a.file, "w", encoding="utf-8").write(text)
        print(f"\nWrote {len(fixes)} tracked changes to {a.file}.")
    else:
        print(f"\nAll {len(fixes)} fixes pass the checks. Run again with --write to apply them.")


def cmd_resolve(a):
    text = open(a.file, encoding="utf-8").read()
    out = render(text, a.accept, a.added, a.deleted)
    n = text.count(f"\\{a.added}{{") + text.count(f"\\{a.deleted}{{")
    if a.write:
        open(a.file, "w", encoding="utf-8").write(out)
        print(f"Resolved {n} markers in {a.file} ({'accepted' if a.accept else 'rejected'}).")
    else:
        sys.stdout.write(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    m = sub.add_parser("mark", help="apply fixes as tracked changes")
    m.add_argument("file")
    m.add_argument("fixes")
    m.add_argument("--write", action="store_true")
    r = sub.add_parser("resolve", help="accept or reject all tracked changes")
    r.add_argument("file")
    g = r.add_mutually_exclusive_group(required=True)
    g.add_argument("--accept", action="store_true")
    g.add_argument("--reject", action="store_true")
    r.add_argument("--write", action="store_true")
    for p in (m, r):
        p.add_argument("--added", default="added", help="name of the added-text macro (default added)")
        p.add_argument("--deleted", default="deleted", help="name of the deleted-text macro (default deleted)")
    a = ap.parse_args()
    cmd_mark(a) if a.cmd == "mark" else cmd_resolve(a)


if __name__ == "__main__":
    main()
