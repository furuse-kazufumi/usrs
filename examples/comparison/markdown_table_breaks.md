# Markdown table breaks — 7 real cases, side-by-side with USV

> Markdown tables are a beloved hack, not a designed format. They were
> retrofitted onto a markup language whose primary unit is "one
> paragraph = one line". This page shows seven cases where that hack
> falls over, and what the same data looks like in USV.
>
> For each case, the Markdown is shown raw (so you can see why it
> breaks) and the **rendered output on GitHub** is described in words —
> screenshots are TODO markers; PRs welcome.

<!-- TODO: add screenshots/case-1-markdown-broken.png (and 2..7) -->

---

## Case 1 — CJK character widths

### Markdown

```markdown
| Product | Qty | Note     |
|---------|-----|----------|
| Apple   | 5   | sweet    |
| みかん  | 12  | 酸っぱい |
| バナナ  | 8   | bland    |
```

**What GitHub renders:** columns appear **misaligned** in the source
view (because the editor uses a proportional font and CJK chars are
~1.7× wider than ASCII). In *rendered* view GitHub's CSS does its best
but cell padding is still uneven.

**Worse:** if you ever open this in `cat` / `less` / a terminal that
uses a *different* East Asian Width policy than the editor, the
alignment is gone entirely.

### USV

```python
from usrs import dumps
print(dumps(
    [["Product","Qty","Note"],
     ["Apple","5","sweet"],
     ["みかん","12","酸っぱい"],
     ["バナナ","8","bland"]],
    with_width=True,
))
```

Width metadata travels with the data — every UAX #11-compliant
renderer produces the same alignment.

---

## Case 2 — emoji

### Markdown

```markdown
| Reaction | Count |
|----------|-------|
| 🎉       | 142   |
| 🚀       | 89    |
| 🐛       | 23    |
```

**What breaks:** emoji are *Wide* (W=2) per UAX #11 but Markdown has
no width hint. Renderers fall into two camps — those that treat emoji
as monospace (and squish the column) and those that don't (and let
emoji overflow). ZWJ sequences (👨‍👩‍👧‍👦) are worse: most renderers
count them as 4 wide characters instead of 1 glyph.

### USV

USV puts the width tag *next to the cell*, so a ZWJ family emoji can
be tagged `W2:👨‍👩‍👧‍👦` and the renderer trusts the metadata over
its own counting.

---

## Case 3 — multi-line cells (illegal in Markdown)

### Markdown

````markdown
| Host    | Notes                |
|---------|----------------------|
| web-01  | - nginx 1.27
- TLS via Let's Encrypt
- rate-limited at 100 rps   |
````

**What breaks:** Markdown table syntax requires **one row per line**.
A literal newline inside a cell terminates the row. There is no escape
sequence in CommonMark for "newline within table cell". You're stuck
with `<br>` (HTML-only, doesn't survive `pandoc -t plain`) or
collapsing to a single line.

### USV

```python
rows = [
    ["Host", "Notes"],
    ["web-01", "- nginx 1.27\n- TLS via Let's Encrypt\n- rate-limited at 100 rps"],
]
print(dumps(rows, with_width=True))
```

USV's only structural characters inside a row are `\x1F` (between cells)
and `\x1E` (between rows). Newlines inside a cell are just data.

---

## Case 4 — pipe characters in cell data

### Markdown

```markdown
| Command         | Description              |
|-----------------|--------------------------|
| `grep \| sort`  | filter then sort         |
| `ls -la \| awk` | list and process columns |
```

**What breaks:** you have to escape `|` as `\|`. Most editors don't
auto-escape on paste, and some renderers handle `\|` differently. If a
user pastes a one-liner with `|` from their terminal, the table
silently corrupts.

### USV

USV's cell separator is `\x1F`, which doesn't appear in command lines.
You can paste the pipe character raw and it just works.

---

## Case 5 — alignment with mixed-width content

### Markdown

```markdown
| Name | Email                | Notes |
|------|----------------------|-------|
| Tom  | tom@example.com      | a     |
| 田中 | tanaka@example.co.jp | a     |
| José | jose@example.es      | a     |
```

**What breaks:** the *source* alignment looks ragged because `田中`,
`Tom`, and `José` have visually different widths in the editor's font.
The *rendered* table on GitHub uses CSS table layout so it looks fine,
but `pandoc -t plain` outputs a 4-column ASCII grid with misaligned
boxes.

### USV

USV is rendered by a function that asks `display_width()` for every
cell, then pads to the column max. Output is identical across
terminal / browser / PDF / printer.

---

## Case 6 — leading / trailing whitespace

### Markdown

```markdown
| Code      | Output       |
|-----------|--------------|
| `  hello` | "  hello"    |
| ` world ` | " world "    |
```

**What breaks:** most Markdown parsers `.strip()` cell content silently.
You can't represent "two leading spaces in this cell" without using
inline code (`` ` `` backticks) — which then changes the *typography*
of the cell from prose to monospace.

### USV

USV preserves cell content verbatim. `  hello` is exactly `  hello` —
two spaces, lowercase h, ello. No stripping, no quoting, no escaping.

---

## Case 7 — Right-to-Left text (Arabic, Hebrew)

### Markdown

```markdown
| English | Arabic        | Hebrew    |
|---------|---------------|-----------|
| hello   | مرحبا         | שלום      |
| world   | عالم          | עולם      |
```

**What breaks:** Markdown table source becomes nearly unreadable in
most editors because the RTL run flips the visual order of cells. The
rendered HTML may also misalign because some renderers don't apply
`unicode-bidi: isolate` per cell.

### USV

USV separates *data* from *rendering*. The renderer can apply
`unicode-bidi: isolate-override` (or its terminal equivalent) per cell
because each cell is a discrete unit, not a position in a `|`-delimited
string. The data file itself is just UTF-8 with structural separators.

---

## Bonus: round-trip lossless conversion

Markdown → USV is lossy (Markdown can't represent multi-line cells, so
USV preserves them via `\n` in the cell content; round-tripping back
to Markdown either loses the newline or requires `<br>` HTML escaping).

But TSV ↔ USV is fully lossless:

```bash
python -m usrs from-tsv data.tsv > data.usv
python -m usrs to-tsv   data.usv > roundtrip.tsv
diff data.tsv roundtrip.tsv   # empty — identical
```

This is the **migration path**: keep your existing TSV pipelines, just
convert at the boundary where you need stable visual rendering.

---

## Why this matters

Every case above is *real* — encountered in actual `*.md` files,
GitHub READMEs, Notion docs, Confluence pages. The Markdown table is
not a data format; it's a *display hint* with implicit assumptions
about character width and parser leniency that don't survive contact
with international text or programmatic data.

USV is the smallest possible separator-of-concerns: **data lives in
one file with one rule (split on `\x1F` and `\x1E`), and rendering
lives elsewhere**.

That's the whole pitch.

→ See [README.md](../../README.md) for quick start and
  [SPEC.md](../../SPEC.md) for the formal rules.
