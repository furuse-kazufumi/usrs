# Contributing to USRS / USV

USRS の発展に関心を持っていただきありがとうございます。本書は本リポジトリ
への貢献方法と、USV 形式を各種エコシステム (エディタ・ターミナル・
ライブラリ) に広げる際のガイドです。

## 1. 貢献の種類

| 種類 | 何が欲しいか |
|---|---|
| **Spec 改善** | SPEC.md への明確化 / 補強 / 矛盾検出 |
| **参考実装** | Rust / TypeScript / Go / Java 等の参考実装 (Python を雛形に) |
| **エディタ統合** | VS Code / Neovim / Helix / Zed / JetBrains etc. の `.usv` サポート |
| **テスト** | 既存実装に追加するエッジケース、CJK / 絵文字 / 多言語サンプル |
| **ドキュメント** | チュートリアル、サンプル、翻訳 (ja/en/zh/ko) |
| **普及活動** | Qiita / dev.to / LinkedIn の記事、コミュニティ言及 |

## 2. 開発フロー

1. **Issue を立てる**: PR の前に Issue で目的を共有 (5 行程度で OK)
2. **fork & branch**: トピックブランチで作業 (例: `feat/rust-impl`,
   `docs/spec-clarify-cells`)
3. **Python 参考実装の場合**: `tests/` にテストを 1 件以上追加
4. **テスト走行**: `PYTHONIOENCODING=utf-8 py -3.11 -m pytest tests/ -q`
5. **PR**: タイトルは `<type>: <一行説明>` (type: feat/fix/docs/test/chore)
6. **Review**: 48 時間以内に first response

## 3. SPEC 変更の特別ルール

`SPEC.md` (規範文書) への変更は **breaking change リスクが高い**。以下を
踏襲:

- **Discussion で 1 週間以上意見募集** してから PR
- **後方互換性を必ず議論** (decoder が古い USV を読めなくなる変更は禁止)
- **rationale を必ず書く** (なぜこの変更が必要か、PR description に)
- **テストを更新** (新規ルールに対する正例 + 違反例)

## 4. テスト・スタイル

- Python は **stdlib のみ** で動くこと (`tabulate` 等の外部依存は参考実装に
  入れない)
- 型ヒント (Python 3.11+) は推奨
- セパレータ文字 (U+001F/U+001E) はテスト内で **直接コードポイントを書く**
  か `\x1f` / `\x1e` を使う
- 関数 / クラスに 1 行 docstring を推奨、長文 docstring は規範部分のみ

## 5. コミュニティ規約

[Contributor Covenant 2.1](https://www.contributor-covenant.org/version/2/1/code_of_conduct/) を採用。

## 6. ライセンス

- 本リポジトリへの貢献は **Apache-2.0** に同意したものとみなします
- DCO (Developer Certificate of Origin) は不要 (Apache-2.0 内に含まれる)
- 商用 dual-license の権利を作者は留保

## 7. 普及活動への貢献

USRS の普及は **エディタ・ターミナル・ライブラリ各 repo への提案** で
最大化される。詳細は [PROMOTION.md](PROMOTION.md) を参照。**Linguist
PR** が最初の鍵 (これが通れば GitHub 上で `.usv` が言語として認識される)。

特に歓迎する貢献:
- `github-linguist/linguist` への `.usv` 言語登録 PR
- Tree-sitter grammar (`tree-sitter-usv`)
- VS Code extension (`vscode-usv` を marketplace へ)
- `highlight.js` / `Pygments` への USV lexer
- ターミナル renderer (`bat` / `eza` / `delta` で `.usv` をハイライト)

## 8. 質問

- 仕様: GitHub Issues / Discussions
- 商用ライセンス: 作者へ直接コンタクト

ようこそ USRS コミュニティへ。
