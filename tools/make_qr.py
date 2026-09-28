#!/usr/bin/env python3
"""QRコード画像（qr_i.png / qr_ro.png）を生成するスクリプト。

依存ライブラリのインストール方法:
    pip install "qrcode[pil]"

（Pillow が必要です。インストールできない場合は
 管理者に確認するか、仮想環境 (venv) 内で実行してください。）
"""

import sys
from pathlib import Path

# 出力先（このスクリプトの親ディレクトリ = リポジトリ直下）
REPO_ROOT = Path(__file__).resolve().parent.parent

# 生成対象 {出力ファイル名: カレンダー登録URL}
TARGETS = {
    "qr_i.png": "https://wganko.github.io/DojoCalendar-LIFF/cal.html?g=i",
    "qr_ro.png": "https://wganko.github.io/DojoCalendar-LIFF/cal.html?g=ro",
}


def make_qr(url: str, dest: Path) -> None:
    """1つのURLからQR画像を生成して保存する。"""
    import qrcode

    # box_size=14, border=4 で 574px 程度（512px 以上）になるようにする
    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=14,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(dest)
    print("生成しました: %s" % dest)


def main() -> int:
    try:
        for filename, url in TARGETS.items():
            make_qr(url, REPO_ROOT / filename)
    except ImportError:
        sys.stderr.write(
            "エラー: qrcode ライブラリが見つかりません。\n"
            "pip install \"qrcode[pil]\" を実行してください。\n"
        )
        return 1
    except Exception as exc:
        sys.stderr.write(
            "エラー: QR画像の生成に失敗しました: %s\n"
            "pip install \"qrcode[pil]\" を実行してください。\n" % exc
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
