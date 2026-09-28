# tools

このリポジトリの配信用ファイルを再生成するための補助スクリプト集です。

## 正本について

カレンダー（ICS）の正本は次にあります。

- `Tools/Scripts/DojoCalendar/src/config.js`
  （絶対パス: `/home/shi/workspace/Tools/Scripts/DojoCalendar/src/config.js`）

このリポジトリ（DojoCalendar-LIFF）には正本の複製を持ちません。
`i.ics` / `ro.ics` は正本から生成した配信用の成果物です。

## ICS の再生成

```bash
python3 tools/ics_from_config.py
```

- 正本 `config.js` の `ICS_I` / `ICS_RO` を取り出し、リポジトリ直下の `i.ics` / `ro.ics` を上書き生成します。
- 取り出した中身の `\n`（バックスラッシュ + n の2文字）はそのまま保持します（表示側で改行に復号するため）。
- 改行コードは LF、ファイル末尾は改行1つです。

一致確認（書き込みなし）:

```bash
python3 tools/ics_from_config.py --check
```

- 一致すれば終了コード 0、不一致またはファイルが無ければ終了コード 1（理由を標準エラーに日本語で出力）。
- 正本が無い・定数が見つからない場合は終了コード 2。

## QR 画像の再生成

依存のインストール:

```bash
pip install "qrcode[pil]"
```

生成:

```bash
python3 tools/make_qr.py
```

- リポジトリ直下に `qr_i.png` / `qr_ro.png` を生成します。
- 内容はそれぞれ `cal.html?g=i` / `cal.html?g=ro` を指すQRコードです。

## 公開について

GitHub Pages はこのリポジトリの `main` ブランチ直下がそのまま公開されます。
反映するには変更を commit + push してください。

## 公開URL一覧

- い組 ICS: https://wganko.github.io/DojoCalendar-LIFF/i.ics
- ろ組 ICS: https://wganko.github.io/DojoCalendar-LIFF/ro.ics
- い組 登録ページ: https://wganko.github.io/DojoCalendar-LIFF/cal.html?g=i
- ろ組 登録ページ: https://wganko.github.io/DojoCalendar-LIFF/cal.html?g=ro
