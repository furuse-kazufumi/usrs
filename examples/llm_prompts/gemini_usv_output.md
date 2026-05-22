# Gemini (Google) — making it emit USV instead of Markdown tables

> Gemini 1.5 / 2.0 / 2.5 default to Markdown tables and — like every
> other LLM — produce broken alignment on CJK / emoji / multi-line
> cells. This page shows prompt templates that make Gemini emit valid
> USV (Unit-Separated Values) instead.

Gemini's strong point is **long-context tabular data extraction** (it
will happily process a 100k-row CSV in one shot). USV is a perfect
output format for that use case because it's stream-friendly and
parses with a 4-line loop.

---

## System instructions (reusable)

```text
You output ONLY USV (Unit-Separated Values).

Separators:
- U+001F = Unit Separator (between cells)
- U+001E = Record Separator (between rows)
- First row is the header.
- Optional per-cell width prefix: "W<n>:<content>" where n is UAX #11
  display width (Wide/Fullwidth = 2, else = 1).
- Unicode visible variant: ␟ (U+241F) / ␞ (U+241E) — use when the
  channel strips control characters.

Forbidden:
- Markdown tables
- JSON / YAML / XML
- Any preamble, postamble, or commentary
- Code fences around the USV stream

Spec: https://github.com/furuse-kazufumi/usrs/blob/main/SPEC.md
```

---

## Task 1 — simple 3-column table

**Prompt:**

```text
Emit USV: 3 fruits, columns name / qty / taste.
Unicode visible variant. Width metadata included.
```

**Expected output:**

```
W4:nameW3:qtyW5:taste␞W5:AppleW1:5W5:sweet␞W6:みかんW2:12W8:酸っぱい␞W6:バナナW1:8W5:bland␞
```

---

## Task 2 — long-context extraction (Gemini's sweet spot)

**Prompt:**

```text
I'm pasting a 2000-line server log below. Extract every WARN or ERROR
line as a USV row with columns: timestamp, level, component, message.
ASCII control variant. No width metadata.

[... 2000 lines of log ...]
```

**Expected output (truncated, control chars shown literal):**

```
timestamp\x1Flevel\x1Fcomponent\x1Fmessage\x1E2026-05-22T10:14:03Z\x1FWARN\x1Fnginx\x1Fupstream timed out (110: Connection timed out)\x1E2026-05-22T10:14:07Z\x1FERROR\x1Fpostgres\x1Fdeadlock detected on relation users\x1E2026-05-22T10:15:12Z\x1FWARN\x1Fnginx\x1Fclient intended to send too large body\x1E...
```

**Why USV beats CSV here:** log messages routinely contain commas,
quotes, and newlines. With CSV you'd need quoting + escaping for ~30%
of rows. With USV the only forbidden character in a cell is `\x1F`
itself, which doesn't appear in human-written logs.

---

## Task 3 — multi-line cell (poem or code snippet table)

**Prompt:**

```text
Emit USV: 3 famous one-line Python tricks. Columns: name, code, why.
The "code" cell contains real Python with newlines.
Unicode visible variant.
```

**Expected output (newlines shown as \n):**

```
name␟code␟why␞walrus␟if (n := len(xs)) > 10:\n    print(n)␟assignment expression introduced in 3.8␞unpack␟a, *rest, b = [1,2,3,4,5]␟extended iterable unpacking␞ternary list␟[x if x>0 else 0 for x in xs]␟in-comprehension conditional␞
```

---

## Task 4 — emoji + CJK + accent (the "everything breaks" case)

**Prompt:**

```text
Emit USV: 5 world greetings. Columns: greeting (in native script),
language, region. Width metadata required. Unicode visible variant.
```

**Expected output:**

```
W8:greetingW10:languageW8:region␞W10:こんにちはW8:JapaneseW5:Japan␞W4:你好W7:ChineseW5:China␞W6:안녕W6:KoreanW5:Korea␞W7:HolaW7:SpanishW5:Spain␞W11:Здравствуй W7:RussianW6:Russia␞
```

**Decoded renders identically in any monospace terminal:**

```
┌────────────┬──────────┬────────┐
│ greeting   │ language │ region │
├────────────┼──────────┼────────┤
│ こんにちは │ Japanese │ Japan  │
│ 你好       │ Chinese  │ China  │
│ 안녕       │ Korean   │ Korea  │
│ Hola       │ Spanish  │ Spain  │
│ Здравствуй │ Russian  │ Russia │
└────────────┴──────────┴────────┘
```

---

## Task 5 — multimodal → USV (Gemini-specific superpower)

**Prompt (with image attached):**

```text
[image: a screenshot of a spreadsheet with 5 rows and 4 columns]

Read the table in the image and emit USV. Preserve cell values
exactly as shown — do not interpret or summarise. Columns in order
from left to right. ASCII control variant.
```

**Expected output (control chars literal):**

```
Date\x1FCustomer\x1FProduct\x1FAmount\x1E2026-05-01\x1FAcme Corp\x1FWidget A\x1F$1,250.00\x1E2026-05-03\x1FBeta Ltd\x1FWidget B\x1F$3,400.00\x1E2026-05-08\x1F株式会社γ\x1FGadget\x1F¥45,000\x1E2026-05-12\x1FDelta GmbH\x1FWidget A\x1F€890.50\x1E
```

**Why USV is ideal for OCR / multimodal output:** the model can't
accidentally produce malformed Markdown (missing pipe, extra dash) that
would derail a downstream parser. The format has exactly two structural
characters — both invisible in normal data — and everything else is
opaque payload.

---

## Tips specific to Gemini

1. **Safety filter quirk:** Gemini occasionally refuses to emit raw
   control characters (`\x1F`) as a "low-confidence safety" trigger.
   Workaround: always start with the **Unicode visible variant** (`␟`
   / `␞`), then post-process to ASCII if needed.
2. **Long-context advantage:** Gemini 2.5 Pro will happily process a
   million-token spreadsheet in one call. USV is stream-friendly so the
   output works even if it's gigabytes — pipe through `usrs.loads()`
   row by row.
3. **Multimodal:** images of tables → USV is one of the cleanest
   extraction targets because there's no escaping ambiguity (unlike CSV
   where commas-in-cells require quoting decisions).
4. **System instructions persist:** Gemini honours the "no Markdown"
   instruction more reliably than GPT across turns — but still
   re-state it if you see drift.
