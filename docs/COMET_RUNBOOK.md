# Perplexity Comet 用 Runbook — USRS / USV 公開と SixArm 連絡

> このファイルは **Perplexity Comet (AI ブラウザエージェント)** にそのまま
> 読ませて自動実行してもらうための手順書。各 step は (1) 操作対象 URL、
> (2) 操作内容、(3) 完了条件 を明示。
>
> 実行アカウント情報:
> - GitHub username: **furuse-kazufumi**
> - email: **kazufumi@furuse.work**
> - 対象 repo: **furuse-kazufumi/usrs**
> - ローカルパス: `D:/projects/usrs/`

---

## Step 0 — 前提環境の確認

**操作**:
1. `https://github.com/furuse-kazufumi` を開く
2. ログイン済みであることを確認 (右上にアバター表示)
3. 未ログインなら GitHub にログイン

**完了条件**: GitHub にログイン済、furuse-kazufumi アカウントで操作可能

---

## Step 1 — GitHub Repository を作成

**操作**:
1. `https://github.com/new` を開く
2. フォームに以下を入力:
   - **Repository name**: `usrs`
   - **Description**: `USV (Unit-Separated Values) — CSV/TSV 後継、罫線連動 + マルチライン cell + Markdown/HTML 埋込 OK / Apache-2.0`
   - **Visibility**: `Public` (重要 — Private にしない)
   - **Initialize this repository**: **すべてのチェックを外す** (README/.gitignore/LICENSE は既にローカルにある)
3. 「**Create repository**」ボタンをクリック

**完了条件**: `https://github.com/furuse-kazufumi/usrs` ページが「empty repo, push your code」を表示している

---

## Step 2 — ローカルから初回 push

**操作** (ターミナルで実行、Comet がターミナルアクセス可能なら):
```bash
cd D:/projects/usrs
git remote add origin git@github.com:furuse-kazufumi/usrs.git
git branch -M main
git push -u origin main
```

(HTTPS なら `https://github.com/furuse-kazufumi/usrs.git`)

**完了条件**: `git push` の出力で `main -> main` が確認できる。GitHub ページをリロードすると README.md / SPEC.md など全ファイルが表示される

---

## Step 3 — Repository 設定 (Web UI)

**操作**:
1. `https://github.com/furuse-kazufumi/usrs/settings` を開く
2. **About** セクションを設定 (右上の歯車アイコン):
   - Description: `USV — CSV/TSV 後継、罫線連動 + マルチライン cell + Markdown/HTML 埋込 OK`
   - Website: 空欄で OK
   - Topics: `text-format`, `csv`, `tsv`, `tabular`, `unicode`, `ascii`, `apache-2.0`, `cjk`, `markdown`, `terminal`, `usv`, `llm`, `ai`
3. **Features** で以下を有効化:
   - Issues: ✓ (有効)
   - Discussions: ✓ (**有効化、RFC 議論用**)
   - Wiki: 任意 (お好み)
4. **Pages** を必要なら有効化 (Source: `main` ブランチ `/docs` フォルダ)

**完了条件**: Repository ページの上部に Discussions タブが表示される

---

## Step 4 — SixArm/usv に Issue を立てる (公開記録の起点)

**操作**:
1. `https://github.com/SixArm/usv/issues/new` を開く
2. **Title** に以下を入力:
   ```
   Reviving USV — proposal to refresh the spec and resubmit a fresh IETF Draft v02
   ```
3. **Description** に以下をそのままコピペ:

```markdown
Hi Joel,

I've been following the USV concept with great interest. I noticed
[`draft-unicode-separated-values-01`](https://datatracker.ietf.org/doc/draft-unicode-separated-values/)
expired in 2024 and the work hasn't progressed toward IANA/IETF since.
The format deserves another push — especially now that LLM/AI tooling
desperately needs a robust tabular text format that survives Markdown /
HTML / CJK / multi-line content without escaping.

I'd like to help revive it. I've prototyped three additions that I
think strengthen the spec without changing its core:

1. **Grid-line semantics** — define US as the vertical rule and RS as
   the horizontal rule, so the separators double as rendering hints
   (no extra metadata needed for renderers to draw aligned tables)
2. **Optional cell width metadata** (`W<n>:cell` prefix) compatible
   with Unicode UAX #11 (East Asian Width). Decoders that ignore the
   prefix get plain text; renderers that read it get aligned output
   for CJK / emoji
3. **A 2-pane viewer reference implementation** in Python (Textual TUI)
   that demonstrates Markdown / HTML cell rendering side-by-side with
   the table — useful as a showcase for editor / terminal integrators

I have a small prototype repo with these additions, a 31-test suite
(all passing), and a draft promotion strategy for engaging editor
projects (Linguist / VS Code / Neovim / Helix / Zed / JetBrains).

Two paths from here, and I'm flexible on which one:

- **Option A**: Contribute upstream to SixArm/usv as a series of PRs
  (spec text + reference impl + viewer + promotion docs)
- **Option B**: Work with you as **co-author on a fresh
  `draft-unicode-separated-values-02`** to resubmit to IETF, refreshing
  the spec with the additions and reactivating the standards path

Would you be open to either? I'm happy to do most of the writing /
review work; I just want to make sure your original vision is honored
and that the credit reflects your foundational contribution.

About me:
- Japanese OSS developer, individual contributor
- Building the FullSense umbrella OSS (llive / llove / llmesh) in my spare time
- Prototype repo: https://github.com/furuse-kazufumi/usrs

Thanks for the foundational work on USV. Looking forward to your thoughts.

Best regards,
Kazufumi Furuse (furuse-kazufumi)
Email: kazufumi@furuse.work
```

4. **Submit new issue** ボタンをクリック
5. 投稿された Issue の URL をメモする (例: `https://github.com/SixArm/usv/issues/N`)

**完了条件**: Issue が public に投稿され、URL が取得できる

---

## Step 5 — Joel に直接メール送信

**操作**:
1. メールクライアント (Gmail / Outlook / 任意) を開く
2. 以下を入力:
   - **To**: `joel@joelparkerhenderson.com`
   - **From**: `kazufumi@furuse.work`
   - **Subject**: `Reviving USV — proposal via GitHub Issue #<番号>` (Step 4 で取得した Issue 番号)
   - **Body**:

```
Hi Joel,

I just opened an issue on github.com/SixArm/usv:

  <Step 4 で取得した Issue URL>

It's a proposal to help revive the USV work — the IETF draft expired
in 2024 and I'd like to either contribute as upstream PRs or co-author
a fresh draft-02 with you. Three concrete additions are described in
the issue (grid-line semantics, optional width metadata, a 2-pane
viewer).

I emailed instead of waiting purely on GitHub notifications since the
datatracker noted your email might be stale; if this address is also
out of date please let me know how best to reach you.

Best regards,
Kazufumi Furuse
GitHub: @furuse-kazufumi
Email: kazufumi@furuse.work
Prototype: https://github.com/furuse-kazufumi/usrs
```

3. **送信**

**完了条件**: メール送信完了。Sent box に記録される

---

## Step 6 — Qiita 記事を公開

**操作**:
1. `https://qiita.com/drafts/new` を開く (Qiita にログイン済前提、未ログインなら https://qiita.com/ でログイン)
2. **タイトル**: `CSV/TSV の後継を作ろうとしたら、既に SixArm USV があった — それでも普及に協力する話`
3. **本文**: ローカル `D:/projects/fullsense/docs/articles/2026-05-18/QIITA_USV_jp.md` の内容をコピペ、ただし冒頭に以下を追加:

```markdown
> 📝 **重要な追記**: 本記事の発想 (CSV/TSV の ASCII 制御文字活用) は
> Joel Parker Henderson 氏による [SixArm/usv](https://github.com/SixArm/usv)
> プロジェクト (2022 年〜) で既に提案・実装されています。本記事は車輪の
> 再発明ではなく、Joel 氏の expired IETF Draft の **revival 提案** と、
> 我々が追加した 3 つの拡張 (罫線連動 / width metadata / 2-pane viewer)
> の紹介です。

```

4. **タグ** に追加:
   - `USV`, `CSV`, `TSV`, `Unicode`, `ASCII`, `LLM`, `IETF`, `OSS`
5. **公開** ボタンをクリック

**完了条件**: Qiita 記事が公開され URL が取得できる

---

## Step 7 — LinkedIn 投稿 (日本語)

**操作**:
1. `https://www.linkedin.com/feed/` を開く (ログイン済前提)
2. 「投稿を作成」をクリック
3. 以下のテキストを貼り付け (約 850 字、絵文字 minimal):

```
60 年前に予約されていた ASCII 制御文字 U+001F と U+001E を活用して、
CSV/TSV の現代版を作る試み「USV (Unicode Separated Values)」を皆さんに
知ってほしい。

実は私のオリジナルではなく、Joel Parker Henderson 氏が 2022 年から
SixArm/usv で提案していたものです。2024 年に IETF Draft も提出された
のですが、その後失効し、約 1 年半停滞していました。

LLM/AI 時代の表データ通信 (Markdown 表が CJK で崩れる、CSV の escape
で破綻する) という新文脈で、USV の価値が再評価されるべきだと感じます。
そこで:

(1) 罫線連動セマンティクス (US = 縦罫線、RS = 横罫線)
(2) cell width 拡張 (UAX #11 East Asian Width 対応)
(3) Python Textual ベース 2 ペインビューワー

の 3 点を追加して、Joel 氏に IETF Draft 共著 or upstream PR を提案
しました。先人を尊重して revival する形での貢献です。

プロトタイプ + 仕様書 + 普及戦略文書をすべて Apache-2.0 で公開:
https://github.com/furuse-kazufumi/usrs

USV ジャンルを再点火させたい方は Issue / Discussion で議論しましょう。
特にエディタ / ターミナル開発者の方、`.usv` を syntax highlight 対応
するだけでも大きな前進です。

#USV #CSV #TSV #Unicode #ASCII #LLM #IETF #OSS
```

4. 「**投稿**」をクリック

**完了条件**: LinkedIn フィードに投稿が表示される

---

## Step 8 — Hacker News に Show HN 投稿 (英語)

**操作**:
1. `https://news.ycombinator.com/submit` を開く (HN にログイン済、未ログインなら https://news.ycombinator.com/login で furuse-kazufumi or 別アカウントでログイン)
2. **Title**:
   ```
   Show HN: Reviving USV (Unicode Separated Values) – ASCII U+001F for tables in the LLM era
   ```
3. **URL**: `https://github.com/furuse-kazufumi/usrs`
4. **Text** (URL を指定する場合は通常不要、ただし detail 追加したいなら):

```
Background: Joel Parker Henderson proposed USV (Unicode Separated Values)
in 2022 using the long-forgotten ASCII U+001F and U+001E information
separators. IETF Draft was submitted in 2024 but expired without further
progression.

This prototype revives the concept and adds three things:
1. Grid-line semantics (US = vertical rule, RS = horizontal rule)
2. Optional W<n>:cell width metadata (Unicode UAX #11 compliant)
3. A 2-pane Textual TUI viewer for Markdown / HTML cells

Especially relevant now that LLMs need a tabular format that survives
Markdown / HTML / CJK / multi-line content without escaping. Open issue
filed with the original author proposing either upstream PRs or fresh
IETF draft co-authorship.

Apache-2.0. Looking for feedback, especially from editor / terminal
developers interested in syntax highlight / preview support.

References:
- Original: https://github.com/SixArm/usv
- Expired IETF Draft: https://datatracker.ietf.org/doc/draft-unicode-separated-values/
- This prototype: https://github.com/furuse-kazufumi/usrs
```

5. **submit** をクリック
6. 投稿 URL を取得

**完了条件**: HN に投稿された URL が取得できる

---

## Step 9 — IETF Draft 提出 (Joel から反応なし or 共著合意後)

**前提条件**: Step 4 から 1-2 週間経過して以下のいずれか
- (a) Joel から反応がなく、独立提出 path に進む
- (b) Joel と共著合意済、author に 2 名分書く

**操作**:
1. `https://authors.ietf.org/getting-started` を開く
2. IETF Datatracker アカウントを作成 (Sign Up):
   - Name: `Kazufumi Furuse`
   - Email: `kazufumi@furuse.work`
3. アカウント confirmation メールを処理
4. `xml2rfc` ツールをローカルにインストール:
   ```bash
   pip install xml2rfc
   ```
5. `D:/projects/usrs/docs/CONTACT_PLAN.md` の §3.1 にある XML 骨子を
   ベースに `docs/ietf-draft/draft-furuse-usv-00.xml` を作成
6. `xml2rfc --v3 docs/ietf-draft/draft-furuse-usv-00.xml` で検証 (errors 0)
7. `https://datatracker.ietf.org/submit/` を開いてアップロード:
   - File: `draft-furuse-usv-00.xml`
   - Submitter: Kazufumi Furuse, kazufumi@furuse.work
8. プレビューで著者・タイトルが正しいか確認 → **Submit**
9. confirmation メールが届くので承認 link をクリック
10. 数時間後、`https://datatracker.ietf.org/doc/draft-furuse-usv/` が公開

**完了条件**: Datatracker に draft URL が永続表示される (= **世界の標準化記録に名前が残る**)

---

## Step 10 — フォローアップ / KPI 追跡

毎週 1 回、以下を確認:
1. SixArm/usv の Issue: Joel からの返信あり/なし
2. `furuse-kazufumi/usrs` の Star 数 / Issues / PR
3. Qiita 記事の LGTM 数 / コメント
4. LinkedIn 投稿の Like / Comment / Repost
5. HN 投稿のスコア / コメント数
6. IETF Datatracker (提出済なら) の引用数
7. Google 検索「Unicode Separated Values furuse」のヒット数 = **周知度**

異常があれば本 runbook の末尾に追記。

---

## 重要原則 (Comet/operator 共通)

1. **Joel への礼節を最優先**: 「先人」「revival」「foundational contribution」を一貫使用
2. **公開記録を活用**: GitHub Issue / IETF Datatracker / Qiita はすべて永続記録、これが「**周知の立場**」の本質
3. **個人攻撃禁止**: 既存 USV の「停滞」「expired」を批判的に書かない、事実中立
4. **車輪の再発明と書かない**: 「revival」「refresh」「additional contribution」と表現
5. **メールアドレス**: 一貫して `kazufumi@furuse.work` を使用

## エラー対処

| エラー | 対処 |
|---|---|
| GitHub push 認証失敗 | SSH key 設定確認、または HTTPS + PAT |
| Issue 投稿時にスパム判定 | Issue 本文を 100 字以内に短縮 → 後で edit で詳細追加 |
| メール bounce | Joel 個人サイト joelparkerhenderson.com のフォーム経由で代替 |
| IETF Draft xml2rfc エラー | エラー行を `D:/projects/usrs/docs/CONTACT_PLAN.md` §3.1 と照合 |
| Qiita タグ上限 (5 つまで) | 重要 5 つに絞る (USV, CSV, Unicode, LLM, IETF) |

## 全工程完了時の状態

- [x] GitHub `furuse-kazufumi/usrs` public 公開
- [x] SixArm/usv に Issue 投稿 (公開記録)
- [x] Joel 直接メール送信
- [x] Qiita / LinkedIn / HN に発表記事
- [x] (1-2 週後) IETF Draft 提出 → Datatracker 永続記録
- [x] 売名効果: Google で「USV furuse-kazufumi」が検索ヒット
