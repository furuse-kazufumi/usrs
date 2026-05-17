# 関連研究・先行事例 (Related Work)

USRS / USV (Unit-Separated Values) と同じ・近い発想を持つ既存仕様や
ツールの調査。**重複リスクの確認** と **差別化軸の明確化** が目的。

> 注: ここでの調査は記憶 + 一般知識ベース。論文 RAG (`rad-research`
> skill) や Web 検索で補完すべき (本ドキュメントは初版、追記歓迎)。

## 1. ASCII US/RS を表データの区切りに使う発想

### 1.1 既存規格

| 名称 | 何 | USRS との差 |
|---|---|---|
| **ASCII 1967 / ANSI X3.4** | U+001C-001F を "Information Separators" として定義 | 規格としては存在するが、**普及した表データフォーマットへの採用例が無い** |
| **古いメインフレーム / 銀行系** | 一部の EBCDIC ベース exchange で US/RS を field/record 区切りに使用 | **特殊用途、汎用 OSS フォーマットとして整備されていない** |
| **MySQL / PostgreSQL の TAB-separated export** | `--fields-terminated-by` でカスタム可能、US 指定可 | 設定でしか使えず、ファイル形式として標準化されていない |

**結論**: ASCII US/RS を表データ区切りに使うアイデア自体は古典的 (60 年来
の既知)。しかし **広く普及した汎用ファイル形式 (CSV/TSV と並ぶ位置)
として整備された例は見つからない**。USRS が埋める空白がここにある。

### 1.2 「制御文字を区切りに使えば良いのに」という定期的議論

- **Hacker News / Stack Overflow** に過去 10 年以上、定期的に
  "Why aren't ASCII control chars used as CSV separators?" という議論が
  立つ (URL は web 検索で多数ヒット)
- いずれも「便利そうだけど誰も整備していない」で終わっている
- USRS は **その実装** を作ったことになる

## 2. 罫線 = 区切り文字 という発想

「区切り文字が罫線そのもの」というアイデアの先行例:

| 名称 | 区切り = 罫線? | USRS との差 |
|---|---|---|
| **Markdown table** | 部分的: `|` が縦罫線、`-` が横罫線として使われる | 入力時にすべて手書き、列幅指定不可、renderer が trim する |
| **reStructuredText Grid Tables** | はい: `+` `\|` `-` で全罫線描画 | 入力が極めて煩雑、自動整列なし、編集が苦痛 |
| **Org-mode Tables (Emacs)** | はい: `\|---\|---\|` 形式、自動整列 | Emacs 内限定、textbook outside の互換性なし |
| **AsciiDoc Tables** | 部分的 | `|` 区切り、罫線は renderer 任せ |
| **DBN-table / textile** | 似た発想 | レガシー、現役の普及形式ではない |

**USRS の独自性**: 「区切り **そのまま** が制御文字で、罫線描画はレンダラが
保証する」。**手で罫線を書かなくて済む** 点が org-mode / RST grid との
大きな差。

## 3. Width Metadata を持つテキスト表形式

| 名称 | width 持つ? | USRS との差 |
|---|---|---|
| **FWF (Fixed-Width Format)** | はい (位置で表現) | 各 cell が固定幅、データ長が cell 幅を超えると壊れる |
| **COBOL Copybook 形式** | はい (file 単位で定義) | レガシー、現行 OSS シーンで使われない |
| **JSON Schema + table data** | 別 file で定義 | 描画 hint は持たない、UI は別途 |
| **CSV + header.tsv (補助)** | 別 file 化が多い | USRS は inline で持つので 1 file 完結 |

**USRS の独自性**: width metadata を **cell 単位で optional 埋込** できる。
header で default を持ち、cell で上書きできる柔軟性。

## 4. CJK / 絵文字 / 全角整形対応

| 名称 | CJK 配慮 | USRS との差 |
|---|---|---|
| **Unicode UAX #11 East Asian Width** | 規範 (規格そのもの) | USRS が **参照する仕様**、USRS の競合ではない |
| **`column` (Unix util)** | 部分的 (locale 依存) | runtime 動作、USRS のような仕様ではない |
| **Python `tabulate`** | はい | ライブラリ、format ではない |
| **Python `rich`** | はい (Box Drawing) | ライブラリ、format ではない |
| **TermDB / Kitty Table protocol** | はい | Terminal escape sequence、不可視 |

**USRS の独自性**: **format 自体** が CJK / 全角 / 絵文字を最初から想定。
ライブラリやアプリ実装に依存しない。

## 5. Unicode "Symbols for Control Codes" (U+2400-241F) の利用

| 名称 | 用途 | USRS との差 |
|---|---|---|
| **Unicode 4.0+** | 制御文字を視覚化するための予約符号位置 | USRS は **これを実用フォーマットに採用した最初期例** の可能性 |
| **教科書・タイポグラフィ書** | 制御文字を本文中で示すための表記 | データ交換用途ではない |

**USRS の独自性**: U+241F / U+241E を「control char 剥がし耐性版」として
duality に組み込んだ点。**先例が確認できる範囲では無い**。

## 6. 「表データを 1 file で持つ」既存規格

| 名称 | バイナリ/テキスト | USRS との差 |
|---|---|---|
| **CSV (RFC 4180)** | テキスト | 整形描画なし、CJK 問題 |
| **TSV (IANA `text/tab-separated-values`)** | テキスト | タブ幅問題、CJK 問題 |
| **JSON Lines / NDJSON** | テキスト | 構造化されてるが表として render できない |
| **Apache Arrow / Parquet / ORC** | バイナリ | 高速だが人間可読でない |
| **Apache Arrow Flight** | バイナリ + 通信 | データ転送に特化 |
| **HL7 v2** | テキスト (専用区切り `|^~\&`) | 医療業界専用、汎用性なし |
| **EDIFACT** | テキスト (専用区切り `: + '`) | 国際取引専用 |
| **dbase / DBF** | バイナリ | レガシー |

**USRS の独自性**: 「**plain text で人間も grep でき、CJK でも崩れず、罫線も
インラインで持つ**」を全て満たす唯一の汎用 OSS format。

## 7. 評価まとめ

### 7.1 USRS の本質的新規性

| 観点 | 既存 | USRS の差別化 |
|---|---|---|
| ASCII US/RS 利用 | 60 年来既知の発想だが、汎用 OSS 形式に未整備 | **整備して提供する** |
| 区切り = 罫線 | Markdown / RST / Org がやっているが入力負荷大 | **制御文字 1 個 = 罫線 1 セグメントの直結** |
| Width metadata | FWF / COBOL は持つが古典的 / 不便 | **optional cell prefix、後方互換** |
| CJK 配慮 | UAX #11 規範はあるが format 採用例少 | **format 自体が CJK 前提** |
| Unicode 視覚変種 | U+241F-241E の使用例皆無 | **可視変種を duality に内包** |

### 7.2 重複リスク

- **完全重複の先例は見つからない**
- ASCII US/RS を表データ区切りに使うアイデア単体は古典的だが、**整備された
  OSS プロジェクトとして公開された例は確認できる範囲で無い**
- USRS は「**過去のアイデアに対する遅れた実装**」として位置付けられる可能性

### 7.3 USRS が「車輪の再発明」と批判されないために

- README で「ASCII US/RS の発想は 60 年前から既知」と明示
- 「**過去から知られていた発想を、現代のエコシステム (Unicode / 絵文字 /
  CJK / 各種エディタ) に統合した実装**」と位置付ける
- 先行事例 (Org-mode / RST grid / Pandoc) との **共存** を強調

### 7.4 さらに調査すべきこと (TODO)

- [ ] arXiv で "tabular text format" を検索、近年の論文発表があるか
- [ ] IETF / W3C で類似の RFC draft 提出履歴を確認
- [ ] 古い ANSI / ISO / ECMA 規格で US/RS の活用提案を再確認
- [ ] PyPI / npm で既存 `unit-separated` `record-separated` パッケージ調査
- [ ] Microsoft / Google / Apple の特許検索 (table format 関連の知財リスク確認)

## 8. 結論

> **USRS は 60 年来知られていたアイデアの整備された実装である**。
>
> 「車輪の再発明」のリスクは小さくない (HN で必ず指摘される) が、
> 「整備された OSS 形式として広く使える形に作った」価値は十分にある。
> 既存類似形式 (CSV / TSV / Markdown / Org / RST) との **共存** を
> 前提に、特定ニッチ (CJK / 罫線連動が必要な領域) で採用される
> ことを狙う。

## 9. 引用候補 (RFC / README で参照する場合)

- ANSI X3.4-1986 (ASCII): ISO/IEC 646:1991 後継、Information Separators の起源
- Unicode UAX #11: East Asian Width
- Unicode Control Pictures: U+2400-241F の規範定義
- RFC 4180 (CSV): 現行汎用 csv の規格
- Tiago Forte, *Building a Second Brain* (2022): データと描画の責務分離という発想の一般的根拠
