# SPDX-License-Identifier: Apache-2.0
"""Tests for USRS reference implementation."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from usrs import (  # noqa: E402
    FS,
    FS_GLYPH,
    GS,
    GS_GLYPH,
    RS,
    RS_GLYPH,
    US,
    US_GLYPH,
    Header,
    display_width,
    dumps,
    from_tsv,
    loads,
    render,
    to_tsv,
)


# ---------------------------------------------------------------------------
# Width
# ---------------------------------------------------------------------------

def test_display_width_ascii():
    assert display_width("Hi") == 2
    assert display_width("Apple") == 5


def test_display_width_cjk():
    assert display_width("商品") == 4  # 2 fullwidth chars
    assert display_width("商品名") == 6


def test_display_width_mixed():
    assert display_width("Apple 商品") == 10   # 5 (Apple) + 1 (space) + 4 (商品)
    assert display_width("X商Y") == 4   # 1 + 2 + 1


def test_display_width_ignores_separators():
    assert display_width(f"A{US}B") == 2
    assert display_width(f"A{RS}B") == 2


# ---------------------------------------------------------------------------
# ASCII control style (default)
# ---------------------------------------------------------------------------

def test_dumps_loads_ascii_roundtrip():
    rows = [["Name", "Qty"], ["Apple", "5"], ["商品", "12"]]
    encoded = dumps(rows)
    assert US in encoded
    assert RS in encoded
    parsed = loads(encoded)
    assert parsed.rows == rows


def test_dumps_with_width_tags():
    rows = [["Apple", "商品"]]
    encoded = dumps(rows, with_width=True)
    assert "W5:Apple" in encoded
    assert "W4:商品" in encoded
    parsed = loads(encoded)
    assert parsed.rows == [["Apple", "商品"]]
    # Widths computed from tags + UAX #11
    assert parsed.widths == [5, 4]


def test_header_widths_propagate():
    rows = [["A", "B"], ["長い文", "X"]]
    encoded = dumps(rows, header_widths=[10, 4])
    parsed = loads(encoded)
    assert parsed.header is not None
    assert parsed.header.widths == [10, 4]
    assert parsed.widths[0] >= 10  # header width must be respected


# ---------------------------------------------------------------------------
# Unicode visible style
# ---------------------------------------------------------------------------

def test_dumps_unicode_style():
    rows = [["Name", "Qty"], ["Apple", "5"]]
    encoded = dumps(rows, style="unicode")
    assert US_GLYPH in encoded
    assert RS_GLYPH in encoded
    assert US not in encoded   # no control chars
    assert RS not in encoded


def test_loads_unicode_visible():
    """Encoder produces Unicode visible; decoder reads back identically."""
    rows = [["Name", "Qty"], ["Apple", "5"], ["商品", "12"]]
    encoded = dumps(rows, style="unicode")
    parsed = loads(encoded)
    assert parsed.rows == rows


def test_loads_mixed_separators():
    """A stream where some rows use ASCII US/RS and some use Unicode glyphs.

    Real-world scenario: HTTP form strips control chars from some rows but
    not others, or two systems produce slightly different USRS. The decoder
    must handle the mixture.
    """
    text = (
        f"Name{US}Qty{RS}"
        f"Apple{US_GLYPH}5{RS_GLYPH}"   # mixed
        f"商品{US}12{RS_GLYPH}"          # mixed within a row
    )
    parsed = loads(text)
    assert parsed.rows == [["Name", "Qty"], ["Apple", "5"], ["商品", "12"]]


def test_invalid_style_raises():
    import pytest
    with pytest.raises(ValueError):
        dumps([["a"]], style="weird")


def test_bom_handling():
    """UTF-8 BOM at the start of the input is stripped silently."""
    bom = "﻿"
    rows = [["Hi", "There"]]
    encoded = bom + dumps(rows)
    parsed = loads(encoded)
    assert parsed.rows == rows


# ---------------------------------------------------------------------------
# Render — box-drawing table
# ---------------------------------------------------------------------------

def test_render_returns_box_drawn_table():
    rows = [["A", "B"], ["1", "2"]]
    out = render(loads(dumps(rows)))
    assert "│" in out
    assert "┌" in out and "┘" in out
    assert "A" in out
    assert "B" in out


def test_render_cjk_alignment():
    rows = [["Name", "Qty"], ["商品", "12"]]
    out = render(loads(dumps(rows, with_width=True)))
    # Confirm the line containing the CJK cell does not collapse columns
    cjk_line = next(l for l in out.splitlines() if "商品" in l)
    pipe_count = cjk_line.count("│")
    assert pipe_count == 3   # left + middle + right


# ---------------------------------------------------------------------------
# TSV ⇄ USRS lossless round-trip
# ---------------------------------------------------------------------------

def test_tsv_to_usrs_and_back_is_lossless():
    original = "Name\tQty\nApple\t5\n商品\t12"
    usrs_text = from_tsv(original)
    assert US in usrs_text
    assert RS in usrs_text
    tsv_back = to_tsv(usrs_text)
    # Trailing newline handling — both formats can lose final RS/\n; ignore
    assert tsv_back.strip() == original.strip()


def test_to_tsv_strips_width_tags():
    rows = [["Apple", "5"]]
    usrs_text = dumps(rows, with_width=True)
    tsv = to_tsv(usrs_text)
    assert "W5:" not in tsv
    assert "Apple\t5" in tsv


# ---------------------------------------------------------------------------
# Header serialisation
# ---------------------------------------------------------------------------

def test_header_serialises_with_widths():
    h = Header(cols=3, widths=[10, 5, 20])
    s = h.serialise()
    assert s.startswith("%USRS")
    assert "cols=3" in s
    assert "widths=10,5,20" in s


# ---------------------------------------------------------------------------
# 列数決定ルール (規範): n_cols = max(各行の US 数) + 1
# ---------------------------------------------------------------------------

def test_n_cols_from_max_us_count():
    """A row with the most US separators wins; shorter rows keep their length."""
    # 3 cols (2 US), 2 cols (1 US), 4 cols (3 US)
    text = f"A{US}B{US}C{RS}D{US}E{RS}F{US}G{US}H{US}I{RS}"
    parsed = loads(text)
    assert parsed.rows == [["A", "B", "C"], ["D", "E"], ["F", "G", "H", "I"]]
    # Width vector size = max columns = 4
    assert len(parsed.widths) == 4


def test_trailing_rs_does_not_create_empty_row():
    """Trailing RS is treated as terminator, not as an empty row marker."""
    text = f"A{US}B{RS}"
    parsed = loads(text)
    assert parsed.rows == [["A", "B"]]
    assert len(parsed.rows) == 1


def test_no_us_means_single_column():
    """0 US in a row means 1 column."""
    text = f"hello{RS}world{RS}"
    parsed = loads(text)
    assert parsed.rows == [["hello"], ["world"]]
    assert len(parsed.widths) == 1


# ---------------------------------------------------------------------------
# マルチラインセル: \n はセル内改行 (CSV との差別化)
# ---------------------------------------------------------------------------

def test_newline_in_cell_is_preserved():
    """A \\n inside a cell stays inside the cell — NOT a row terminator."""
    text = f"商品説明{US}特徴{RS}ジューシーで\n甘い熟成リンゴ{US}3 種類混在\n各 1 個ずつ{RS}"
    parsed = loads(text)
    assert len(parsed.rows) == 2  # 2 rows, not 4 lines
    assert parsed.rows[1][0] == "ジューシーで\n甘い熟成リンゴ"
    assert parsed.rows[1][1] == "3 種類混在\n各 1 個ずつ"


def test_cr_in_cell_is_preserved():
    """\\r and \\r\\n also stay inside cells."""
    text = f"A{RS}line1\r\nline2{RS}"
    parsed = loads(text)
    assert parsed.rows == [["A"], ["line1\r\nline2"]]


def test_no_csv_quoting_needed_for_newlines():
    """USV needs no quoting rules — newlines are first-class in cells."""
    rows = [
        ["title", "body"],
        ["poem", "Roses are red,\nViolets are blue,\nUSV does not need quotes,\nand neither do you."],
    ]
    text = dumps(rows)
    # Encoded form must NOT contain CSV-style quotes around the multi-line cell
    assert '"' not in text
    # Round-trip preserves the newlines
    parsed = loads(text)
    assert parsed.rows[1][1].count("\n") == 3


# ---------------------------------------------------------------------------
# Cell content freedom: tab / Markdown / HTML are all just cell content
# ---------------------------------------------------------------------------

def test_tab_in_cell_is_cell_content():
    """\\t is NOT a column separator in USV — it's cell-internal indentation."""
    code = "def f():\n\treturn 42"   # Python function with tab indent
    rows = [["snippet"], [code]]
    parsed = loads(dumps(rows))
    assert parsed.rows[1][0] == code
    assert "\t" in parsed.rows[1][0]
    # Crucially: the tab does NOT cause a split into multiple columns
    assert len(parsed.rows[1]) == 1


def test_markdown_in_cell_passes_through():
    """Markdown syntax in a cell is preserved verbatim — renderer interprets."""
    md = "## Section\n\n**Bold**, *italic*, `code`, [link](https://example.com).\n\n- list 1\n- list 2"
    rows = [["doc"], [md]]
    parsed = loads(dumps(rows))
    assert parsed.rows[1][0] == md
    # Markdown control chars (`*`, `#`, `[]`, backtick) must survive
    for token in ("##", "**", "*italic*", "`code`", "[link]", "(https"):
        assert token in parsed.rows[1][0]


def test_html_in_cell_passes_through():
    """HTML in a cell is preserved — security is the renderer's responsibility."""
    html = '<b>bold</b> and <a href="https://example.com">link</a><br/><svg width="10"/>'
    rows = [["html_cell"], [html]]
    parsed = loads(dumps(rows))
    assert parsed.rows[1][0] == html
    # No quoting / escaping — the raw HTML is intact
    assert "<b>" in parsed.rows[1][0]
    assert "<svg" in parsed.rows[1][0]


def test_cell_with_tab_indent_markdown_html_combo():
    """All three (tab, Markdown, HTML) in the same cell — USV is agnostic."""
    cell = "## Hello\n\tindented line\n<br/><kbd>Ctrl</kbd>+<kbd>C</kbd>"
    rows = [["mixed"], [cell]]
    parsed = loads(dumps(rows))
    assert parsed.rows[1][0] == cell
    assert "\t" in parsed.rows[1][0]
    assert "<kbd>" in parsed.rows[1][0]
    assert "## " in parsed.rows[1][0]
