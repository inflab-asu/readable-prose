# Tracked changes in LaTeX

Use this when the user wants the fixes visible for review, as blue new text and gray struck-through old text, rather than applied silently.

## 1. Add the macros
Put these in the preamble or in a macros file that the preamble reads. Check first that the document does not already define `\added` or `\deleted`, for example through the `changes` package; if it does, reuse those.

```latex
% Tracked changes: \added prints new text in blue, \deleted prints removed text in gray strikethrough.
% Set \showchangesfalse for the clean text: \added then prints plain text and \deleted prints nothing.
% The empty group in \added keeps a leading space, which \color would otherwise skip.
\RequirePackage[normalem]{ulem}   % normalem keeps \emph as italics
\newif\ifshowchanges
\showchangestrue
\providecommand{\added}[1]{\ifshowchanges\textcolor{blue}{{}#1}\else#1\fi}
\providecommand{\deleted}[1]{\ifshowchanges\textcolor{gray}{\sout{#1}}\fi}
```

The document needs `xcolor`. The empty group `{}` matters: `\color` ends with `\ignorespaces`, so without it an inserted word that starts with a space runs into the word before it ("controllera request").

## 2. Write the fixes as old and new spans
Collect the fixes as a JSON list of objects with `old` and `new` keys. Each `old` must be copied exactly from the file, including line breaks and indentation, must occur exactly once, and must not run through a `%` comment line. Keep spans as short as the fix allows, but a fix that restructures a sentence can span the whole sentence.

```json
[
  {"old": "the policy decides on the object itself", "new": "the policy checks the object itself"},
  {"old": "A request that changes nothing \\SystemName{} covers continues,\n    such as the write with which \\texttt{cat} prints\n    to its output pipe.",
   "new": "A request continues if it changes nothing that \\SystemName{} covers.\nFor example, \\texttt{cat}'s write to its output pipe continues."}
]
```

## 3. Apply them with the script
```bash
python3 <skill>/scripts/mark_changes.py mark paper.tex fixes.json            # preview the markup
python3 <skill>/scripts/mark_changes.py mark paper.tex fixes.json --write    # apply it to the file
```
The script diffs each pair word by word, keeping punctuation as its own token, and wraps only the changed words. If a change would split a brace group, it marks the whole span instead. Before it writes anything, it checks every span three ways. With the changes accepted, the span must equal the new text. With them rejected, it must equal the old text. In neither must a space come before a period or comma. If any check fails, it writes nothing and names the failing pair.

Then build the document and look at one marked page, because `\sout` can fail on some commands. References, citations, `\texttt` and custom macros inside `\deleted` work. For a footnote or math inside a deleted span, mark the whole sentence instead, or wrap the command in `\mbox{}`.

## 4. Accept or reject later
When the author has reviewed the changes:
```bash
python3 <skill>/scripts/mark_changes.py resolve paper.tex --accept --write   # keep the new text
python3 <skill>/scripts/mark_changes.py resolve paper.tex --reject --write   # restore the old text
```
For one change at a time, edit the file by hand: keep the body of `\added{...}` and delete `\deleted{...}`, or the reverse.

## Other formats
- **Markdown.** Write `~~old words~~ **new words**`, or give a table of findings and let the user apply them.
- **Word.** Use the docx skill's tracked changes, which Word shows natively.
- **Plain text or email.** Give the findings table and the revised text.
