"""CLI処理モジュール"""

import importlib
import sys
from pathlib import Path
from typing import Optional

import questionary


def get_commands_dir() -> Path:
    """
    コマンドディレクトリのパスを取得

    Returns:
        コマンドディレクトリのPath
    """
    return Path(__file__).parent / "commands"


def discover_commands() -> list[str]:
    """
    commandsディレクトリ内のコマンドを検出

    Returns:
        コマンド名のリスト（.pyファイル名から拡張子を除いたもの）
    """
    commands_dir = get_commands_dir()

    if not commands_dir.exists():
        return []

    commands = []
    for file_path in commands_dir.glob("*.py"):
        if file_path.name.startswith("_"):
            continue
        command_name = file_path.stem
        commands.append(command_name)

    return sorted(commands)


def get_command_description(command_name: str) -> Optional[str]:
    """
    コマンドの説明を取得

    Args:
        command_name: コマンド名

    Returns:
        コマンドの説明文（__doc__から取得）
    """
    try:
        module = importlib.import_module(f"quick_cmd.commands.{command_name}")
        return module.__doc__
    except ImportError:
        return None


def execute_command(command_name: str) -> None:
    """
    指定されたコマンドを実行

    Args:
        command_name: 実行するコマンド名
    """
    try:
        module = importlib.import_module(f"quick_cmd.commands.{command_name}")

        if hasattr(module, "run"):
            module.run()
        else:
            print(f"エラー: コマンド '{command_name}' には run() 関数がありません。")
            sys.exit(1)

    except ImportError as e:
        print(f"エラー: コマンド '{command_name}' の読み込みに失敗しました: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"エラー: コマンド '{command_name}' の実行中にエラーが発生しました: {e}")
        sys.exit(1)


def get_user_choice(prompt: str, choices: list[str]) -> str:
    """
    ユーザーに選択肢を提示して選択を取得（カーソルキーで選択）

    Args:
        prompt: プロンプトメッセージ
        choices: 選択肢のリスト

    Returns:
        選択された項目
    """
    result = questionary.select(
        prompt,
        choices=choices,
        instruction="(↑↓ キーで選択、Enterで決定)",
    ).ask()

    if result is None:
        print("\n操作がキャンセルされました。")
        sys.exit(0)

    return result


def main() -> None:
    """メインエントリポイント"""
    try:
        print("=" * 60)
        print("quick_cmd - コマンドランチャー")
        print("=" * 60)

        commands = discover_commands()

        if not commands:
            print("\nエラー: 実行可能なコマンドが見つかりません。")
            print("quick_cmd/commands/ ディレクトリにコマンドを追加してください。")
            sys.exit(1)

        # コマンド名と説明を組み合わせた選択肢を作成
        choices = []
        for cmd in commands:
            desc = get_command_description(cmd)
            if desc:
                # 最初の行のみを使用
                first_line = desc.strip().split("\n")[0]
                choices.append(f"{cmd} - {first_line}")
            else:
                choices.append(cmd)

        selected = get_user_choice("実行するコマンドは？", choices)

        # 選択されたコマンド名を抽出（" - " で分割して最初の部分を取得）
        command_name = selected.split(" - ")[0]

        print(f"\n'{command_name}' を実行します...\n")
        print("-" * 60)

        execute_command(command_name)

        print("-" * 60)
        print("\n完了しました。")

    except KeyboardInterrupt:
        print("\n\n操作がキャンセルされました。")
        sys.exit(0)
    except Exception as e:
        print(f"\nエラーが発生しました: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
