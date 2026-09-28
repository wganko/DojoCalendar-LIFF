#!/usr/bin/env python3
"""config.js から ICS 定数を取り出して i.ics / ro.ics を生成するスクリプト。

正本の場所: /home/shi/workspace/Tools/Scripts/DojoCalendar/src/config.js
このリポジトリには正本の複製を持たない。
"""

import re
import sys
from pathlib import Path

# 正本 config.js の絶対パス
CONFIG_PATH = Path("/home/shi/workspace/Tools/Scripts/DojoCalendar/src/config.js")

# 出力先（このスクリプトの親ディレクトリ = リポジトリ直下）
REPO_ROOT = Path(__file__).resolve().parent.parent


def extract_constant(source: str, name: str) -> str:
    """テンプレートリテラル定数 `name` の中身を返す。

    `const NAME = ` ... `;` の最初と最後のバッククォートの間を取り出す。
    取り出した中身の `\\n`（バックスラッシュ+n の2文字）はそのまま保持する。
    JS テンプレートリテラルの物理改行は実改行としてそのまま出力する。
    """
    # 定数の開始位置（const NAME = の直後のバッククォート）を探す
    start_pattern = re.compile(
        r"const\s+" + re.escape(name) + r"\s*=\s*`"
    )
    start_match = start_pattern.search(source)
    if start_match is None:
        raise LookupError("定数 %s が見つかりませんでした。" % name)

    body_start = start_match.end()
    # 対になる最後のバッククォートを探す
    end_index = source.find("`", body_start)
    if end_index == -1:
        raise LookupError("定数 %s の終端（バッククォート）が見つかりませんでした。" % name)

    return source[body_start:end_index]


def normalize(text: str) -> str:
    """改行コードを LF に統一し、末尾に改行を1つだけ付ける。"""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    return text.rstrip("\n") + "\n"


def build_outputs() -> dict:
    """生成対象 {ファイル名: 内容} を返す。"""
    if not CONFIG_PATH.is_file():
        raise FileNotFoundError(
            "正本の config.js が見つかりません: %s" % CONFIG_PATH
        )

    source = CONFIG_PATH.read_text(encoding="utf-8")

    return {
        "i.ics": normalize(extract_constant(source, "ICS_I")),
        "ro.ics": normalize(extract_constant(source, "ICS_RO")),
    }


def write_outputs(outputs: dict) -> None:
    """生成結果をリポジトリ直下へ上書き保存する。"""
    for filename, content in outputs.items():
        target = REPO_ROOT / filename
        target.write_text(content, encoding="utf-8", newline="\n")
        print("書き出しました: %s" % target)


def check_outputs(outputs: dict) -> bool:
    """既存ファイルと生成結果を比較する。一致しなければ理由を出力する。"""
    ok = True
    for filename, content in outputs.items():
        target = REPO_ROOT / filename
        if not target.is_file():
            sys.stderr.write("不一致: %s が存在しません。\n" % target)
            ok = False
            continue
        existing = target.read_text(encoding="utf-8")
        if existing != content:
            sys.stderr.write(
                "不一致: %s が生成結果と異なります。\n" % target
            )
            ok = False
        else:
            print("一致: %s" % target)
    return ok


def main(argv) -> int:
    check = "--check" in argv[1:]

    try:
        outputs = build_outputs()
    except (FileNotFoundError, LookupError) as exc:
        sys.stderr.write("エラー: %s\n" % exc)
        return 2
    except Exception as exc:  # 想定外の失敗も日本語で案内する
        sys.stderr.write("エラー: 予期しない失敗が発生しました: %s\n" % exc)
        return 2

    if check:
        return 0 if check_outputs(outputs) else 1

    try:
        write_outputs(outputs)
    except Exception as exc:
        sys.stderr.write("エラー: ファイルの書き出しに失敗しました: %s\n" % exc)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
