# プロジェクト名

## 🎯 目的  
※ここにプロジェクトのゴールや概要を記載

---

## 🚀 環境構築

### 新しいコンペを触るときにやること

### Powershellから以下を実行
   ```bash
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   cd C:\Users\337587\PlayGround\01_Personal\Kaggle
   .\new_comp.ps1 -Name comp_XXXX_XXXX
   ```
### 新たなコンペフォルダ内のREADME更新

1. Python 仮想環境作成

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   ```
2. 依存関係インストール
   ```bash
    pip install -U pip
    pip install -r requirements.txt
   ```
3. pre-commit フック有効化
   ```bash
    pre-commit install
   ```

## 🛠️ VS Code ワークスペース

ワークスペースファイル: your-project.code-workspace

推奨拡張機能:

Python, Pylance, Jupyter, Black Formatter, isort, Prettier

## 🔧 コード整形 & リント
保存時に自動整形（Black＋isort）が走ります

コミット前に Black, isort, Flake8, Mypy を実行

## ✅ テスト
pytest を採用

テストは tests/ フォルダに配置

実行コマンド:
   ```bash
   pytest -q
   ```
## 📓 Jupyter Notebook
ノートブックのルートはワークスペース直下に固定

変数エクスプローラーで実行時の変数を GUI で確認可能

選択セルをインタラクティブウィンドウに送って実行

## 🤝 コーディング規約
PEP8 準拠

import は isort で自動ソート

型チェックは mypy（pre-commit フック）

## 📝 その他
requirements.txt の更新後は必ずテスト＆リンターを実行

新しい拡張機能導入や設定変更はこの README に追記してください