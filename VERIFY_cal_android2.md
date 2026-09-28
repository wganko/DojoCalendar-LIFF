# 検証報告: cal.html Android導線修正（再検証）

## 判定: GO

ローカル成果物（未配備）に対する判定。C1〜C12はすべてPASSであり、検出した不具合はない。

## 項目別

| 項目 | 判定 | 根拠（JSONの該当キーと値、または実行したコマンドと出力） |
|---|---|---|
| C1 | PASS | `cases` の `env: Android` 4件すべてで `buttons_in_order` は1番目「Googleカレンダーで開く」、2番目「.icsファイルを保存する」。`env: iPhone` 4件すべてで1番目「カレンダーに追加」（`href` は `webcal://...`）、2番目「.icsファイルを保存する」。 |
| C2 | PASS | Android 4件すべてで「Googleカレンダーで開く」の `download: false`、保存ボタンの `download: true`。iPhone 4件およびPC 4件の保存ボタンもすべて `download: true`。 |
| C3 | PASS | Android 4件の「Googleカレンダーで開く」は `https://wganko.github.io/DojoCalendar-LIFF/<組>.ics` を直接参照し、`calendar.google.com` を経由していない。`?g=i` は `i.ics`、`?g=ro` は `ro.ics`、`?g=xxx` とクエリなしは `i.ics`。 |
| C4 | PASS | 4環境すべての `heading` で、`?g=i`→「い組」、`?g=ro`→「ろ組」、`?g=xxx`→「い組」、クエリなし→「い組」。 |
| C5 | PASS | `cases` は16件で、全件の `pageerrors` が `[]`。 |
| C6 | PASS | `fallback.body_empty: false`。`fallback.buttons_in_order` に「.icsファイルを保存する」かつ `download: true` があり、`fallback.body_text` に「パソコンで登録する場合のURL」と `ro.ics` を含む。 |
| C7 | PASS | PC 4件（`?g=i` / `?g=ro` / `?g=xxx` / なし）の `has_pc_steps` がすべて `true`。 |
| C8 | PASS | LINE-Android 4件の `has_notice` がすべて `true`。iPhone、Android、PCの各4件はすべて `false`。 |
| C9 | PASS | 16件すべてで `external_script_tags: []` かつ `external_css_tags: []`。 |
| C10 | PASS | `rg -n 'calendar\.google\.com' cal.html` は該当なし。`python3 tools/ics_from_config.py --check` は「一致: .../i.ics」「一致: .../ro.ics」を出力し exit 0。`git diff --name-only ffbaeeb -- i.ics ro.ics` は出力なし（両ICSに差分なし）。 |
| C11 | PASS | Pythonで各ファイルをバイト読み取り。`android_ro.png`: 61,514 bytes、`iphone_ro.png`: 38,592 bytes、`fallback.png`: 40,208 bytes。全ファイルの先頭8 bytesは `89504e470d0a1a0a` で、実在する非0バイトPNG。 |
| C12 | PASS | `served_android.buttons_in_order` は修正前の「.icsファイルをダウンロード」と「Googleカレンダーに追加」を含み、後者の `href` は `https://calendar.google.com/...`。公開URLには修正がまだ反映されていない証跡であり、本報告の判定範囲をローカル成果物（未配備）に限定した。 |

## 検出した不具合（あれば、再現手順つきで）

なし。

## 判定できなかった項目と理由（配備後の実機確認が未実施であることを必ず含める）

- 配備後の公開URLに対する実機確認は未実施のため判定できない。`served_android` は配備前の公開URLをAndroid UAで確認した証跡であり、修正前の内容が返っている。本GO判定はローカル成果物（未配備）だけを対象とする。
