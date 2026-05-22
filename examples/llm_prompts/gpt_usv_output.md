# GPT (OpenAI) — making it emit USV instead of Markdown tables

> GPT-4 / GPT-4o default to Markdown tables and they break the moment
> you ask for CJK, emoji, or multi-line cells. This page shows prompts
> that produce valid USV output you can decode with `usrs.loads()`.

GPT tends to be more verbose than Claude, so the `# system` block needs
to be a little stricter about "no prose".

---

## System message (reusable)

```text
You output ONLY data in USV (Unit-Separated Values) format.

Format rules:
- U+001F separates cells within a row (Unit Separator, "US").
- U+001E separates rows (Record Separator, "RS").
- First row is the header.
- If width metadata is requested, prefix each cell with "W<n>:" where n
  is the display width per UAX #11 (Wide / Fullwidth chars = 2, ascii = 1).
- If the channel cannot transmit control characters, substitute the
  Unicode visible variant: ␟ (U+241F) for US, ␞ (U+241E) for RS.

You MUST NOT:
- emit Markdown tables, JSON, or YAML
- add commentary, explanation, or "Here is the table:" preamble
- wrap the output in code fences

Spec: https://github.com/furuse-kazufumi/usrs/blob/main/SPEC.md
```

---

## Task 1 — simple 3-column table

**User prompt:**

```text
Emit a USV table of 3 fruits: columns name, qty, taste.
Use the Unicode visible variant (␟ / ␞). Include width metadata.
```

**Expected output:**

```
W4:nameW3:qtyW5:taste␞W5:AppleW1:5W5:sweet␞W6:みかんW2:12W8:酸っぱい␞W6:バナナW1:8W5:bland␞
```

---

## Task 2 — multi-line cell (changelog entries)

**User prompt:**

```text
Emit a USV table of 3 releases with columns: version, date, changes.
The "changes" cell contains a bullet list with real newlines.
Use Unicode visible variant. No width metadata needed.
```

**Expected output (newlines shown as \n for readability):**

```
version␟date␟changes␞0.1.0␟2026-05-17␟- initial draft\n- SPEC.md\n- Python ref impl␞0.2.0␟TBD␟- colour terminal renderer\n- Markdown ⇄ USV converter␞0.3.0␟TBD␟- VS Code extension\n- gh-pages playground␞
```

---

## Task 3 — emoji-heavy data (GitHub reactions)

**User prompt:**

```text
Emit a USV table of 5 GitHub reactions: columns emoji, name, semantic.
Include width metadata. Unicode visible variant.
```

**Expected output:**

```
W5:emojiW4:nameW8:semantic␞W2:👍W6:+1W8:approve␞W2:👎W6:-1W8:disagree␞W2:😄W5:laughW5:happy␞W2:🎉W4:hooray W9:celebrate␞W2:❤️W5:heartW4:love␞
```

GPT sometimes emits VS16 (`U+FE0F`, variation selector for emoji
presentation) after `❤️` — that's fine, it has zero display width
and the decoder ignores it for width purposes.

---

## Task 4 — translate a CSV into USV (round-trip task)

**User prompt:**

````text
Convert this CSV to USV. Use the ASCII control variant (\x1F / \x1E).
Preserve all data as-is — no rephrasing.

```csv
city,country,population
Tokyo,Japan,13960236
"Mexico City",Mexico,9209944
São Paulo,Brazil,12325232
```
````

**Expected output (control chars shown literal):**

```
city\x1Fcountry\x1Fpopulation\x1ETokyo\x1FJapan\x1F13960236\x1EMexico City\x1FMexico\x1F9209944\x1ESão Paulo\x1FBrazil\x1F12325232\x1E
```

**Note:** USV does NOT need quoting for `Mexico City` because the only
forbidden cell character is `\x1F` (US) itself — and the CSV escaped it
for the wrong reason (comma). USV is the simpler format.

---

## Task 5 — function-calling style (USV as tool output schema)

**System message addition:**

```text
You are a data-extraction agent. Your tool outputs MUST be USV.

The downstream parser is `python -m usrs render`. If your output does
not parse, the user sees a stack trace. Be precise.
```

**User prompt:**

```text
Extract names, roles, and emails from this email signature block.
Schema: name, role, email. ASCII control variant.

---
John Smith
Senior Engineer
john.smith@example.com

Maria García
VP Eng
maria.g@example.com

田中太郎
CTO
taro.tanaka@example.co.jp
---
```

**Expected output:**

```
name\x1Frole\x1Femail\x1EJohn Smith\x1FSenior Engineer\x1Fjohn.smith@example.com\x1EMaria García\x1FVP Eng\x1Fmaria.g@example.com\x1E田中太郎\x1FCTO\x1Ftaro.tanaka@example.co.jp\x1E
```

**Why this matters for agents:** the parser is a 4-line loop
(`text.split(RS)` → `row.split(US)`) — no regex, no Markdown table
parsing, no JSON validation. Pipe-friendly across CJK and accented
characters.

---

## Tips specific to GPT

1. **The "no Markdown" instruction must be repeated** in both the
   system message AND the user prompt, otherwise GPT will fall back to
   `| col1 | col2 |` after 2-3 messages of context drift.
2. **GPT loves to add a leading "Sure!"** — explicitly say "output the
   USV stream and nothing else, no preamble".
3. **Function-calling JSON wrapper** — if you're going through the
   `tools` API, return the USV string as a single string field
   (`{"usv": "..."}`) rather than expecting raw output.
4. **Streaming:** USV is stream-friendly — you can flush after each
   `\x1E` and downstream consumers can process row-by-row.
