# quick_cmd

カーソルキーで選択して実行するコマンドランチャー CLI ツール

## 概要

`quick_cmd` は、複数のコマンドをカーソルキーで選択して実行できるコマンドラインツールです。よく使うコマンドや作業手順をPythonスクリプトとして登録し、簡単に呼び出せます。

## 機能

- **カーソルキー操作**: 矢印キーで選択肢を選ぶ直感的なUI
- **コマンド自動検出**: `commands/` ディレクトリ内のPythonファイルを自動的に検出
- **説明表示**: 各コマンドのdocstringを選択肢に表示
- **簡単な拡張**: 新しいコマンドは `.py` ファイルを追加するだけ

## 必要要件

- Python 3.10以上

## インストール

```bash
# リポジトリをクローン
git clone https://github.com/yourname/quick_cmd.git
cd quick_cmd

# パッケージをインストール
pip install .

# または開発モードでインストール
pip install -e .
```

## 使用方法

コマンドを実行するだけです：

```bash
quick_cmd
```

インタラクティブな選択画面が表示されます：

```
$ quick_cmd
============================================================
quick_cmd - コマンドランチャー
============================================================
? 実行するコマンドは？ (↑↓ キーで選択、Enterで決定)
 » example - サンプルコマンド
   open_daily - 日報を開く
   create_report - レポートを作成
```

## コマンドの追加方法

`src/quick_cmd/commands/` ディレクトリに `.py` ファイルを作成します。

### コマンドファイルの形式

```python
"""コマンドの説明（選択肢に表示されます）

複数行の説明も書けますが、
選択肢には最初の1行のみ表示されます。
"""

def run() -> None:
    """コマンドのメイン処理"""
    print("処理を実行します")

    # 複数の作業を記述
    task1()
    task2()
    task3()

def task1() -> None:
    """タスク1"""
    pass

def task2() -> None:
    """タスク2"""
    pass

def task3() -> None:
    """タスク3"""
    pass
```

### 必須要素

1. **モジュールのdocstring**: コマンドの説明として選択肢に表示されます
2. **`run()` 関数**: コマンド実行時に呼び出されるエントリポイント

### コマンドの例

#### 日報を開くコマンド (`open_daily.py`)

```python
"""日報ファイルを開く"""

import subprocess
from datetime import datetime


def run() -> None:
    """今日の日報を開く"""
    today = datetime.now().strftime("%Y-%m-%d")
    filepath = f"~/Documents/diary/{today}.md"
    subprocess.run(["open", filepath])
```

#### バックアップコマンド (`backup.py`)

```python
"""プロジェクトをバックアップ"""

import shutil
from datetime import datetime
from pathlib import Path


def run() -> None:
    """プロジェクトをバックアップディレクトリにコピー"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    src = Path.cwd()
    dst = Path.home() / "backup" / f"{src.name}_{timestamp}"

    print(f"バックアップ先: {dst}")
    shutil.copytree(src, dst)
    print("完了しました")
```

## ディレクトリ構造

```
quick_cmd/
├── pyproject.toml
├── README.md
├── LICENSE
├── src/
│   └── quick_cmd/
│       ├── __init__.py
│       ├── __main__.py
│       ├── cli.py
│       └── commands/
│           ├── __init__.py
│           ├── example.py
│           └── (追加するコマンド.py)
└── tests/
```

## 開発

```bash
# 開発用依存関係を含めてインストール
pip install -e ".[dev]"

# テスト実行
pytest

# コードフォーマット
black src/

# 型チェック
mypy src/
```

## トラブルシューティング

### コマンドが表示されない

- `src/quick_cmd/commands/` ディレクトリにファイルが配置されているか確認
- ファイル名が `_` で始まっていないか確認（`_` で始まるファイルは除外されます）
- Pythonの構文エラーがないか確認

### コマンド実行時にエラーが発生する

- コマンドファイルに `run()` 関数が定義されているか確認
- 必要な依存パッケージがインストールされているか確認

## ライセンス

MIT License
