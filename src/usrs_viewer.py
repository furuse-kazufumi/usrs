# SPDX-License-Identifier: Apache-2.0
"""USV Viewer — Textual-based 2-pane viewer for .usv files.

Left pane: scrollable USV table with cell selection (DataTable widget).
Right pane: full cell content rendered in one of 3 modes:

  - plain     — raw text, preserves \\t indents and \\n newlines
  - markdown  — Markdown rendered (Textual built-in renderer)
  - html      — HTML escaped to plain text (safety default; UI explicitly
                does NOT execute HTML in the right pane to avoid XSS)

Quick start::

    pip install textual>=0.50
    python -m usrs_viewer examples/sales.usv

Keyboard shortcuts:
  arrow keys / hjkl  — move cell selection
  m                  — cycle render mode (plain → markdown → html → plain)
  q                  — quit

Reference implementation for the USRS / USV ecosystem. The intent is for
editor and terminal developers to embed similar 2-pane behaviour in their
products (VS Code, JetBrains, Neovim, Helix, Wezterm, iTerm2, etc.).
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import cast

try:
    from textual.app import App, ComposeResult
    from textual.binding import Binding
    from textual.containers import Horizontal, VerticalScroll
    from textual.widgets import DataTable, Footer, Header, Markdown, Static
except ImportError as e:  # pragma: no cover
    raise SystemExit(
        "Textual is required for the USV viewer. Install with:\n"
        "    pip install textual>=0.50\n"
        f"Original error: {e}"
    )

# Resolve the sibling `usrs` module regardless of how this file is invoked.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from usrs import ParsedTable, loads  # noqa: E402


RENDER_MODES: tuple[str, ...] = ("plain", "markdown", "html")


class UsvViewerApp(App):
    """A minimal 2-pane USV viewer."""

    CSS = """
    Screen {
        layout: vertical;
    }
    #panes {
        height: 1fr;
    }
    #left {
        width: 60%;
        border: solid $accent;
    }
    #right {
        width: 40%;
        border: solid $secondary;
        padding: 1 2;
    }
    DataTable {
        height: 1fr;
    }
    #mode_bar {
        dock: top;
        height: 1;
        background: $primary;
        color: $text;
        padding: 0 1;
    }
    """

    BINDINGS = [
        Binding("m", "cycle_mode", "Cycle Render Mode"),
        Binding("q", "quit", "Quit"),
        Binding("escape", "quit", "Quit"),
    ]

    def __init__(self, path: Path, mode: str = "plain") -> None:
        super().__init__()
        self._path = path
        self._mode = mode if mode in RENDER_MODES else "plain"
        text = path.read_text(encoding="utf-8")
        self._parsed: ParsedTable = loads(text)

    def compose(self) -> ComposeResult:
        yield Header(show_clock=False)
        yield Static(self._mode_bar_text(), id="mode_bar")
        with Horizontal(id="panes"):
            with VerticalScroll(id="left"):
                yield DataTable(zebra_stripes=True, cursor_type="cell", id="table")
            with VerticalScroll(id="right"):
                yield Markdown("Select a cell on the left.", id="content_md")
                yield Static("", id="content_plain")
        yield Footer()

    def _mode_bar_text(self) -> str:
        return f" 📄 {self._path.name}   mode: [b]{self._mode}[/b]   (press 'm' to cycle, 'q' to quit)"

    def on_mount(self) -> None:
        table = self.query_one("#table", DataTable)
        rows = self._parsed.rows
        if not rows:
            table.add_column("(empty)")
            return
        # Header row = first row
        header = rows[0]
        for idx, h in enumerate(header):
            # Width hint from parsed.widths if available
            w = self._parsed.widths[idx] if idx < len(self._parsed.widths) else 20
            table.add_column(_truncate(h, 30), width=max(8, w + 2))
        for row in rows[1:]:
            # Truncate long / multi-line cells for the table preview;
            # full content goes to the right pane.
            preview = [_truncate(c.replace("\n", " ⏎ ").replace("\t", " → "), 50) for c in row]
            # Pad short rows to header width
            while len(preview) < len(header):
                preview.append("")
            table.add_row(*preview)
        # Hide the markdown widget initially; show on selection
        self.query_one("#content_plain", Static).display = False
        self.query_one("#content_md", Markdown).display = True

    def on_data_table_cell_highlighted(self, event: DataTable.CellHighlighted) -> None:
        self._refresh_right_pane(event.coordinate.row, event.coordinate.column)

    def on_data_table_cell_selected(self, event: DataTable.CellSelected) -> None:
        self._refresh_right_pane(event.coordinate.row, event.coordinate.column)

    def _refresh_right_pane(self, row_idx: int, col_idx: int) -> None:
        # `row_idx` here is 0-based relative to DataTable (i.e. excludes header).
        data_rows = self._parsed.rows[1:]
        if not (0 <= row_idx < len(data_rows)):
            return
        row = data_rows[row_idx]
        if not (0 <= col_idx < len(row)):
            return
        cell = row[col_idx]
        md_widget = self.query_one("#content_md", Markdown)
        plain_widget = self.query_one("#content_plain", Static)
        if self._mode == "markdown":
            md_widget.display = True
            plain_widget.display = False
            md_widget.update(cell)
        elif self._mode == "html":
            md_widget.display = False
            plain_widget.display = True
            # Escape HTML to plain text — explicit safety. We do not execute HTML.
            from html import escape
            plain_widget.update(escape(cell))
        else:  # plain
            md_widget.display = False
            plain_widget.display = True
            plain_widget.update(cell)

    def action_cycle_mode(self) -> None:
        idx = RENDER_MODES.index(self._mode)
        self._mode = RENDER_MODES[(idx + 1) % len(RENDER_MODES)]
        self.query_one("#mode_bar", Static).update(self._mode_bar_text())
        table = self.query_one("#table", DataTable)
        coord = table.cursor_coordinate
        self._refresh_right_pane(coord.row, coord.column)


def _truncate(s: str, n: int) -> str:
    if len(s) <= n:
        return s
    return s[: n - 1] + "…"


def main(argv: list[str] | None = None) -> int:
    import argparse
    p = argparse.ArgumentParser(prog="usrs-viewer", description="2-pane USV viewer")
    p.add_argument("path", help=".usv file to view")
    p.add_argument("--mode", choices=RENDER_MODES, default="plain",
                   help="initial render mode for the right pane")
    args = p.parse_args(argv)
    path = Path(args.path)
    if not path.exists():
        print(f"File not found: {path}", file=sys.stderr)
        return 1
    UsvViewerApp(path=path, mode=args.mode).run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
