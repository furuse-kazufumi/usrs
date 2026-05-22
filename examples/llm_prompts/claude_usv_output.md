# Claude — making it emit USV instead of Markdown tables

> Claude (Anthropic) is good at Markdown tables by default — but those
> tables routinely break when the data contains CJK, emoji, or multi-line
> cells. This page shows prompt templates that make Claude emit valid USV
> (Unit-Separated Values) instead, and example outputs you can decode with
> `usrs.loads()`.

All separators below are written as escape sequences for readability.
Real USV files contain the actual control characters `\x1F` (US) and
`\x1E` (RS). Either run the prompt and capture stdout, or ask Claude to
use the **Unicode visible variant** (`␟` / `␞`) when you can't safely
copy-paste control characters out of the chat UI.

---

## System / preamble (reusable)

```text
You are emitting data in USV (Unit-Separated Values) format, NOT Markdown.

Rules:
- Use U+001F (Unit Separator) between cells within a row.
- Use U+001E (Record Separator) between rows.
- The first row is the header.
- If the user wants width metadata, prefix each cell with "W<n>:" where
  <n> is the display width per Unicode UAX #11 East Asian Width
  (Wide / Fullwidth = 2, everything else = 1).
- If the channel cannot transmit control characters, use the Unicode
  visible variant: ␟ (U+241F) for US, ␞ (U+241E) for RS.
- Do NOT emit a Markdown table. Do NOT add explanatory prose unless
  asked. Output the USV stream and nothing else.

Spec: https://github.com/furuse-kazufumi/usrs/blob/main/SPEC.md
```

---

## Task 1 — simple 3-column table

**Prompt:**

```text
[paste system preamble above]

Emit a USV table of 3 fruits with columns: name, qty, taste.
Use the Unicode visible variant (␟ / ␞) so I can paste the result back.
Include width metadata.
```

**Expected output:**

```
W4:nameW3:qtyW5:taste␞W5:AppleW1:5W5:sweet␞W6:みかんW2:12W8:酸っぱい␞W6:バナナW1:8W5:bland␞
```

**Decode check:**

```python
from usrs import loads, render
text = open("out.usv", encoding="utf-8").read()
print(render(loads(text)))
```

---

## Task 2 — multi-line cell (Markdown can't do this)

**Prompt:**

```text
[paste system preamble above]

Emit a USV table of 2 servers with columns: hostname, role, notes.
The "notes" column should contain newline-separated bullet points
(real \n characters inside the cell — USV allows this).
Use the Unicode visible variant.
```

**Expected output (`\n` shown literal here for readability):**

```
hostname␟role␟notes␞web-01␟frontend␟- nginx 1.27\n- TLS via Let's Encrypt\n- rate-limited at 100 rps␞db-01␟postgres-primary␟- pg16\n- streaming replication to db-02\n- WAL archived to S3␞
```

**Why this matters:** Markdown tables can't carry newlines inside a
cell at all. CSV / TSV need quoting + escaping. USV just allows it.

---

## Task 3 — emoji-heavy data

**Prompt:**

```text
[paste system preamble above]

Emit a USV table of 4 reactions with columns: emoji, name, count.
Include width metadata so a renderer can align columns.
Use the Unicode visible variant.
```

**Expected output:**

```
W5:emojiW4:nameW5:count␞W2:🎉W11:tadaW3:142␞W2:🚀W10:rocketW3:89␞W2:🐛W3:bugW2:23␞W2:✨W8:sparklesW3:67␞
```

**Note on emoji width:** UAX #11 says most emoji are Wide (W=2), but
ZWJ-joined sequences (👨‍👩‍👧‍👦) are an open problem — Claude may
over-count. The renderer recomputes width from content if `with_width`
metadata is missing or wrong.

---

## Task 4 — CJK + ASCII mixed alignment

**Prompt:**

```text
[paste system preamble above]

Emit a USV table of 3 cities with columns: city (CJK), country, population.
Width metadata required. Use Unicode visible variant.
```

**Expected output:**

```
W4:cityW7:countryW10:population␞W6:東京W5:JapanW10:13,960,236␞W6:北京W5:ChinaW10:21,893,095␞W6:서울W5:KoreaW9:9,668,465␞
```

**Decoded render:**

```
┌────────┬─────────┬────────────┐
│ city   │ country │ population │
├────────┼─────────┼────────────┤
│ 東京   │ Japan   │ 13,960,236 │
│ 北京   │ China   │ 21,893,095 │
│ 서울   │ Korea   │  9,668,465 │
└────────┴─────────┴────────────┘
```

---

## Task 5 — structured tool output (Claude as data API)

**Prompt:**

```text
[paste system preamble above]

I'm going to give you free-form text. Extract entities and emit them as
a USV table with columns: entity, type, sentiment.
Use the ASCII control variant (\x1F / \x1E) — I'll pipe the output
through a parser. Width metadata not required.

Text: "Anthropic released Claude 4.7 with a 1M-token context window.
Reviewers loved the long-context performance but criticised the price."
```

**Expected output (control chars shown as \x1F / \x1E):**

```
entity\x1Ftype\x1Fsentiment\x1EAnthropic\x1Forg\x1Fneutral\x1EClaude 4.7\x1Fproduct\x1Fpositive\x1E1M-token context window\x1Ffeature\x1Fpositive\x1Eprice\x1Fattribute\x1Fnegative\x1E
```

This is the **agentic use case**: Claude emits a stream that another
program parses without regex-fighting Markdown.

---

## Tips for reliable output

1. **Be explicit about the variant** — ASCII (`\x1F` / `\x1E`) for
   machine pipelines, Unicode (`␟` / `␞`) when humans copy-paste.
2. **State "do not emit Markdown"** — the default tabular behaviour is
   strong, you need to override it.
3. **Width metadata is optional** but lets downstream renderers skip
   the UAX #11 lookup; emit it when you can.
4. **End with a Record Separator** — the spec allows but does not
   require a trailing RS; including one makes streaming parsers happier.
5. **Round-trip test:** pipe the output through `python -m usrs to-tsv`
   and compare with the source.
