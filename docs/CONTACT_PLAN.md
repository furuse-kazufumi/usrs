# SixArm USV への接触プラン + IETF Draft 復活手順

> 既存先駆者 SixArm/usv (Joel Parker Henderson、2022 年〜停滞) に対し、共著者・
> 復活提案者ポジションを取るための **実行可能な文書一式**。
>
> このディレクトリ内のテンプレを順にコピペすれば、1 日で全工程に着手できる。

## 全体タイムライン

```
Day 0  : GitHub Issue を立てる (公開記録開始)
Day 0  : Joel に直接メール (Issue リンク付き)
Day 7  : 反応待ち期間 (1 週間)
Day 7+ : 反応あり → 共著 IETF Draft v02 を共同作成
         反応なし → 我々が単独で revival Draft を提出
Day 14 : IETF Draft 提出 (Datatracker に永続記録)
Day 14 : Qiita / LinkedIn / HN で「USV 復活」を発表
Day 30 : KPI 確認 (GitHub Star / Draft 引用 / メディア言及)
```

## 1. SixArm/usv GitHub Issue 文案 (公開記録の起点)

**投稿先**: https://github.com/SixArm/usv/issues/new

**タイトル**:
```
Reviving USV — proposal to refresh the spec and resubmit a fresh IETF Draft v02
```

**本文** (英語、そのままコピペ):

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
review work; I just want to make sure your original vision is
honored and that the credit reflects your foundational contribution.

About me:
- Japanese OSS developer, individual contributor
- Building the FullSense umbrella OSS (llive / llove / llmesh) in my spare time
- Prototype repo: <will-share-after-issue-acknowledged>

Thanks for the foundational work on USV. Looking forward to your thoughts.

Best regards,
furuse-kazufumi
```

> ⚠️ 投稿前のチェック:
> - GitHub アカウントが活動的 (アバター・bio・他リポジトリあり)
> - プロトタイプ repo を **そのとき同時に公開** すると説得力大
> - 「Issue → 即 PR」より「**Issue → 反応 → PR**」の方が礼節

## 2. Joel への直接メール文案 (フォローアップ)

**宛先**: `joel@joelparkerhenderson.com`
**件名**: `Reviving USV — proposal via GitHub Issue #<番号>`

**本文 (英語)**:

```text
Hi Joel,

I just opened an issue on github.com/SixArm/usv:

  <Issue URL>

It's a proposal to help revive the USV work — the IETF draft expired
in 2024 and I'd like to either contribute as upstream PRs or co-author
a fresh draft-02 with you. Three concrete additions are described in
the issue (grid-line semantics, optional width metadata, a 2-pane
viewer).

I emailed instead of waiting purely on GitHub notifications since the
draft datatracker noted your email might be stale; if this address is
also out of date please let me know how best to reach you.

Best regards,
furuse-kazufumi
GitHub: @furuse-kazufumi
```

> メールは Issue の **複製ではなく単なる注意喚起**。本文は短く、議論本体は
> GitHub Issue 側に集約する (公開記録性の維持)。

## 3. 反応がなかった場合の独立提出文書

### 3.1 IETF Draft v02 (revival) — XML/RFC v3 形式の骨子

ファイル名: `docs/ietf-draft/draft-furuse-usv-00.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE rfc SYSTEM "rfc2629-xhtml.ent">
<rfc xmlns:xi="http://www.w3.org/2001/XInclude"
     ipr="trust200902"
     docName="draft-furuse-usv-00"
     submissionType="independent"
     category="info"
     version="3">

  <front>
    <title abbrev="USV">
      Unicode Separated Values (USV) — revival and refinement
    </title>
    <author fullname="Kazufumi Furuse" initials="K." surname="Furuse">
      <organization>Independent</organization>
      <address>
        <email>kazufumi@furuse.work</email>
      </address>
    </author>
    <date year="2026"/>
    <area>Applications and Real-Time</area>
    <keyword>USV</keyword>
    <keyword>tabular data</keyword>
    <keyword>CSV alternative</keyword>
    <keyword>Unicode</keyword>
    <abstract>
      <t>
        Unicode Separated Values (USV) is a plain-text tabular data
        format that reuses the ASCII Information Separators (U+001F and
        U+001E), originally specified in ANSI X3.4-1967, as cell and
        record delimiters. This document refreshes Joel Parker
        Henderson's expired draft-unicode-separated-values-01 (2024)
        with the following additions:
      </t>
      <t>
        (1) explicit grid-line semantics tying separators to rendering;
        (2) an optional cell width metadata prefix compatible with
        Unicode UAX #11; and (3) a clarified rule that any character
        other than U+001F and U+001E is valid cell content, including
        Markdown, HTML, LaTeX, multi-line text, and tab indentation.
      </t>
    </abstract>
  </front>

  <middle>
    <!-- 1. Introduction -->
    <!-- 2. Conventions and definitions -->
    <!-- 3. Format syntax (US/RS) -->
    <!-- 4. Cell content universality -->
    <!-- 5. Optional width metadata -->
    <!-- 6. Grid-line rendering semantics -->
    <!-- 7. Interoperability with CSV / TSV / Markdown -->
    <!-- 8. Security considerations -->
    <!-- 9. IANA considerations (media type text/usv) -->
    <!-- 10. Acknowledgements (Joel Parker Henderson の貢献を明示) -->
  </middle>
</rfc>
```

> **重要**: Acknowledgements 節で **Joel Parker Henderson** の名前と
> 元 draft への引用を明示。これがないと「先人の貢献を奪った」と
> コミュニティから批判される。礼節最重要。

### 3.2 IETF I-D Submission 手順

1. https://authors.ietf.org/getting-started でアカウント作成
2. `xml2rfc draft-furuse-usv-00.xml` でローカル検証
3. https://datatracker.ietf.org/submit/ にアップロード
4. メタデータを確認 → submit
5. 約数時間で `https://datatracker.ietf.org/doc/draft-furuse-usv/` が
   公開される (= **世界の Datatracker に永続記録**)

## 4. プロトタイプ repo の公開準備チェックリスト

GitHub Issue / メールに repo リンクを貼る前に整える:

- [x] README.md (Quick Start 5 分以内)
- [x] SPEC.md (規範文書)
- [x] PROMOTION.md (普及戦略)
- [x] CONTRIBUTING.md (貢献ガイド)
- [x] LICENSE (Apache-2.0)
- [x] docs/RELATED_WORK.md (SixArm USV を主要先行例として明記)
- [x] docs/SHOWCASE.md (2 ペインビューワー UI 設計)
- [x] docs/CONTACT_PLAN.md (本ファイル)
- [x] src/usrs.py (Python 参考実装)
- [x] src/usrs_viewer.py (Textual 2 ペインビューワー)
- [x] tests/test_usrs.py (31 件、全 PASS)
- [x] examples/sales.usv (サンプル)
- [ ] GitHub Repo を `furuse-kazufumi/usrs` で **public 公開**
- [ ] README に「SixArm/usv とは何が同じで何が違うか」短いセクション追加
- [ ] About / Topics / Discussions 設定

## 5. メディア展開タイムライン

GitHub Issue を立てた **後** に投稿することが重要 (順序: 当事者通知 → 公開発表)。

| Day | チャネル | 内容 |
|---|---|---|
| Day 0 | SixArm/usv Issue | revival 提案を投稿 (公開記録の起点) |
| Day 0 | Joel に直接メール | 上記 Issue の link |
| Day 0 | GitHub: furuse-kazufumi/usrs を public 化 | プロトタイプ公開 |
| Day 7 | Qiita | 「USV を復活させる試み」記事 (Joel への敬意を明記) |
| Day 7 | LinkedIn jp | 同じ趣旨を 850 字で |
| Day 14 | IETF Draft 提出 | revival draft (Joel と共著、または独立) |
| Day 14 | Hacker News (Show HN) | 英語 + Datatracker link |
| Day 14 | dev.to (en) | 詳細記事 (LLM 角度) |
| Day 21 | r/programming / r/LocalLLaMA | Discussion 開始 |
| Day 30 | 経過レポート | KPI 確認 + 次戦略 |

## 6. KPI (1 ヶ月後のチェック)

- [ ] SixArm/usv Issue: Joel から返信あり / なし
- [ ] GitHub: `furuse-kazufumi/usrs` Star 数 100+
- [ ] IETF Draft 提出済 (Datatracker URL 取得)
- [ ] Qiita / LinkedIn / HN 言及数
- [ ] エディタコミュニティ (Linguist / VS Code 等) からの反応
- [ ] Anthropic / OpenAI / Microsoft からの言及 (LLM 角度で)
- [ ] 「Unicode Separated Values」Google 検索結果トップ 20 に
      furuse-kazufumi の名前が出る = **周知の立場達成**

## 7. 礼節の原則 (重要)

| Do | Don't |
|---|---|
| Joel への敬意を一貫して表現 | 「自分が発明者」と主張しない |
| Acknowledgements 節を厚く書く | Joel の名前を消す / 弱める |
| 共著の選択肢を最初に提示 | いきなり独立提出 |
| 「revival」「refinement」と表現 | 「再発明」「改善」と表現 |
| 過去 draft を必ず引用 | 既存仕様を意識的に避けて書く |

「**先人を尊重しつつ、現代の角度 (LLM/AI 時代の表データ需要) を持ち込んで再活性化する**」というポジションが、最も売名効果と倫理性の両立になります。

## 8. このファイル自体の運用

- Issue / メール送信時にこのファイルを **削除しない** (記録として残す)
- 反応があったら本ファイルに追記 (反応日時 / 内容 / 次アクション)
- IETF Draft 提出後は `docs/ietf-draft/` 配下に正式版を保管
