"""サンプルコマンド

このファイルは quick_cmd のコマンド作成例です。
"""

from datetime import datetime


def run() -> None:
    """コマンドのメイン処理"""
    print("これはサンプルコマンドです。")
    print(f"現在時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    print("新しいコマンドを追加するには:")
    print("  1. src/quick_cmd/commands/ に .py ファイルを作成")
    print("  2. モジュールのdocstringに説明を記述")
    print("  3. run() 関数を実装")
