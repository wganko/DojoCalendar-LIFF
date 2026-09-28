# 検証報告: cal.html Android導線修正

## 判定: NO-GO

ヘッドレスChromiumが実行環境の制限で起動できず、必須のDOM実測を完了できなかったため。検出した実バグはないが、推測でPASSとはしない。

## 項目別

| 項目 | 判定 | 実際に実行したコマンドと出力（抜粋） |
|---|---|---|
| V1 | 判定できない | `node /tmp/verify_cal_android.js` → Chromium 1243: `setsockopt: Operation not permitted (1)`、`signal=SIGTRAP`。headless shellでも `sandbox_host_linux.cc:41 ... shutdown: Operation not permitted (1)`、`signal=SIGTRAP`。よって4 UA × 2クエリのDOM順とpageerror件数を実測できず。 |
| V2 | PASS | `rg -n 'calendar\.google\.com' cal.html` → 出力なし、exit 1（該当なし）。 |
| V3 | 判定できない | 差分上はAndroid主ボタンが `href: icsUrl` で、`download` を設定する処理はないことを確認。ただしChromium DOMでの必須実測ができないためPASSとはしない。 |
| V4 | 判定できない | 差分上は副ボタン生成関数に `link.setAttribute('download', '')` があることを確認。ただしChromium DOMでの必須実測ができないためPASSとはしない。 |
| V5 | 判定できない | `?g=i` / `?g=ro` / `?g=xxx` / パラメータなしを測るPlaywrightテストを実行したが、ブラウザ起動前に上記制限で終了。組表示とpageerror 0件を実測できず。 |
| V6 | 判定できない | `Navigator.prototype.userAgent` のgetterを例外化する `page.addInitScript` を含むPlaywrightテストを実行したが、ブラウザ起動前に終了。フォールバックDOMを実測できず。 |
| V7 | PASS | `rg -n '<script[^>]+src[[:space:]]*=' cal.html` → 出力なし、exit 1。`rg -n "BASE\|i\.ics\|ro\.ics\|webcal://wganko\.github\.io/DojoCalendar-LIFF/" cal.html` → `BASE = 'https://wganko.github.io/DojoCalendar-LIFF/'`、`ro.ics`、`i.ics`、正しいwebcal基底を確認。`git diff --unified=25 ffbaeeb -- cal.html` で `resolveGroup()` に変更がないことを確認。`python3 tools/ics_from_config.py --check` → `一致: .../i.ics`、`一致: .../ro.ics`、exit 0。 |

### V1: 4 UA × 2クエリのDOM実測結果

| User-Agent | クエリ | DOM上のボタン順 | 補助表示 | pageerror |
|---|---|---|---|---|
| iPhone | `?g=i` | 判定できない | 判定できない | 判定できない |
| iPhone | `?g=ro` | 判定できない | 判定できない | 判定できない |
| Android | `?g=i` | 判定できない | 判定できない | 判定できない |
| Android | `?g=ro` | 判定できない | 判定できない | 判定できない |
| PC | `?g=i` | 判定できない | 判定できない | 判定できない |
| PC | `?g=ro` | 判定できない | 判定できない | 判定できない |
| LINE内（Android + ` Line/14.15.0`） | `?g=i` | 判定できない | 判定できない | 判定できない |
| LINE内（Android + ` Line/14.15.0`） | `?g=ro` | 判定できない | 判定できない | 判定できない |

## 検出した不具合（あれば、再現手順つきで）

なし。なお、DOM実測未完了のため「不具合なし」を保証する判定ではない。

## 判定できなかった項目と理由

V1、V3、V4、V5、V6。Playwright自体とChromiumバイナリは既存環境に存在したため実行したが、通常ChromiumはCrashpadのsocket操作が拒否されてSIGTRAPとなり、headless shellもsandbox hostのshutdown操作が拒否されてSIGTRAPとなった。いずれもページを開く前に終了したため、DOM、ボタン属性、組表示、pageerror、例外時フォールバックを実測できなかった。
