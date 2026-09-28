# 検証報告: DojoCalendar カレンダー購読アセット

## 判定: GO

## 項目別

| 項目 | 判定 | 実際に実行したコマンドと出力（抜粋） |
|---|---|---|
| V1 | PASS | `python3` で両ファイルをバイト列・UTF-8・行・プロパティ単位に検査。`i.ics: bytes=4175, CR=0, LF=88, ends_LF=True, structural_valid=True, VEVENT=8, bad_property_lines=[]`、`ro.ics: bytes=4134, CR=0, LF=88, ends_LF=True, structural_valid=True, VEVENT=8, bad_property_lines=[]`。DESCRIPTION は各8行で、物理行内のリテラル `\n`（バックスラッシュ＋n）は `i.ics=17`、`ro.ics=16`。例: Python `repr` は `'DESCRIPTION:対象：い組\\n内容：...\\n備考：...'`。DESCRIPTION中で実改行へ化けていないことも assert で確認。 |
| V2 | PASS | `python3 tools/ics_from_config.py --check` → `一致: .../i.ics`、`一致: .../ro.ics`。さらにスクリプトの抽出関数は使わず、別の Python 正規表現で `/home/shi/workspace/Tools/Scripts/DojoCalendar/src/config.js` のバッククォート間を抽出・LF正規化して比較。`ICS_I i.ics equal=True`、双方 SHA-256 `d082bfdeb69541b0b7087436f0b380bd2177f7bdd6afb1f70f88dff0ec4d3ef1`、リテラル `\n` は双方17個。`ICS_RO ro.ics equal=True`、双方 SHA-256 `f1a7099bfca45311cdb4e5d597af6480eb3c9e17600cb0c3e6f6b5af9ba6bc3e`、リテラル `\n` は双方16個。 |
| V3 | PASS | `cal.html` 内の JavaScript を Node `vm` で構文解析・実行し、簡易DOMへ実際に描画。iPhone / Android / PC / ` Line/14.0.0` 付きiPhone の各UA × `?g=i` / `?g=ro` / `?g=xxx` / パラメータなし（16通り）を実行。組は順に i / ro / i / i、リンク種別は iPhone=`webcal:`、Android=`calendar.google.com/...cid=webcal://...`、PC=「パソコンから登録する場合」、LINE UAのみ `LINE_notice=true`。全ケースで対応する `i.ics` / `ro.ics` URLを確認。`navigator.userAgent` getterを意図的に例外化した試験は `forced exception fallback warn=true blank=false` で、ろ組URLとダウンロードリンクが残った。`new vm.Script(src)` → `JavaScript syntax: OK`。 |
| V4 | PASS | OpenCV未導入のため、PNGを直接展開し、画素から33×33 QRモジュールを読み、マスク解除・コードワード逆インターリーブ・byte-mode復号を行う独立 Python デコーダを `/tmp` にもファイルを作らず実行。`qr_i.png (mask=2, 'https://wganko.github.io/DojoCalendar-LIFF/cal.html?g=i', codewords=100, modules=33, 574x574)`、`qr_ro.png (mask=2, 'https://wganko.github.io/DojoCalendar-LIFF/cal.html?g=ro', codewords=100, modules=33, 574x574)`。 |
| V5 | PASS | `git diff --exit-code -- absence.html register.html broadcast.html README.md` → exit 0。`git diff --name-only` と `git diff --cached --name-only` はともに空。`git status --short` は対象新規ファイル等が `??` のみで、既存4ファイルの変更表示なし。検証中に git の commit / push / add / stash / checkout は未実施。 |

## 検出した不具合（あれば、再現手順つきで）

なし。

## 判定できなかった項目と理由

なし。
