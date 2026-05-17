# 公開手順 — USRS / USV プロジェクトを世界に出す

このファイルはユーザー (作者) 向けの **GitHub 公開と各メディア投稿の
チェックリスト**。Claude は手順とテンプレを用意するが、**API トークン
が必要な操作 (push / PR / SNS 投稿) は作者が実行する**。

## 1. GitHub 公開 (最優先)

### 1.1 Repo 作成 (作者作業)

GitHub Web UI または `gh` CLI で **`furuse-kazufumi/usrs`** をプライベート
ではなく **公開 (Public)** リポジトリとして作成。

```bash
# gh CLI を使う場合 (作者が実行):
gh repo create furuse-kazufumi/usrs --public \
    --description "USV (Unit-Separated Values) — CSV/TSV 後継、罫線連動 + マルチライン cell + Markdown/HTML 埋込 OK" \
    --homepage "https://github.com/furuse-kazufumi/usrs"
```

### 1.2 Remote 設定と初回 push

```bash
cd D:/projects/usrs
git remote add origin git@github.com:furuse-kazufumi/usrs.git
# (HTTPS の場合: git remote add origin https://github.com/furuse-kazufumi/usrs.git)
git branch -M main
git push -u origin main
```

### 1.3 公開後のリポジトリ設定 (GitHub 上、作者作業)

- **About** セクション: description + tags (`text-format`, `csv`,
  `tsv`, `tabular`, `unicode`, `ascii`, `apache-2.0`)
- **Topics** タグ: 上記 + `cjk` `markdown` `terminal`
- **Discussions** を有効化 (RFC 議論用)
- **Issues template**: バグ報告 / 機能要望 / spec 議論の 3 種
- **GitHub Pages** を有効 (`docs/` から、または別 branch)

## 2. Linguist PR (普及戦略の起点)

`github-linguist/linguist` に PR を投げる手順 (作者作業):

```bash
gh repo fork github-linguist/linguist --clone --remote
cd linguist
# 1. lib/linguist/languages.yml に追加:
#   USV:
#     type: data
#     extensions:
#       - ".usv"
#     ace_mode: text
#     tm_scope: source.usv
# 2. samples/USV/sales.usv をコピー
# 3. テスト走行 + PR
```

PR title 案: `feat: Add USV (Unit-Separated Values) data format`

## 3. メディア投稿の優先順

### 3.1 Qiita (日本語、最優先)

ファイル: `fullsense/docs/articles/2026-05-18/QIITA_USV_jp.md` (作成済)
- 配信: 公開準備完了後すぐ
- ハッシュタグ: `#TSV` `#CSV` `#Unicode` `#エディタ` `#普及`

### 3.2 LinkedIn (日本語、組込翻訳)

ファイル: `fullsense/docs/articles/2026-05-18/LinkedIn_USV_jp.md`

### 3.3 Hacker News (英語、Show HN)

ファイル: `fullsense/docs/articles/2026-05-18/HN_USV_en.md`
- タイトル: `Show HN: USV – CSV/TSV's modern successor for CJK, multi-line cells, and Markdown/HTML`
- 投稿時間: 米西海岸 月曜朝 (PT 08:00-10:00) が黄金

### 3.4 dev.to (英語、長文)

ファイル: `fullsense/docs/articles/2026-05-18/DEVTO_USV_en.md`

### 3.5 X (旧 Twitter) / Mastodon / Bluesky

短文 + GIF。GIF は `examples/demo.gif` (asciinema → gif 変換、要録画)

### 3.6 Reddit r/programming / r/golang / r/rust 等

- title: "I built USV, a CSV/TSV alternative with universal cell content (Markdown, HTML, multi-line, CJK)"
- 各 subreddit のルール確認、self-promotion 制約に従う

## 4. AI/LLM 文脈の特別 angle

USV の **AI ⇄ 人間コミュニケーションの負荷削減** という側面が、本来想定
していたよりも大きい価値:

- LLM が表データを出力するとき、Markdown 表が崩れる問題が消える
- LLM input prompt に USV を渡せば、tokenizer が US/RS を 1 token として
  扱うため、CSV/TSV より trick less
- 人間 → AI: 表を USV で書けば quoting/escape 不要、書きやすい
- AI → 人間: USV で返せば render は受信側に任せる、AI の責任が小さい

この angle を強調した投稿先候補:
- **AI コミュニティ** (LangChain Discord, Anthropic forum, OpenAI dev forum)
- **Prompt engineering 系**: PromptHub, LearnPrompting.org
- **r/LocalLLaMA, r/ChatGPT, r/MachineLearning**

## 5. パートナーシップ 直接コンタクト先

普及をブーストする「公式ステークホルダー」:

| 対象 | 連絡先 |
|---|---|
| **Anthropic Claude team** | feedback フォーム、または X で言及 |
| **Microsoft VS Code team** | discussions / Erich Gamma 系の team accounts |
| **GitHub Linguist maintainers** | PR で直接 |
| **Pandoc (John MacFarlane)** | repo issue + メール |
| **Wezterm / iTerm2 maintainer** | GH issue |

## 6. 採用追跡 (KPI ダッシュボード)

公開後 30 日でチェック:

- [ ] GitHub Stars: 50+
- [ ] Linguist PR: open / merged のいずれか
- [ ] Tree-sitter grammar: 草案 commit (本 repo or 別 repo)
- [ ] 採用エディタ: 1 つ以上で `.usv` syntax が認識される
- [ ] Qiita LGTM 数: 30+
- [ ] HN front page 到達: yes/no
- [ ] Anthropic / OpenAI から言及: あり/なし

## 7. 公開時のセルフチェック

- [ ] LICENSE が repo root にある (Apache-2.0)
- [ ] README に Quick Start が 5 分以内
- [ ] SPEC.md が単独で読める (前提知識不要)
- [ ] tests が pass する (CI 設定: GitHub Actions、Python 3.11/3.12 マトリクス)
- [ ] CONTRIBUTING.md でコミュニティ参加方法が明確
- [ ] PROMOTION.md / SHOWCASE.md で各エディタへの提案テンプレが揃う
- [ ] examples/ にサンプルが 3 種類以上
- [ ] CHANGELOG.md (今後の version 追跡用、現状 v0.1.0-draft)
- [ ] CODE_OF_CONDUCT.md (Contributor Covenant 2.1)
