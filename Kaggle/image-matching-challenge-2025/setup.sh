#!/usr/bin/env bash
set -e

# --- 仮想環境 ---
python3 -m venv .venv
source .venv/bin/activate

# --- パッケージ ---
pip install -U pip
pip install -r requirements.txt

# --- pre-commit フック ---
if command -v pre-commit >/dev/null 2>&1; then
  pre-commit install
fi

echo "✔ Environment ready"
