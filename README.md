# USRS — Unit/Record Separator Spec (file format: **USV** `.usv`)

> CSV / TSV に並ぶ **USV (Unit-Separated Values)** — 罫線描画と連動する
> 整形可能テキスト表形式。ASCII 1967 から眠っていた `U+001F` / `U+001E`
> を再活性化、Unicode 図形 `␟` / `␞` 形式も同時サポート。

| 規格 | 区切り文字 | 拡張子 | MIME |
|---|---|---|---|
| CSV | `,` | `.csv` | `text/csv` |
| TSV | `\t` (U+0009) | `.tsv` | `text/tab-separated-values` |
| **USV** | **`\x1f` (U+001F) + `\x1e` (U+001E)** | **`.usv`** | **`text/usv`** (proposed) |

[![License: Apache-2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Status: RFC draft](https://img.shields.io/badge/Status-RFC_draft-orange.svg)](SPEC.md)

## なぜ作るのか

タブ区切り (TSV) と CSV は半世紀前から表データの事実上の標準だが、
**罫線・整形描画とセル幅が連動しない** ため:

- タブ幅が 4/8 等で設定依存
- CJK 全角・絵文字の表示幅補正なし
- proportional フォントでパディングが効かない
- Markdown 表は renderer が空白を trim する

**データと描画の責務が混ざっている**ことが根本問題。USRS は「データ +
セル表示幅メタを 1 ストリームに同居」させ、エディタ・ブラウザ・
ターミナルが**同じ規則で罫線を引ける**世界を目指す。

## Quick Start

### Python

```python
from usrs import dumps, loads, render

rows = [
    ["商品", "個数", "備考"],
    ["Apple", "5", "甘い"],
    ["みかん", "12", "酸っぱい"],
]
text = dumps(rows, with_width=True, header_widths=[8, 4, 10])
print(render(loads(text)))
```

出力:

```
┌──────────┬──────┬────────────┐
│ 商品     │ 個数 │ 備考       │
├──────────┼──────┼────────────┤
│ Apple    │ 5    │ 甘い       │
│ みかん   │ 12   │ 酸っぱい   │
└──────────┴──────┴────────────┘
```

### CLI

```bash
# TSV → USRS 変換 (lossless)
python -m usrs from-tsv data.tsv > data.usrs

# USRS → アラインメント済の表 (端末表示)
python -m usrs render data.usrs

# USRS → TSV に戻す (lossless)
python -m usrs to-tsv data.usrs > data.tsv
```

## 仕様の核

| 役割 | ASCII 制御変種 | Unicode 可視変種 |
|---|---|---|
| セル間 (Unit) | `U+001F` | `␟` (U+241F) |
| 行間 (Record) | `U+001E` | `␞` (U+241E) |
| 表ブロック (Group) | `U+001D` | `␝` (U+241D) |
| ファイル (File) | `U+001C` | `␜` (U+241C) |

- **ASCII 制御変種** がデフォルト (TSV 互換、`\t` → `\x1F` の機械置換で導入可能)
- **Unicode 可視変種** は HTTP form / メール pipeline で制御文字が剥がされる
  場合に使用 (両形式は decoder で透過的に受け入れ)

セル幅メタは `W<digits>:<本文>` の prefix で表現:

```
W2:Hi    ← 表示幅 2 桁
W6:商品名  ← 表示幅 6 桁 (全角 3 文字)
```

詳細は [SPEC.md](SPEC.md) を参照。

## 既存規格との関係

- **ASCII 1967 / ISO/IEC 646** の Information Separators (U+001C-001F) を活用
- **Unicode UAX #11** East Asian Width を幅計算の規範として参照
- **Unicode Control Pictures** (U+2400-241F) を可視化変種に流用
- **RFC 4180 (CSV)** / **TSV (IANA `text/tab-separated-values`)** の後継候補
- **Markdown table** とは双方向変換可能 (`usrs from-md` / `usrs to-md` 予定)

## プロジェクト構成

```
usrs/
├── SPEC.md                # 規範的仕様 (RFC 草案)
├── README.md              # 本ファイル
├── PROMOTION.md           # 普及戦略ガイドライン
├── CONTRIBUTING.md        # コミュニティ参加ガイド
├── LICENSE                # Apache-2.0
├── src/
│   └── usrs.py            # Python 参考実装
├── examples/              # サンプルファイル (.usrs)
├── docs/                  # 設計判断ログ・ロゴ・図表
└── tests/                 # 回帰テスト
```

## ロードマップ

| Phase | 内容 |
|---|---|
| **0.1.0** (本草案) | SPEC + Python encode/decode + TSV round-trip テスト |
| 0.2.0 | 端末 renderer (色付き)、Markdown ⇄ USRS converter |
| 0.3.0 | VS Code extension (`.usrs` を表で表示) |
| 0.4.0 | Web Component (`<usrs-table>`)、Rust 実装 |
| 0.5.0 | gh-pages にプレイグラウンド、各種エディタプラグイン |
| 1.0.0 | RFC として IETF Draft 提出検討 |

## ライセンス

[Apache-2.0](LICENSE) (OSS) + Commercial dual-license。OSS 利用は自由、
商用 SaaS / SI 案件のみ別契約。

## コミュニティ

- 課題報告 / 機能要望: GitHub Issues
- 設計議論: GitHub Discussions
- 普及活動ガイド: [PROMOTION.md](PROMOTION.md)
- コントリビューションガイド: [CONTRIBUTING.md](CONTRIBUTING.md)
