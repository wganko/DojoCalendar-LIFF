# 判定: GO

検証対象は `cal.html`、実測証跡は `uat_evidence/autodl_results.json`、各 DOM スナップショットおよびスクリーンショット。ブラウザ・サーバーは起動していない。

| AC | 判定 | 根拠の実測値 |
|---|---|---|
| AC-1 | PASS | `env=android`, `mode=after`: `download_count=1`, `downloads=["i.ics"]`。 |
| AC-2 | PASS | `env=android`, `mode=after`: `has_manual_btn=true`。`autodl_after_android.html` の実 DOM は `<a class="btn" href="https://wganko.github.io/DojoCalendar-LIFF/i.ics" download="">.icsファイルをダウンロード</a>` で、クリック可能な `.ics` 直リンクかつ `download` 属性付き。ソースでは Android 分岐内の `cal.html:240` から `renderDownloadButton(card, icsUrl)` を呼び、同関数は `href: icsUrl` と `download` 属性を設定している（`cal.html:185-194`）。 |
| AC-3 | PASS | `env=android`, `mode=after`: `has_kalender_select_text=true`。`autodl_after_android.html` の実文は「ダウンロードしたファイルをタップし、『カレンダー』（または『Googleカレンダー』）を選んでください。」。 |
| AC-4 | PASS | `env=android_line`, `mode=after`: UA に `Line/14.5.0/IAB` を含み、`download_count=0`, `downloads=[]`。ソースでは自動DL呼出が Android 分岐内の `if (!isLine)` 内に限定されている（`cal.html:247-250`）。`autodl_after_android_line.png` はLINE内ブラウザの注意表示、手動ボタン、説明文を表示しており、0件という実測と矛盾しない。 |
| AC-5 | PASS | `env=iphone`: `card_html_sha` は before/after とも `e23f6e150b27b0f3ac270d0c5388a620060a662ba5cedefda3a1cc6579ea4324`、長さもともに `367`。after の `has_webcal=true`。 |
| AC-6 | PASS | `env=pc`: `card_html_sha` は before/after とも `f009226b1c8b166015e47270f689a22b0d271326f279bff9c7748547d440869f`、長さもともに `394`。 |
| AC-7 | PASS | after 4環境すべてで `pageerrors=[]`（android / android_line / iphone / pc、各0件）。 |

## 追加確認

- `window.location` によるダウンロード遷移はない。自動DLは一時的な `<a href=icsUrl download>` を `document.body` に追加し、`click()` 後に削除する実装（`cal.html:198-206`）。
- 自動DL全体は `try/catch` で保護されている（`cal.html:199-209`）。加えて、実測でも全4環境の `pageerrors` は0件。
- `git diff --unified=0 -- cal.html` で列挙された変更は次の4点のみ。
  1. `autoDownload` 関数の15行追加。
  2. Android説明文1行の変更。
  3. Androidヒント文1行の変更。
  4. Android分岐内への `if (!isLine) { autoDownload(icsUrl); }` の5行追加。
- 差分には iOS の `webcal://` 行、PC手順の「他のカレンダー」「URL で追加」、PCのダウンロードボタン生成行・ラベルは含まれない。iPhone/PCの before/after DOMハッシュ一致とも整合する。

以上より、AC-1〜AC-7はすべてPASS。実バグまたは受入条件未達は検出されなかった。
