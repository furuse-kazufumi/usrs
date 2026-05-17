# USV Viewer Showcase — 各エディタ・ターミナル開発者向け事例

USRS / USV の **2 ペインビューワー事例** を、各エディタ・ターミナル
開発者に「こういう UI を組み込んでくれないか」と提案するための共有素材。

## 1. 提案する UI 体験

```
┌──────────────────────────────────────┬──────────────────────────┐
│  📄 sales.usv   mode: markdown       │                          │
├──────────────────────────────────────┼──────────────────────────┤
│ 商品     │ 個数 │ 備考                │  ## みかん                │
│──────────┼──────┼─────────────────── │                          │
│ Apple    │ 5    │ 甘い                │  - 旬は冬                 │
│▶みかん   │ 12   │ 酸っぱい(冬が旬)     │  - **酸っぱい**           │
│ バナナ   │ 8    │ 常温保存可          │  - 詳細: [Citrus]([url]) │
└──────────────────────────────────────┴──────────────────────────┘
   ↑ cell 選択                         ↑ 選択 cell の full content を render
```

**左ペイン**: USV テーブル (アラインメント済、罫線連動)。矢印キーで cell 選択。

**右ペイン**: 選択 cell の **full content** を表示。3 モード切替可能 (`m` キー):
- `plain` — そのままの文字列 (タブ・改行・制御文字も保持)
- `markdown` — Markdown を render (見出し / リスト / リンク / コード)
- `html` — HTML を escape 後 plain 表示 (XSS 安全側)

## 2. なぜこの UI が必要か

| ユースケース | 現状の問題 | 2 ペイン UI の解決 |
|---|---|---|
| 長いセル (数行のコード / 詩 / 説明文) | TSV / CSV では行が崩れて見えない | 右ペインで full content を見られる |
| Markdown を埋め込んだ表 (README / docs) | renderer で markup が消える / 崩れる | 右ペインで render される |
| HTML / SVG を埋め込んだ表 (UI library 用 spec) | text editor では tag 文字が並ぶだけ | mode 切替で意図通り表示 |
| 多言語混在 (CJK / RTL / 絵文字) | TSV の幅崩れ | 左ペインは USRS 罫線、右で全文 |

## 3. 参考実装

| 言語 | 場所 | ライブラリ |
|---|---|---|
| **Python** | `src/usrs_viewer.py` | Textual (TUI) |
| Rust (予定) | `src/usrs_viewer.rs` | ratatui / crossterm |
| TypeScript (予定) | `src/usrs_viewer.ts` | Web Components |

Python 版起動:

```bash
pip install textual>=0.50
python -m usrs_viewer examples/sales.usv
```

## 4. 各種エディタへの組み込み提案

USRS の発想を **各種エディタ / ターミナルで再現** してくれることを期待。
提案テンプレ:

### 4.1 VS Code

```markdown
# Proposal: 2-pane viewer for `.usv` files

VS Code has the Markdown Preview side-by-side feature. Extending the same
pattern to `.usv`:

- main editor pane shows the raw `.usv` text or an aligned table
- preview pane shows the cell content under cursor (Markdown / HTML rendered)

Extension API hooks needed:
- `vscode.commands.registerCommand` for cycle mode
- `vscode.window.createWebviewPanel` for the preview
- file decoration provider to highlight U+001F / U+001E

Reference: <https://github.com/furuse-kazufumi/usrs/blob/main/src/usrs_viewer.py>
```

### 4.2 Neovim / Helix (Tree-sitter)

- `tree-sitter-usv` grammar で US/RS をトークン化
- `:UsvSplit` コマンドで右側にプレビューバッファを開く
- `<C-w>l` で行き来、`m` でモード切替

### 4.3 JetBrains IDEs

- Language plugin として `.usv` filetype + 2-pane editor を提供
- Kotlin 実装で `EditorEx` + `JBSplitter` を使う

### 4.4 ターミナル (iTerm2 / Wezterm / Alacritty)

- 端末自体に「`bat file.usv` → 自動でアラインメント表示」を組み込む
- 拡張モード: マウスでセル選択 → ステータスバーに full content

### 4.5 Web (Mintlify / GitBook / Docusaurus)

- `<usv-table src="data.usv">` Web Component
- 内蔵で 2 ペイン (mobile では accordion 形式)

## 5. デモ素材 (整備中)

- [ ] `examples/demo.gif` — viewer の動作録画 (asciinema → gif)
- [ ] `examples/screenshot_*.png` — 各モード (plain / markdown / html) のスクショ
- [ ] `examples/large_table.usv` — 1000 行サンプル (パフォーマンス検証用)
- [ ] `examples/multilang.usv` — ja/en/zh/ko/ar/he 混在サンプル
- [ ] `examples/markdown_heavy.usv` — Markdown 多用サンプル
- [ ] `examples/html_dashboard.usv` — HTML 表現サンプル (SVG / kbd / details)

## 6. llove 統合 (FullSense umbrella)

USV viewer は llove (FullSense TUI) に **F26: USV Table Widget** として
統合予定:

- llive の Brief 結果を USV 形式で出力 → llove で 2 ペイン表示
- llove F16 (game arena) の状態履歴を USV テーブル化
- llove F22 (テトリス) のリプレイログを USV テーブル化

詳細は llove repo の REQUIREMENTS.md (該当 FR が追加されたら) を参照。

## 7. 各エディタへの共有先 repo リスト

PR / Issue を投げる順序 (PROMOTION.md も参照):

1. `github-linguist/linguist` — `.usv` を言語として認識させる (最優先)
2. `tree-sitter/tree-sitter` org に `tree-sitter-usv` 公開
3. `microsoft/vscode` Discussion で「USV preview」提案
4. `helix-editor/helix` / `zed-industries/zed` に Tree-sitter 経由で
5. `neovim/neovim` / `vim/vim` に filetype/syntax 提案
6. `JetBrains/intellij-platform` plugin marketplace に extension
7. `iTerm2-Mac/iTerm2` / `wez/wezterm` / `kitty` に terminal hook 提案
8. `markedjs/marked` / `markdown-it/markdown-it` に USV embed plugin
9. `jgm/pandoc` に `usv` reader/writer
10. `microsoft/playwright` / Web Components シーンに USV viewer

## 8. 採用判断の指標

各エディタは「**追加コストが低く、ユーザー価値が高い**」と判断したら採用
してくれる。USRS の場合:

- 仕様: US + RS 2 文字のみ、SPEC 1 ページ
- 実装: 参考実装 200 行未満
- ユーザー価値: タブ幅問題 + CJK 問題 + マルチライン cell 問題を同時解消

これら 3 拍子が揃った format は他に類がない。
