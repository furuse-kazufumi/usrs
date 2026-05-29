# USV — tables that don't break on CJK or emoji

> **The pain:** your Markdown table looks fine until someone drops `みかん`,
> `😀`, or a multi-line cell into it — and now the whole thing is a slanted
> mess in every renderer except yours.
>
> **The fix:** **USV (Unit-Separated Values)** — a tiny text format that
> uses the ASCII 1967 `U+001F` / `U+001E` separators *plus* per-cell
> display-width metadata, so editors / browsers / terminals all draw the
> same aligned table.

<!-- TODO: add 30s GIF — "Markdown breaks → switch to .usv → aligned everywhere" -->
<!-- placeholder: docs/assets/usv-demo.gif -->

[![License: Apache-2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Status: RFC draft](https://img.shields.io/badge/Status-RFC_draft-orange.svg)](SPEC.md)
[日本語 README](README_JA.md) ・ [SPEC](SPEC.md) ・ [Discussion #1](https://github.com/furuse-kazufumi/usrs/discussions/1) ・ [SixArm/usv #14 (revival proposal)](https://github.com/SixArm/usv/issues/14)

---

## 60-second pitch

| Format | Separator | Breaks on CJK / emoji? | Breaks on multi-line cell? | Lossless round-trip? |
|---|---|---|---|---|
| CSV | `,` | yes (renderer-dependent) | needs quoting + escaping | tricky (RFC 4180 corners) |
| TSV | `\t` | yes (tab width = 4? 8?) | no multi-line support | yes (no tabs in cells) |
| Markdown table | `\|` | **yes** (any non-ASCII) | **no** (illegal) | n/a (rendering format) |
| **USV** | **`\x1F`** (Unit) + **`\x1E`** (Record) | **no** (UAX #11 width tags) | **yes** (any char allowed in cell) | **yes** (TSV ⇄ USV) |

---

## Quick start (3 lines)

```python
from usrs import dumps, loads, render

text = dumps([["商品","個数","備考"], ["Apple","5","甘い"], ["みかん","12","酸っぱい"]], with_width=True)
print(render(loads(text)))
```

Output (renders identically in any monospace terminal):

```
┌──────────┬──────┬────────────┐
│ 商品     │ 個数 │ 備考       │
├──────────┼──────┼────────────┤
│ Apple    │ 5    │ 甘い       │
│ みかん   │ 12   │ 酸っぱい   │
└──────────┴──────┴────────────┘
```

CLI:

```bash
python -m usrs from-tsv  data.tsv  > data.usv   # TSV → USV (lossless)
python -m usrs render    data.usv               # aligned table to terminal
python -m usrs to-tsv    data.usv  > data.tsv   # USV → TSV (lossless)
```

---

## Before / after — Markdown vs USV

A real table with CJK, emoji, and a multi-line cell.

### Before — Markdown (broken)

````markdown
| Product | Qty | Note          |
|---------|-----|---------------|
| Apple   | 5   | sweet         |
| みかん  | 12  | 酸っぱい 🍊   |
| バナナ  | 8   | 常温保存可
   (室温 25℃ 以下)            |
````

Renders in GitHub as a column-misaligned, broken-on-newline mess; renders
*differently* in VS Code preview, Obsidian, and pandoc. The pipe character
in `室温 25℃` doesn't break parsing — but the newline inside the cell does.

### After — USV (`.usv`)

```python
from usrs import dumps
rows = [
    ["Product", "Qty", "Note"],
    ["Apple",   "5",   "sweet"],
    ["みかん",  "12",  "酸っぱい 🍊"],
    ["バナナ",  "8",   "常温保存可\n(室温 25℃ 以下)"],   # newline is fine
]
print(dumps(rows, with_width=True))
```

Every renderer that understands USV (terminal `render()`, future VS Code
extension, future `<usv-table>` Web Component) draws **the same**
column-aligned, multi-line-cell-respecting table — because the width
metadata travels with the data.

See [examples/comparison/markdown_table_breaks.md](examples/comparison/markdown_table_breaks.md)
for 5 more side-by-side cases.

---

## Why `U+001F` is safe (gotchas, honestly)

ASCII reserved `U+001C`-`U+001F` as **Information Separators** in 1967 —
designed for exactly this job — and almost nobody uses them. That makes
them collision-free in real data, which is the whole point.

**It works in:**
- file I/O, pipes, sockets, sqlite TEXT columns, JSON strings (escaped
  as ``), zip archives, git blobs, tar, S3 objects
- modern terminals (they ignore unrecognised C0 codes by default)
- any UTF-8-clean toolchain

**It can get stripped in:**
- HTML form submissions, some email gateways, paste filters of
  "rich text" editors, naive `printf "%s"` in old shells

**For those cases USV has a Unicode visible variant** — `␟` (U+241F) /
`␞` (U+241E) — and the decoder accepts either. So you pick the wire
format that survives your pipeline; the data is the same.

→ Full rules in [SPEC.md §3](SPEC.md). Limits and non-goals are listed
  honestly in [PROMOTION.md §0](PROMOTION.md).

---

## What's in this repo

```
usrs/
├── SPEC.md                # normative spec (RFC draft)
├── README.md  README_JA.md
├── src/usrs.py            # Python reference implementation (~330 LOC)
├── examples/
│   ├── sales.usv          # tiny sample file
│   ├── sales_unicode.usv  # same data, U+241F variant
│   ├── llm_prompts/       # prompt templates for Claude / GPT / Gemini
│   └── comparison/        # Markdown-table-breaks side-by-side
├── docs/                  # design log, related work, contact plan
└── tests/                 # 31 round-trip + edge-case tests
```

---

## Roadmap

| Phase | Scope |
|---|---|
| **0.1.0** (this draft) | SPEC + Python encode/decode + TSV round-trip |
| 0.2.0 | Colour terminal renderer; Markdown ⇄ USV converter |
| 0.3.0 | VS Code extension (`.usv` as table view) |
| 0.4.0 | Web Component (`<usv-table>`); Rust implementation |
| 0.5.0 | gh-pages playground; editor plugins (Neovim / JetBrains / Obsidian) |
| 1.0.0 | IETF Draft submission |

---

## Related work

USV is **not the first try**. [SixArm/usv](https://github.com/SixArm/usv)
(Joel Parker Henderson, 2022 — currently quiet) reached an IETF Draft
v01 then went dormant. We've opened a **revival proposal upstream** at
[SixArm/usv#14](https://github.com/SixArm/usv/issues/14) — the goal is
either to feed our additions back in, or co-author a fresh IETF draft
together. See [docs/RELATED_WORK.md](docs/RELATED_WORK.md) for the full
prior-art map (ASCII 1967, RFC 4180, IANA TSV, UAX #11, Control Pictures).

Community discussion lives in
[Discussion #1](https://github.com/furuse-kazufumi/usrs/discussions/1).

---

## License

[Apache-2.0](LICENSE) (OSS) + Commercial dual-license. OSS use is free;
only commercial SaaS / SI engagements need a separate agreement.

## Community

- Bug reports / feature requests → GitHub Issues
- Design discussion → [GitHub Discussions](https://github.com/furuse-kazufumi/usrs/discussions)
- Adoption strategy → [PROMOTION.md](PROMOTION.md)
- Contribution guide → [CONTRIBUTING.md](CONTRIBUTING.md)
