# USV — CJK や絵文字で崩れない表データ形式

> **痛み**: Markdown 表は `みかん` や `😀`、改行入りセルが 1 つ混じるだけで
> renderer ごとに違う形に崩れる。
>
> **解決**: **USV (Unit-Separated Values)** — ASCII 1967 の `U+001F` /
> `U+001E` 区切り文字 + セル表示幅メタデータを 1 ストリームに同居させ、
> エディタ・ブラウザ・端末が**同じ規則で罫線を引ける**ようにした小さな形式。

<!-- TODO: 30 秒 GIF を追加 — 「Markdown 崩れる → .usv に切替 → 全環境で揃う」 -->
<!-- placeholder: docs/assets/usv-demo.gif -->

[![License: Apache-2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Status: RFC draft](https://img.shields.io/badge/Status-RFC_draft-orange.svg)](SPEC.md)
[English README](README.md) ・ [SPEC](SPEC.md) ・ [Discussion #1](https://github.com/furuse-kazufumi/usrs/discussions/1) ・ [SixArm/usv #14 (復活提案)](https://github.com/SixArm/usv/issues/14)

---

## 60 秒で要点

| 形式 | 区切り | CJK / 絵文字で崩れる? | 改行入りセルは? | 往復可逆? |
|---|---|---|---|---|
| CSV | `,` | 崩れる (renderer 依存) | 引用符 + escape 必要 | 角ケース注意 (RFC 4180) |
| TSV | `\t` | 崩れる (tab 幅 = 4? 8?) | 不可 | 可 (cell に tab 不可) |
| Markdown 表 | `\|` | **崩れる** (非 ASCII 全般) | **不可** (構文違反) | n/a (描画形式) |
| **USV** | **`\x1F`** (Unit) + **`\x1E`** (Record) | **崩れない** (UAX #11 幅タグ) | **可** (任意文字 OK) | **可** (TSV ⇄ USV) |

---

## Quick start (3 行)

```python
from usrs import dumps, loads, render

text = dumps([["商品","個数","備考"], ["Apple","5","甘い"], ["みかん","12","酸っぱい"]], with_width=True)
print(render(loads(text)))
```

出力 (どの monospace 端末でも同じ見た目):

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
python -m usrs from-tsv  data.tsv  > data.usv   # TSV → USV (可逆)
python -m usrs render    data.usv               # 端末に整形表示
python -m usrs to-tsv    data.usv  > data.tsv   # USV → TSV (可逆)
```

---

## Before / After — Markdown vs USV

CJK・絵文字・改行入りセルが混在する実例。

### Before — Markdown (崩れる)

````markdown
| Product | Qty | Note          |
|---------|-----|---------------|
| Apple   | 5   | sweet         |
| みかん  | 12  | 酸っぱい 🍊   |
| バナナ  | 8   | 常温保存可
   (室温 25℃ 以下)            |
````

GitHub では列ずれ + 改行で構文破綻。VS Code preview、Obsidian、pandoc で
それぞれ違って描画される。`室温 25℃` のパイプ似文字は問題ないが、セル
内改行で Markdown parser が即死する。

### After — USV (`.usv`)

```python
from usrs import dumps
rows = [
    ["Product", "Qty", "Note"],
    ["Apple",   "5",   "sweet"],
    ["みかん",  "12",  "酸っぱい 🍊"],
    ["バナナ",  "8",   "常温保存可\n(室温 25℃ 以下)"],   # 改行 OK
]
print(dumps(rows, with_width=True))
```

USV を理解する任意の renderer (端末の `render()`、将来の VS Code 拡張、
将来の `<usv-table>` Web Component) が**同じ**整列・改行尊重の表を描く
— 幅メタデータがデータと同じ stream に乗っているため。

5 つの追加事例は [examples/comparison/markdown_table_breaks.md](examples/comparison/markdown_table_breaks.md)
を参照。

---

## なぜ `U+001F` は安全か (gotchas 含めて正直に)

ASCII は 1967 年に `U+001C`-`U+001F` を **Information Separators** として
予約 — まさにこの用途のため — そしてほぼ誰も使っていない。実データと
衝突しないのが本質。

**問題なく通る:**
- ファイル I/O、パイプ、ソケット、sqlite TEXT カラム、JSON 文字列 (`` で
  escape)、zip アーカイブ、git blob、tar、S3 オブジェクト
- 現代の端末 (未知の C0 コードを既定で無視)
- UTF-8 clean なツールチェーン全般

**剥がされる可能性:**
- HTML フォーム送信、一部のメールゲートウェイ、「リッチテキスト」
  エディタの貼付フィルタ、古い shell の素朴な `printf "%s"`

**そのために USV には Unicode 可視変種** — `␟` (U+241F) / `␞` (U+241E)
— があり、decoder は両方受け入れる。pipeline に応じて wire 形式を選べる
が、データは同じ。

→ 完全規則は [SPEC.md §3](SPEC.md)。限界・非目標は
  [PROMOTION.md §0](PROMOTION.md) に正直に明記。

---

## リポジトリ構成

```
usrs/
├── SPEC.md                # 規範的仕様 (RFC 草案)
├── README.md  README_JA.md
├── src/usrs.py            # Python 参考実装 (~330 LOC)
├── examples/
│   ├── sales.usv          # 小サンプル
│   ├── sales_unicode.usv  # 同データ、U+241F 変種
│   ├── llm_prompts/       # Claude / GPT / Gemini 用 prompt テンプレ
│   └── comparison/        # Markdown 崩れ比較
├── docs/                  # 設計判断ログ・関連研究・連絡計画
└── tests/                 # 23 件 round-trip + 端ケース test
```

---

## ロードマップ

| Phase | 内容 |
|---|---|
| **0.1.0** (本草案) | SPEC + Python encode/decode + TSV round-trip |
| 0.2.0 | 端末 renderer (色付き)、Markdown ⇄ USV converter |
| 0.3.0 | VS Code extension (`.usv` を表で表示) |
| 0.4.0 | Web Component (`<usv-table>`)、Rust 実装 |
| 0.5.0 | gh-pages プレイグラウンド、各種エディタプラグイン |
| 1.0.0 | IETF Draft 提出 |

---

## 関連研究

USV は**初の試みではない**。[SixArm/usv](https://github.com/SixArm/usv)
(Joel Parker Henderson, 2022 — 現在停滞) は IETF Draft v01 まで到達後に
止まった。我々は**復活提案**を [SixArm/usv#14](https://github.com/SixArm/usv/issues/14)
で upstream に投げた — 拡張を取り込んでもらうか、共著で fresh IETF
draft を出すかの 2 択。先行例マップ全体は
[docs/RELATED_WORK.md](docs/RELATED_WORK.md) (ASCII 1967, RFC 4180,
IANA TSV, UAX #11, Control Pictures) を参照。

コミュニティ議論は
[Discussion #1](https://github.com/furuse-kazufumi/usrs/discussions/1)。

---

## ライセンス

[Apache-2.0](LICENSE) (OSS) + Commercial dual-license。OSS 利用は自由、
商用 SaaS / SI 案件のみ別契約。

## コミュニティ

- 課題報告 / 機能要望 → GitHub Issues
- 設計議論 → [GitHub Discussions](https://github.com/furuse-kazufumi/usrs/discussions)
- 普及戦略 → [PROMOTION.md](PROMOTION.md)
- コントリビューションガイド → [CONTRIBUTING.md](CONTRIBUTING.md)
