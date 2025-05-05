param(
    [Parameter(Mandatory)] [string]$Name
)

# エラー時は即停止
$ErrorActionPreference = "Stop"

# UTF-8 コードページに切り替え（非ASCII対応）
chcp 65001 | Out-Null

# プロジェクトルートとテンプレートパス
$root     = "C:\Users\337587\PlayGround\01_Personal\Kaggle"
$template = Join-Path $root "00_comp_template"
$dest     = Join-Path $root $Name

Write-Host "🚀 Creating project '$Name' from template…"

# テンプレートをコピー
Copy-Item $template $dest -Recurse -Force

Push-Location $dest

# 仮想環境作成
Write-Host "🐍 Creating virtual environment…"
python -m venv venv01

# 仮想環境有効化
Write-Host "🔄 Activating virtual environment…"
& .\venv01\Scripts\Activate.ps1

# pip のアップグレード
Write-Host "⬆️  Upgrading pip…"
python -m pip install --upgrade pip

# 依存関係インストール
Write-Host "📦 Installing requirements…"
python -m pip install --no-cache-dir -r requirements.txt

# Jupyterカーネル用パッケージを追加インストール
Write-Host "📘 Installing Jupyter & ipykernel…"
python -m pip install --no-cache-dir notebook ipykernel

# カーネル登録
ing $kernelName = "$Name"
ing $displayName = "$Name (Python)"
Write-Host "🌐 Registering Jupyter kernel: $kernelName …"
python -m ipykernel install --user --name $kernelName --display-name "$displayName"

# VS Code 用設定ディレクトリ & settings.json を作成
$vscodeDir = Join-Path $dest ".vscode"
if (!(Test-Path $vscodeDir)) {
    New-Item -ItemType Directory -Path $vscodeDir | Out-Null
}

$settings = @{
    "python.defaultInterpreterPath" = "${dest}\\venv01\\Scripts\\python.exe"
    "jupyter.notebookFileRoot"     = "${fileDirname}"
}
$settingsJson = $settings | ConvertTo-Json -Depth 3
$settingsFile = Join-Path $vscodeDir "settings.json"
$settingsJson | Out-File -FilePath $settingsFile -Encoding UTF8

# pre-commit フック（あれば）
if (Get-Command pre-commit -ErrorAction SilentlyContinue) {
    Write-Host "🔧 Installing pre-commit hooks…"
    pre-commit install
}

# マルチルートワークスペースファイルの自動更新ブロック
Write-Host "🔄 Updating multi-root workspace file…"
$workspaceFile = Join-Path $root "kaggle.code-workspace"
$folders = Get-ChildItem -Path $root -Directory |
           Where-Object { $_.Name -notin @(".git", ".vscode") } |
           ForEach-Object { @{ path = $_.Name } }

$workspace = @{
    folders  = $folders
    settings = @{}
}

$workspace | ConvertTo-Json -Depth 5 | Out-File -FilePath $workspaceFile -Encoding UTF8
Write-Host "🌐 Workspace file refreshed: $workspaceFile"

Pop-Location

Write-Host "✅ Project '$Name' created at $dest"
