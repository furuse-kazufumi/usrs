# USRS 普及戦略ガイドライン

> 「タブ区切りに代わる新しい区切り文字」というのは **大きすぎる提案**。
> 軽率なバズマーケでは普及しない。本ガイドラインは USRS を
> **正攻法で持続的に広める**ための施策を整理する。

## 0. 普及戦略の原則

1. **動くものを最優先** — 仕様だけでは普及しない。Python 参考実装 + VS Code
   plugin + Web Component の 3 つを動く状態で揃える
2. **既存ツールチェーンとの親和性** — TSV/CSV/Markdown との lossless 変換が
   必須。「既存ファイルを USRS 化する移行コスト」を限りなくゼロに
3. **段階的説得** — まず「タブ崩れに苦労した人」を狙う。マニア向け→開発者→
   一般ユーザーの順
4. **Honest disclosure** — 「全部解決する」と言わない。USRS の限界
   (proportional font / メール pipeline での制御文字剥がし等) を最初から開示
5. **コミュニティ駆動** — 1 人で広めるのは無理。RFC 化 + エディタ提供者との
   パートナーシップを通じて「標準」に近づける

## 1. 採用ファネル (Adoption Funnel)

```
発見 (Awareness)
  ↓
試用 (Trial)
  ↓
採用 (Adoption)
  ↓
推薦 (Advocacy)
```

各段階で何を提供すべきか:

| 段階 | 必要なもの | 指標 |
|---|---|---|
| 発見 | Qiita / dev.to / HN の記事、 ロゴ、1 行 hook | impressions, page views |
| 試用 | `pip install usrs` (1 行で入る)、Quick Start 5 分以内 | downloads, sample run |
| 採用 | VS Code extension、エディタ統合、Markdown 変換 | active installs, recurring use |
| 推薦 | RFC 草案、エディタ提供者との連携、論文/ブログ言及 | GitHub stars, fork, mentions |

## 2. チャネル別戦略

### 2.1 Qiita (日本語、優先度高)

- **記事 1**: `タブ幅 4 と 8 の戦争に終止符を — USRS という新しい区切り文字`
- **記事 2**: `CJK 全角の表を綺麗に描く方法 — UAX #11 と USRS`
- **記事 3**: `Markdown 表が崩れる理由と、USRS による解決`
- **記事 4**: `60 年前に予約されていた ASCII 制御文字を再活性化した話 (US/RS/GS/FS)`

各記事は `feedback_article_break_points` に従い ☕休憩ポイントを 3-4 個挟む。

### 2.2 LinkedIn (日本語のみ、組込翻訳に委譲)

- **投稿 1** (~850 字): USRS の概要 + GitHub repo 誘導
- **投稿 2** (~850 字): VS Code extension リリース時
- **投稿 3** (~850 字): 1.0.0 RFC 提出時

### 2.3 Hacker News / Lobsters / Reddit r/programming

- **タイトル案**: "USRS: bringing the 60-year-old ASCII Unit Separator back to life for proper table rendering"
- 投稿前に Show HN ガイドライン熟読、ライセンス・デモ・スクショ準備
- 攻撃的コメントへの応答テンプレ用意 (FAQ.md 参照)

### 2.4 dev.to / Medium (英語)

- **記事**: "Why your terminal tables break: an East-Asian-Width survival guide"
- USRS を解決策の 1 つとして紹介、競合 (Markdown table / RST grid table) と並べて比較

### 2.5 X (旧 Twitter) / Bluesky / Mastodon

- 短文 + GIF (USRS で表が綺麗に並ぶ動画) を 1 日 1 投稿、3 日連続
- hashtag: `#USRS` `#TSV` `#CJK` `#Unicode` `#Markdown`

### 2.6 GitHub Stars 戦略

- README にバッジ (stars / build / coverage)
- 各 issue を `good-first-issue` `help-wanted` 等の label で分類
- Discussions で「あなたのプロジェクトで USRS を試してくれたら教えて」と呼びかけ

## 3. メッセージング (Why → How → What)

Simon Sinek の Golden Circle に従い、**Why から語る**。

**Why** (信念):
> データと描画の責務が混ざっているのが、表が崩れる根本原因だ。
> 60 年前の ASCII 設計は正しかった。我々はそれを忘れていただけだ。

**How** (差別化):
> ASCII US/RS を再活性化し、Unicode 可視変種も同時サポート。
> セル幅メタを optional に持たせることで、既存 TSV から 1 行 sed で
> 移行できる low-friction migration path を死守する。

**What** (機能):
> Python / Rust / TypeScript の参考実装、VS Code extension、
> Web Component、TSV/CSV/Markdown 双方向変換。

各記事・投稿は **Why から始める**。「new format を作りました」では誰も聞かない。
「タブ幅 4 vs 8 の戦争で 60 年無駄にしてきた」と始めれば共感が得られる。

## 4. パートナーシップ — 各種エディタの GitHub で共有 (重要度最高)

普及の最大レバレッジは **エディタ・ターミナル提供者との連携**。仕様が
US + RS の 2 文字だけと極端に簡素なので、各エディタへの実装提案コストも
低い。**各 repo に Issue を立てるところから始める**。

### 4.1 ターゲット repo とアプローチ手順

| 対象 | repo | アプローチ |
|---|---|---|
| **VS Code** | `microsoft/vscode` | (1) Discussion で「`.usrs` filetype を組み込む価値」を問う。(2) 否定的なら独立 extension `vscode-usrs` を marketplace へ。(3) `*.usrs` を `tabular text` として grammar 登録 |
| **Neovim** | `neovim/neovim` + `nvim-treesitter/nvim-treesitter` | treesitter grammar 投稿、`set filetype=usrs` の autocmd plugin |
| **Vim (vim-polyglot)** | `sheerun/vim-polyglot` | filetype + syntax ファイルを PR |
| **Emacs** | `melpa/melpa` | `usrs-mode.el` を作って MELPA に登録 |
| **Sublime Text** | `wbond/package_control_channel` | `.tmLanguage` + table viewer plugin、Package Control に登録 |
| **JetBrains 全 IDE** | `JetBrains/intellij-platform` | Language plugin として `Plugins Marketplace` へ。Kotlin で書く |
| **Atom (sunsetted)** | (履歴のみ) | 公式 archive。Pulsar (Atom fork) を対象に |
| **Pulsar** | `pulsar-edit/pulsar` | grammar 提供 PR |
| **Zed** | `zed-industries/zed` | Tree-sitter grammar、`extensions` repo に PR |
| **Helix** | `helix-editor/helix` | `runtime/queries/` に query 追加 |
| **GitHub Linguist** | `github-linguist/linguist` | **これが効く**: `.usrs` を言語として GitHub が認識すれば、各 repo で自動 syntax highlight が効く。`samples/` に sample 追加 + `languages.yml` に登録 PR |
| **highlight.js** | `highlightjs/highlight.js` | web 上の syntax highlighting (Qiita 等が使う) |
| **Pygments** | `pygments/pygments` | docs 系 (Sphinx 等) の syntax highlighting |
| **Marked.js / markdown-it** | `markedjs/marked`, `markdown-it/markdown-it` | Markdown 内に USRS テーブルを埋め込めるよう plugin |
| **Pandoc** | `jgm/pandoc` | reader/writer module を `--from usrs --to markdown` で提供 |
| **iTerm2 / Wezterm / Alacritty / kitty** | 各 repo | terminal で renderer を内蔵する選択肢 (escape seq 拡張) |
| **GitHub Markdown** | `github/cmark-gfm` | GFM 拡張として `.usrs` block を render (中長期) |

### 4.2 各 repo への提案テンプレ (英語、コピペ可)

各 repo の Issue / Discussion に投稿するときの **テンプレ文** を用意。
過剰な売り込みを避け、礼節と必要十分な情報を保つ:

```markdown
# Proposal: support for `.usrs` (Unit/Record Separator with Width Metadata)

## Context
USRS is a small text format that reuses the 60-year-old ASCII control
characters `U+001F` (Unit Separator) and `U+001E` (Record Separator) as
**cell and row separators that double as the rendered grid lines**.
It targets the long-standing "tab width 4 vs 8" / "Markdown table column
shifts on CJK" problem.

- Spec: <link to SPEC.md>
- Reference implementation (Python): <link to repo>
- License: Apache-2.0

## Why this repo
We'd love `.usrs` to be displayable in {VS Code, Neovim, Helix, ...}
without an external viewer. Two non-invasive ways to do this:

1. **Filetype + simple syntax highlight only** — treat `U+001F` and
   `U+001E` as separator tokens, no further parsing. Trivial PR.
2. **Optional table renderer** — display `.usrs` as a Box-Drawing
   aligned table (similar to how some editors render `.md` tables).

## What we're asking
Are you open to (1) and/or (2)? If yes, we'll prepare a focused PR.
If no, no hard feelings — we have a list of alternative editors lined up.
```

### 4.3 順序とタイミング

エディタコミュニティへの並列アプローチ計画 (1.0.0 直前 4 週間で):

| 週 | アクション |
|---|---|
| 1 | GitHub Linguist (`linguist`) に PR を **最初** に投げる — これが通れば
他エディタの説得材料が一気に増える |
| 2 | Tree-sitter grammar を書いて Zed / Helix / Neovim へ PR (treesitter 経由は
配布チャネル共通なので 3 つ同時に効く) |
| 3 | VS Code / JetBrains / Sublime に extension/plugin 提出 |
| 4 | highlight.js / Pygments / Pandoc に PR (web/docs 表示の最終ピース) |

### 4.4 戦術的注意

- **いきなり PR を投げない**。各 repo の `CONTRIBUTING.md` を読み、
  Discussion / RFC プロセスがある場合はそれに従う。Linguist は
  `CONTRIBUTING.md` で「新言語追加には sample が要る」と明記している
- **否定的反応を受けても撤退しない**。1 つの repo がリジェクトしても、
  10 個チャネルがあれば 3-4 個は通る
- **採用される確率を上げる工夫**:
  - sample ファイルを 5 種類以上用意 (`.usrs` の examples 充実)
  - "in the wild" use case を示す (USRS 採用済プロジェクトのリスト)
  - 既存 user (GitHub stars / issue 活発さ) を客観数値で示す
- **コミュニティリーダーへの直接コンタクト**: 各 editor の core team
  メンバーは GitHub プロフィールに連絡先を公開していることが多い。
  Spam にならない範囲で 1 人 1 回までフォローアップ

## 5. 競合・先行事例の整理

普及戦略で必須なのは「先行事例との差別化」を明示すること:

| 既存 | 差別化軸 |
|---|---|
| **TSV / CSV** | 罫線連動なし、CJK 全角サポートなし — USRS は両方解決 |
| **Markdown table** | renderer が trim する、列幅指定不可 — USRS は明示できる |
| **RST grid table** | 入力時に罫線を手で描く必要 — USRS は自動 |
| **ASCII art table (古典)** | フォント依存 — USRS は UAX #11 規範 |
| **JSON Lines / NDJSON** | 表として render できない — USRS は両立 |
| **Apache Arrow / Parquet** | binary、人間可読でない — USRS は plain text |

「**plain text で人間も grep でき、かつ描画も綺麗**」が他にない USP。

## 6. ロゴ / ブランディング

- **シンボル**: ASCII US/RS をモチーフにした 4 マス grid。色は monochrome (#1F1E1D1C)
- **タグライン (jp)**: 「タブ幅 4 vs 8 の戦争に、終わりを」
- **タグライン (en)**: "Bringing the 60-year-old Unit Separator back to life."
- **フォント**: モノスペース系 (JetBrains Mono / IBM Plex Mono) — 表テーマに合う

## 7. 普及指標 (KPI)

| 指標 | 目標 (1.0.0 リリース時) |
|---|---|
| GitHub Stars | 500+ |
| `pip install usrs` 月間 downloads | 1,000+ |
| VS Code extension active installs | 200+ |
| Qiita / dev.to 記事言及数 | 20+ |
| エディタ提供者からの正式 fork / PR | 1+ |
| RFC / IETF Draft 提出 | 1 件 |

KPI は **目安**。USRS の本質的成功は「**読者が表崩れに悩まなくなる**」こと。

## 8. リソース (整備すべきもの)

- [ ] `docs/logo.svg` — ロゴ (4 マス grid)
- [ ] `docs/playground.html` — Web Component デモ
- [ ] `examples/sales.usrs`, `examples/i18n.usrs` — サンプル
- [ ] `examples/demo.gif` — Terminal で USRS render が綺麗に並ぶ動画
- [ ] `FAQ.md` — 想定 Q&A 30 件 (control char strip, font 依存, パフォーマンス等)
- [ ] `MIGRATION.md` — TSV/CSV/Markdown からの移行手順
- [ ] `COMPATIBILITY.md` — エディタ・ターミナル別の動作確認マトリクス

## 9. ガバナンス

- **意思決定**: BDFL モデル (現状: 作者 1 人)。将来は steering committee へ
- **PR レビュー**: 24h 以内に first response、48h 以内に merge or reject
- **RFC プロセス**: 大きな変更は GitHub Discussions で 1 週間以上意見募集
- **コミュニティ規約**: Contributor Covenant 2.1 を採用

## 10. アンチパターン (やってはいけないこと)

- **バズマーケ的な誇大宣伝**: 「TSV はもう終わり」と言わない。TSV はこれからも
  使われる。USRS は補完であって置換ではない
- **複雑なフォーマット拡張**: 仕様を 1 ページ以下に保つ。仕様が肥大化すると
  実装者が離れる
- **エコシステム破壊**: 既存ツール (awk / grep / sed) と互換を保つ。
  control char を使うのはそのため (これらは普通に動く)
- **特定言語依存**: 参考実装は Python だが、仕様自体は言語非依存。
  Rust / Go / TypeScript / Java / C / Lua 実装を歓迎
- **ライセンス制限**: Apache-2.0 は商用利用も自由。「OSS だが商用は要許可」
  のような制限はかけない (商用 SaaS だけは別契約モデル)

## 11. 普及活動のセルフチェックリスト

新しい施策を始める前に以下を自問:

- [ ] 動くものがあるか? (Python 参考実装、サンプル、CLI)
- [ ] 5 分 Quick Start が README にあるか?
- [ ] **Why から** メッセージしているか?
- [ ] 既存ツールとの互換性を保っているか?
- [ ] 限界 (アンチパターン) を開示しているか?
- [ ] パートナー候補に **聞く** ステップが入っているか? (いきなり PR でなく)
- [ ] 指標を観察可能か? (GitHub stars / downloads / mentions)

## 12. 関連プロジェクト

USRS は FullSense umbrella から独立した小さなプロジェクトだが、設計判断は
FullSense 設計哲学に従う:

- **Local 環境こそ AI の本来の居場所** — エディタも同じ。クラウド依存しない
- **責任所在を architecture level に持ち込む** — データと描画の責務を分離
- **多側面の思考を構造化** — 表という最も基本的な多側面情報を扱う
- **TRIZ で創造を構造に持ち込む** — 「タブ幅 vs 一意表示」の矛盾を US/RS 分離で解く
- **Honest disclosure** — proportional font 問題、制御 char 剥がし等を最初から開示
- **ファミリーで作る** — usrs は独立プロジェクトだが、llove TUI で render すれば
  llive の Brief 結果が綺麗に表示される連携も可能
