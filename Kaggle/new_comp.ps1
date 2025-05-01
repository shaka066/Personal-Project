param(
  [Parameter(Mandatory)] [string]$Name
)

# エラー時は即停止
$ErrorActionPreference = "Stop"

# UTF-8 コードページに切り替え（非ASCII対応）
chcp 65001 | Out-Null

$root     = "C:\Users\337587\PlayGround\01_Personal\Kaggle"
$template = Join-Path $root "00_comp_template"
$dest     = Join-Path $root $Name

Write-Host "🚀 Creating project '$Name' from template…"

# テンプレートをコピー
Copy-Item $template $dest -Recurse -Force

Push-Location $dest

# 仮想環境作成
Write-Host "🐍 Creating virtual environment…"
python -m venv .venv

# 仮想環境有効化
Write-Host "🔄 Activating .venv…"
& .\.venv\Scripts\Activate.ps1

# pip のアップグレード
Write-Host "⬆️  Upgrading pip…"
python -m pip install --upgrade pip

# 依存関係インストール
Write-Host "📦 Installing requirements…"
python -m pip install --no-cache-dir -r requirements.txt

# pre-commit フック（インストール済みなら）
if (Get-Command pre-commit -ErrorAction SilentlyContinue) {
    Write-Host "🔧 Installing pre-commit hooks…"
    pre-commit install
}

Pop-Location

Write-Host "✅ Project '$Name' created at $dest"
