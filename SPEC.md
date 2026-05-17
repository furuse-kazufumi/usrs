# USRS — Unit/Record Separator + Width Metadata

**Version**: 0.1.0-draft (2026-05-17)
**Status**: RFC draft
**License**: Apache-2.0 + Commercial dual (FullSense conventions)

## 1. 何を解くか

タブ区切り (TSV) と CSV は半世紀前から使われているが、**罫線・整形描画と
セル幅が連動しない**ため、エディタ・ブラウザ・ターミナル間で表が崩れる:

- タブ幅が 4/8 等で設定依存
- CJK 全角・絵文字・絵文字修飾子 (ZWJ シーケンス) の表示幅補正なし
- proportional フォントでパディングが効かない
- Markdown table は renderer が trim する

データと描画の責務が混ざっているのが根本問題。

USRS は **データ + セル表示幅メタを 1 ストリームに同居** させ、レンダラが
そのメタに従って罫線を描画する体系を定める。

## 2. 区切り文字 = 罫線 (規範的、2026-05-17 大改訂)

ASCII 1967 から予約されている制御文字のうち、**core 仕様では 2 文字** のみを
使う。**この 2 つで表全体が記述可能**。

| 符号位置 | 名前 | 役割 | 罫線として |
|---|---|---|---|
| `U+001F` | UNIT SEPARATOR (US) | **横方向の区切り** (cell 間) | 縦罫線 `│` |
| `U+001E` | RECORD SEPARATOR (RS) | **縦方向の区切り** (row 間) | 横罫線 `─` |

> 💡 **コア設計判断 (1)**: 「区切り文字 = 罫線そのもの」という再解釈。
> **罫線情報を別途持たない**。US が出現したら **そこに縦罫線**、RS が出現したら
> **そこに横罫線**を引く。レンダラは box drawing 文字
> (`┌┬┐├┼┤└┴┘`) の交点判定だけ行えばよい。
>
> 💡 **コア設計判断 (2)**: 仕様の根幹は **US + RS の 2 文字のみ**。これ以上の
> 区切り文字は core 仕様に含めない。1 つの表ファイル全体を 2 文字で記述
> できることが学習容易性・実装容易性の両面で重要。

### 2.0 optional 拡張 (本仕様外、参考)

複数表を 1 ファイルに収めたい / バッチ送信したい場合のために、ASCII には
更に 2 つの区切り文字が予約されている。**core 仕様には含めない**:

| 符号位置 | 名前 | 役割 (optional) |
|---|---|---|
| `U+001D` | GROUP SEPARATOR (GS) | 複数表を 1 ファイルに収めるブロック区切り |
| `U+001C` | FILE SEPARATOR (FS) | ストリーミング送信用のファイル境界 |

これらは将来拡張で扱うが、**互換実装には必須でない**。読み手は GS/FS を
RS と同等の終端記号として扱ってよい (forward compatibility)。

### 2.1 文字の物理特性

これらは UTF-8 で 1 バイト、テキストエディタは表示しないが grep / awk /
sed では普通に処理できる。

### 2.2 パーサー規範 (規範的、2026-05-17 追加)

USV パーサーは以下の minimal ルールで実装可能:

1. **U+001E (RS) で表の境界・行の区切りを判定**:
   - 入力の最初の RS の前にコンテンツがあれば、それは 1 行目 (= ヘッダ
     候補) として扱う
   - RS が出現するたびに行を確定し、次の行のバッファを開始する
   - 末尾の RS は空行を作らない (trailing RS は許容、ignore)
2. **U+001F (US) で列の区切りを判定**:
   - 各行内で US が現れた位置で cell を分割
   - cell の中身は UTF-8 文字列 (制御文字を含まない、`W<n>:` 接頭辞は
     optional metadata)
3. **列数の決定**:
   - **列数 = max(各行の US の数) + 1**
   - US が 0 個の行は 1 列、US が 2 個の行は 3 列
   - 不揃いの行は **最大列数に合わせて右側を空 cell で補う** (renderer 自由、
     データ層は不揃いを保持してよい)
4. **改行・タブ・Markdown・HTML はすべて cell 内コンテンツ** (重要、CSV との差別化):
   - **予約された制御文字は US (U+001F) と RS (U+001E) の 2 文字のみ**
   - **それ以外の文字はすべて cell の中身として通過する**
   - 結果として cell 内に以下を自由に埋め込める:

   | 種別 | 扱い | 例 |
   |---|---|---|
   | 改行 `\n` / `\r\n` | cell 内改行 (マルチライン cell) | 詩、長文、コードスニペット |
   | タブ `\t` | cell 内インデント | コードブロック、構造化テキスト |
   | **Markdown** | cell 内 Markdown 記述 | `**bold**`, `[link](url)`, `# heading`, ``` ```code``` ``` |
   | **HTML** | cell 内 HTML タグ | `<b>bold</b>`, `<a href="...">`, `<svg>` |
   | 絵文字 / CJK | cell 内通過 | 🍎, 商品, 한국어 |
   | NUL `\0` (U+0000) | cell 内通過 (推奨しない) | binary-ish data も技術的には許容 |

   - **CSV の `"` 周りの quoting / escape ルールは存在しない** — 必要なし
   - renderer は cell content を **そのまま** あるいは **Markdown → HTML →
     plain text のいずれかに解釈** して表示する (renderer の責任)

### 2.3 Cell content の renderer 解釈モード (規範外、参考)

cell content をどう描画するかは renderer 自由だが、以下 3 モードが想定される:

| モード | 解釈 | ユースケース |
|---|---|---|
| **plain** (default) | cell content をそのまま等幅で描画。`\n` で改行、`\t` でタブ幅展開 | ターミナル `bat`、`cat` 等 |
| **markdown** | cell content を Markdown として render | ブラウザ、IDE preview |
| **html** | cell content を HTML として描画 (XSS リスクは受信側責任) | Web UI、信頼できる入力源 |

renderer は `%USRS render=markdown` のような header 拡張、または UI 側
設定で mode を切り替える (本仕様では mode 自体は規定しない)。

> ⚠️ **HTML モードのセキュリティ警告**: cell に raw HTML を許容すると XSS
> 注入リスク。USV を **信頼できない入力源** から読む場合は plain or
> markdown モードに留め、HTML render は禁止すること。仕様レベルでは
> 「HTML を埋められる」を保証するが、「HTML を render するかは renderer
> 判断」 — 強い分離。
   - 例:

```
"商品説明"␟"特徴"␞ジューシーで\n甘い熟成リンゴ␟3 種類混在\n各 1 個ずつ␞
                                       ↑ cell 内に改行             ↑ RS が来るまで cell 継続
```

   - renderer は cell 内 `\n` を `<br>` / 端末では複数行配置で render

擬似コード:

```python
def loads(text: str) -> list[list[str]]:
    rows = []
    for record in text.split("\x1e"):    # ① RS で行分割
        if not record:                    # trailing RS による空行は無視
            continue
        cells = record.split("\x1f")      # ② US で列分割
        rows.append(cells)
    n_cols = max((len(r) for r in rows), default=0)   # ③ 列数 = max
    return rows, n_cols
```

この 3 ステップが core 仕様の全て。実装者はこの 10 行を Python / Rust /
TypeScript / Go / C で書けば USV パーサーになる。

### 2.1 罫線描画の交点規則 (規範的)

レンダラは text 中の US / RS 位置を **罫線セグメント** として処理する:

```
データ:    商品␟個数␞Apple␟5␞みかん␟12
レイアウト: 商品 │ 個数
           ─────┼──────
           Apple│ 5
           ─────┼──────
           みかん│ 12
```

交点判定: 各 cell の右下角に US と RS が **両方** 接する場合、box drawing
の cross 文字 `┼` を配置。**罫線の長さ・厚さ・色は本仕様外** (renderer 自由)。

### 2.2 Unicode 可視変種 (重要)

ASCII 制御文字は HTTP form / メール pipeline で剥がされる場合がある。
そのため Unicode "Symbols for Control Codes" を可視変種として併用:

| ASCII 制御 | Unicode 可視 | 名前 |
|---|---|---|
| `U+001F` | `␟` (U+241F) | SYMBOL FOR UNIT SEPARATOR |
| `U+001E` | `␞` (U+241E) | SYMBOL FOR RECORD SEPARATOR |
| `U+001D` | `␝` (U+241D) | SYMBOL FOR GROUP SEPARATOR |
| `U+001C` | `␜` (U+241C) | SYMBOL FOR FILE SEPARATOR |

可視変種は **そのまま罫線として読める**:

```
商品␟個数␟備考␞Apple␟5␟甘い␞みかん␟12␟酸っぱい␞
```

renderer は両形式を等価に扱う (decoder で正規化、本仕様 § 7 参照)。

## 3. セル形式

各セルは以下の **2 つのフォーマット** のいずれかを取る。

### 3.1 Plain cell (デフォルト)

```
<UTF-8 文字列>
```

レンダラは East Asian Width (Unicode UAX #11) を計算して幅を求める。
**現行 TSV と互換**: 区切り文字を `\t` から `\x1F` に置換するだけで USRS 化できる。

### 3.2 Width-tagged cell (推奨、整形精度を上げたい場合)

```
W<digits>:<UTF-8 文字列>
```

`W` リテラル + 表示幅 (10 進、表示桁数) + `:` + 本文。例:

- `W2:Hi` — 表示幅 2 桁
- `W6:商品名` — 表示幅 6 桁 (全角 3 文字 × 2)
- `W10:📦 Box 1` — 絵文字 (2) + 空白 (1) + 英数 (5) + 余白 (2) で計 10

レンダラは width metadata があれば計算を省略し、無ければ UAX #11 で算出。
**幅指定は描画ヒントであり、正規データ部ではない** (剥がしても情報は失われない)。

## 4. ヘッダ行 (オプション)

ファイル先頭にメタ行を置ける (RS で終わる)。

```
%USRS v0.1.0; cols=3; widths=10,30,20\x1E
列名1\x1F列名2\x1F列名3\x1E
値1\x1F値2\x1F値3\x1E
```

`%USRS` で始まる行はメタ。`v=<version>`、`cols=<列数>`、`widths=<n,n,n>`
(default 列幅) を `;` 区切りで持つ。レンダラはこれを参照して罫線を引く。

## 5. レンダリングルール (規範的)

レンダラは以下を保証:

1. **列幅** = max(各行の同列 width-tag の最大値、UAX #11 計算値、header `widths`)
2. **罫線**: U+2500/2502/2510/250C/2518/2514 等の Box Drawing 文字で描く
3. **CJK セーフ**: 半角空白で右パディング。proportional font 環境では幅 hint を `<meta>` か CSS で渡す
4. **絵文字幅**: Unicode Emoji Spec の `text_presentation` / `emoji_presentation` を尊重
5. **column overflow**: 幅超過セルは末尾 `…` で truncate、または折り返し (renderer option)

## 6. ファイル拡張子 / MIME

- 拡張子: `.usrs`
- MIME type: `text/usrs` (proposed)、未登録時は `text/plain; charset=utf-8` で fallback

## 7. 既存形式との変換

| from | 変換ルール |
|---|---|
| TSV | `\t` → `\x1F`、`\n` → `\x1E`。lossless |
| CSV | (RFC 4180 に従い quoting 解除) → US/RS 区切り。`,` 中の `,` は quote 解除 |
| Markdown table | header → `%USRS widths=...`、各 `\|` → `\x1F`、行末 → `\x1E` |
| `.usrs` → TSV | width-tag 剥がして `\x1F` → `\t`、`\x1E` → `\n`。lossless (描画情報のみ消える) |

## 8. 既存ツールとの互換

- `cat file.usrs` — 制御文字が表示されないので「データだけ」が見える
- `awk -F$'\x1F' '{print $1}' file.usrs` — 普通に動作
- `grep` — 区切り文字を気にせず使える
- `git diff` — 制御文字を `^_` `^^` 等で表示するため可読

## 9. 参考実装 (本リポ)

- `src/usrs.py` — Python 参考実装 (encode/decode/render)
- `src/usrs.rs` — Rust 参考実装 (予定)
- `src/usrs.ts` — TypeScript 参考実装 (予定、Web Component 用)
- `examples/sales.usrs` — サンプルデータ
- `tests/test_roundtrip.py` — TSV ⇄ USRS のラウンドトリップ検証

## 10. 既存規格との関係

- ASCII (ANSI X3.4-1986 / ISO/IEC 646) の Information Separators を再活性化
- Unicode UAX #11 East Asian Width を幅計算規範として参照
- RFC 4180 (CSV) の補完仕様として位置付け
- TSV (IANA `text/tab-separated-values`) の後継候補

## 11. 商標 / コミュニティ

- プロジェクト名: **USRS** (Unit / Record Separator) または **USep**
- リポジトリ: 公開時に `github.com/<user>/usrs`
- 議論: GitHub Discussions + RFC 草案 PR

## 12. ロードマップ

| Phase | 内容 |
|---|---|
| **0.1.0** (本草案) | SPEC + Python encode/decode + TSV round-trip テスト |
| 0.2.0 | 端末 renderer (Box Drawing + ANSI color)、Markdown converter |
| 0.3.0 | VS Code extension (.usrs を表で表示) |
| 0.4.0 | Web Component (`<usrs-table>`)、Rust 実装 |
| 0.5.0 | gh-pages にプレイグラウンド、各種エディタプラグイン |
| 1.0.0 | RFC として IETF Draft 提出検討 |

## 13. 設計判断ログ

- **TAB を新文字に置き換えない**: TAB はインデント用途で広く使われており、表専用の新文字 (US) を別に用意する方が破壊が少ない
- **PUA (U+E000-U+F8FF) を使わない**: 既に存在する ASCII 制御文字を再活性化する方が標準準拠性が高い
- **バイナリ形式にしない**: テキストとして表示可能 (制御文字は不可視) で grep/awk 互換を保つことが普及には必須
- **width tag は optional**: 既存 TSV を 1 行 sed で USRS 化できる "low friction migration path" を死守
