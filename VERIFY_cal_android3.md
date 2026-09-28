# 検証報告: cal.html Android導線（ダウンロードリンク方式）

## 判定: GO

## 項目別

| 項目 | 判定 | 根拠（JSONの該当キーと値、または実行したコマンドと出力） |
|---|---|---|
| D1 Androidの導線 | PASS | `cases` の `env: "Android"` 4件すべてで `buttons_in_order` は1件のみ。全件の `text` は `.icsファイルをダウンロード`、`download` は `true`。`?g=i` は `href: https://wganko.github.io/DojoCalendar-LIFF/i.ics`、`?g=ro` は `.../ro.ics`、`?g=xxx` とクエリなしは `.../i.ics`。 |
| D2 旧Google Calendar導線なし | PASS | `rg -n "calendar\\.google\\.com" cal.html` の出力は空（該当なし）。 |
| D3 iPhone非退行 | PASS | `env: "iPhone"` 4件すべてで `buttons_in_order` は、1番目が `text: カレンダーに追加`、対応する `webcal://wganko.github.io/DojoCalendar-LIFF/<組>.ics`、`download: false`。2番目が `text: .icsファイルをダウンロード`、対応するHTTPS URL、`download: true`。 |
| D4 PC非退行 | PASS | `env: "PC"` 4件すべてで `has_pc_steps: true`。各件の保存ボタンは `text: .icsファイルをダウンロード`、`download: true`。 |
| D5 JS例外ゼロ | PASS | `cases` 全16件で `pageerrors: []`。 |
| D6 フォールバック | PASS | `fallback.body_empty: false`。`fallback.buttons_in_order` に `text: .icsファイルをダウンロード`、`download: true` のボタンあり（`href: .../ro.ics`）。 |
| D7 LINE注意書き | PASS | `env: "LINE-Android"` 4件はすべて `has_notice: true`。iPhone・Android・PCの計12件はすべて `has_notice: false`。 |
| D8 外部リソースなし | PASS | `cases` 全16件で `external_script_tags: []` かつ `external_css_tags: []`。 |
| D9 組判定 | PASS | 4環境すべてで `heading` は `?g=i` が `尺八道場（い組） カレンダー登録`、`?g=ro` が `尺八道場（ろ組） カレンダー登録`、`?g=xxx` とクエリなしが `尺八道場（い組） カレンダー登録`。 |
| D10 ICS健全性・無変更 | PASS | `python3 tools/ics_from_config.py --check` は `一致: .../i.ics`、`一致: .../ro.ics` を出力し exit 0。`git diff --name-only ffbaeeb -- i.ics ro.ics` の出力は空。 |
| D11 証跡の実在性 | PASS | Pythonで先頭8バイトを読み取り確認。`android_ro.png`: 52,913 bytes、`iphone_ro.png`: 38,327 bytes、`fallback.png`: 39,949 bytes。すべて先頭8バイトは `89504e470d0a1a0a` で、非0バイト。 |
| D12 判定範囲 | PASS | `served_android.buttons_in_order` は旧内容（`Googleカレンダーで開く`, `download: false` と `.icsファイルを保存する`, `download: true`）を返しており、公開URLは未配備。本判定はローカル成果物（未配備）に対する判定であることを確認。Android実機での再確認は未実施。 |

## 検出した不具合（あれば、再現手順つきで）

なし。

## 判定できなかった項目と理由（Android実機での再確認が未実施であることを必ず含める）

- Android実機で、ダウンロードした `.ics` をタップした際にカレンダー追加画面が開くことの再確認は未実施。今回提供された証跡はホスト側Chromiumによるローカル成果物のDOM確認であり、`served_android` の公開URLは修正前の内容を返しているため、配備後のAndroid実機挙動は判定できない。
- したがって、このGO判定の範囲はローカル成果物（未配備）のみであり、公開環境およびAndroid実機での動作を含まない。
