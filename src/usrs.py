# SPDX-License-Identifier: Apache-2.0
"""USRS — Unit/Record Separator + Width Metadata.

Reference implementation. Encode tabular data into a UTF-8 stream that
uses ASCII Information Separators (U+001F = US, U+001E = RS, U+001D = GS,
U+001C = FS) and optional per-cell width metadata so renderers can draw
aligned tables across editors / browsers / terminals.

See ../SPEC.md for the formal specification.

Quick start:

    from usrs import dumps, loads, render
    rows = [["Name", "Qty", "備考"], ["Apple", "5", "甘い"]]
    text = dumps(rows, with_width=True, header_widths=[10, 4, 6])
    table = render(loads(text))
    print(table)
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass

US = "\x1f"   # Unit (cell) separator
RS = "\x1e"   # Record (row) separator
GS = "\x1d"   # Group (table block) separator
FS = "\x1c"   # File separator

# Unicode "Symbols for Control Codes" — visible glyphs for the same logical
# separators. Many systems strip ASCII control characters (HTTP forms, email
# normalisation, paste filters); the Unicode visible variants survive those
# pipelines while remaining machine-distinguishable.
US_GLYPH = "␟"   # ␟ SYMBOL FOR UNIT SEPARATOR
RS_GLYPH = "␞"   # ␞ SYMBOL FOR RECORD SEPARATOR
GS_GLYPH = "␝"   # ␝ SYMBOL FOR GROUP SEPARATOR
FS_GLYPH = "␜"   # ␜ SYMBOL FOR FILE SEPARATOR

# Decoder accepts either form; the encoder picks based on a Style flag.
_US_ANY = (US, US_GLYPH)
_RS_ANY = (RS, RS_GLYPH)
_GS_ANY = (GS, GS_GLYPH)
_FS_ANY = (FS, FS_GLYPH)


def _normalise_separators(text: str) -> str:
    """Replace Unicode visible separators with their ASCII control equivalents,
    so the rest of the pipeline only has to handle one form."""
    return (
        text
        .replace(US_GLYPH, US)
        .replace(RS_GLYPH, RS)
        .replace(GS_GLYPH, GS)
        .replace(FS_GLYPH, FS)
    )


VERSION = "0.1.0-draft"


# ---------------------------------------------------------------------------
# Width calculation — Unicode UAX #11 East Asian Width
# ---------------------------------------------------------------------------

def display_width(s: str) -> int:
    """Compute terminal display width per UAX #11.

    Returns 2 for Wide/Fullwidth (W/F) and 1 for everything else. Control
    chars contribute 0. Zero-width joiners (ZWJ) are treated as 0 — emoji
    sequences may still over-count, but this gets us 95% there in pure stdlib.
    """
    w = 0
    for ch in s:
        if ch in (US, RS, GS, FS):
            continue  # control chars in our format itself — don't render
        cat = unicodedata.category(ch)
        if cat.startswith("C"):
            continue
        eaw = unicodedata.east_asian_width(ch)
        w += 2 if eaw in ("W", "F") else 1
    return w


# ---------------------------------------------------------------------------
# Encode / Decode
# ---------------------------------------------------------------------------

_WIDTH_TAG_RE = re.compile(r"^W(\d+):(.*)$", re.DOTALL)


@dataclass
class Header:
    """Optional `%USRS v=... cols=... widths=...` metadata line."""

    version: str = VERSION
    cols: int | None = None
    widths: list[int] | None = None

    def serialise(self) -> str:
        parts = [f"v={self.version}"]
        if self.cols is not None:
            parts.append(f"cols={self.cols}")
        if self.widths is not None:
            parts.append("widths=" + ",".join(str(w) for w in self.widths))
        return "%USRS " + "; ".join(parts)


def dumps(
    rows: list[list[str]],
    *,
    header: Header | None = None,
    with_width: bool = False,
    header_widths: list[int] | None = None,
    style: str = "ascii",
) -> str:
    """Encode rows into a USRS string.

    Args:
        rows: list of rows, each row a list of cell strings
        header: optional %USRS metadata to prepend
        with_width: emit each cell with `W<n>:` prefix for renderer hints
        header_widths: shortcut — adds widths=... to header (creates one if absent)
        style: 'ascii' (default, uses U+001F/U+001E control chars) or
               'unicode' (uses U+241F/U+241E visible glyphs — survives
               systems that strip control characters)
    """
    if style not in ("ascii", "unicode"):
        raise ValueError(f"style must be 'ascii' or 'unicode', got {style!r}")
    us = US if style == "ascii" else US_GLYPH
    rs = RS if style == "ascii" else RS_GLYPH
    parts: list[str] = []
    if header_widths is not None:
        if header is None:
            header = Header(widths=header_widths, cols=len(header_widths))
        else:
            header.widths = header_widths
            if header.cols is None:
                header.cols = len(header_widths)
    if header is not None:
        parts.append(header.serialise() + rs)
    for row in rows:
        encoded_cells: list[str] = []
        for cell in row:
            if with_width:
                w = display_width(cell)
                encoded_cells.append(f"W{w}:{cell}")
            else:
                encoded_cells.append(cell)
        parts.append(us.join(encoded_cells) + rs)
    return "".join(parts)


@dataclass
class ParsedTable:
    header: Header | None
    rows: list[list[str]]
    widths: list[int]  # computed per column (max of width-tag, UAX #11)


def loads(text: str) -> ParsedTable:
    """Parse a USRS string into rows + computed column widths.

    Accepts **both** ASCII control variant (U+001F/U+001E) and Unicode
    visible variant (U+241F/U+241E). Mixed inputs are also handled.
    """
    if not text:
        return ParsedTable(header=None, rows=[], widths=[])
    # Normalise Unicode visible separators to ASCII control variants
    text = _normalise_separators(text)
    # Strip optional UTF-8 BOM if present
    if text.startswith("﻿"):
        text = text[1:]
    # Split into records, ignore trailing empty record
    records = text.split(RS)
    if records and records[-1] == "":
        records.pop()
    header: Header | None = None
    rows: list[list[str]] = []
    for rec in records:
        if rec.startswith("%USRS"):
            header = _parse_header(rec)
            continue
        cells = rec.split(US)
        parsed_cells: list[str] = []
        for cell in cells:
            m = _WIDTH_TAG_RE.match(cell)
            if m:
                parsed_cells.append(m.group(2))
            else:
                parsed_cells.append(cell)
        rows.append(parsed_cells)
    # Compute per-column widths
    if not rows:
        widths = list(header.widths) if header and header.widths else []
    else:
        n_cols = max(len(r) for r in rows)
        widths = [0] * n_cols
        for r in rows:
            for i, cell in enumerate(r):
                w = display_width(cell)
                if w > widths[i]:
                    widths[i] = w
        # Header widths can override (if larger)
        if header and header.widths:
            for i, hw in enumerate(header.widths):
                if i < len(widths) and hw > widths[i]:
                    widths[i] = hw
    return ParsedTable(header=header, rows=rows, widths=widths)


def _parse_header(line: str) -> Header:
    """Parse '%USRS v=0.1.0; cols=3; widths=10,30,20' into a Header."""
    body = line[len("%USRS"):].strip()
    parts = [p.strip() for p in body.split(";") if p.strip()]
    h = Header()
    for p in parts:
        if "=" not in p:
            continue
        k, v = (s.strip() for s in p.split("=", 1))
        if k == "v":
            h.version = v
        elif k == "cols":
            try:
                h.cols = int(v)
            except ValueError:
                pass
        elif k == "widths":
            try:
                h.widths = [int(x) for x in v.split(",")]
            except ValueError:
                h.widths = None
    return h


# ---------------------------------------------------------------------------
# Render — Box Drawing aligned table
# ---------------------------------------------------------------------------

# Unicode Box Drawing Characters
_TL, _T, _TR = "┌", "┬", "┐"
_ML, _M, _MR = "├", "┼", "┤"
_BL, _B, _BR = "└", "┴", "┘"
_H, _V = "─", "│"


def render(parsed: ParsedTable, *, header_row: bool = True) -> str:
    """Render a parsed USRS table as an aligned ASCII/Unicode box-drawn table.

    The first row is treated as the header row by default (separator line
    drawn beneath it). Width comes from ``parsed.widths`` so the result is
    consistent across renderers.
    """
    if not parsed.rows:
        return ""

    widths = parsed.widths
    sep_top    = _TL + _T.join(_H * (w + 2) for w in widths) + _TR
    sep_middle = _ML + _M.join(_H * (w + 2) for w in widths) + _MR
    sep_bottom = _BL + _B.join(_H * (w + 2) for w in widths) + _BR

    lines: list[str] = [sep_top]
    for idx, row in enumerate(parsed.rows):
        cells_padded: list[str] = []
        for i, w in enumerate(widths):
            cell = row[i] if i < len(row) else ""
            actual = display_width(cell)
            pad = max(0, w - actual)
            cells_padded.append(" " + cell + " " * pad + " ")
        lines.append(_V + _V.join(cells_padded) + _V)
        if header_row and idx == 0 and len(parsed.rows) > 1:
            lines.append(sep_middle)
    lines.append(sep_bottom)
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Format converters
# ---------------------------------------------------------------------------

def from_tsv(text: str) -> str:
    """Lossless TSV → USRS. \\t → US, \\n → RS."""
    return text.replace("\t", US).replace("\n", RS)


def to_tsv(text: str) -> str:
    """USRS → TSV. Strips width tags, replaces separators."""
    out_lines: list[str] = []
    for rec in text.split(RS):
        if not rec or rec.startswith("%USRS"):
            continue
        cells = []
        for cell in rec.split(US):
            m = _WIDTH_TAG_RE.match(cell)
            cells.append(m.group(2) if m else cell)
        out_lines.append("\t".join(cells))
    return "\n".join(out_lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _cli() -> int:
    import argparse
    import sys

    p = argparse.ArgumentParser(prog="usrs")
    p.add_argument("command", choices=("render", "from-tsv", "to-tsv"))
    p.add_argument("path", nargs="?", default="-", help="input file or - for stdin")
    args = p.parse_args()

    if args.path == "-":
        text = sys.stdin.read()
    else:
        from pathlib import Path
        text = Path(args.path).read_text(encoding="utf-8")

    if args.command == "render":
        print(render(loads(text)))
    elif args.command == "from-tsv":
        sys.stdout.write(from_tsv(text))
    elif args.command == "to-tsv":
        sys.stdout.write(to_tsv(text))
    return 0


if __name__ == "__main__":
    raise SystemExit(_cli())
