# 雙擊或執行這個檔案即可：重置肌少症衛教小測驗現場競賽的排行榜。
# QR code 不用換，只有它指向的內容會換成新的一輪。
$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
chcp 65001 > $null
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Split-Path -Parent $scriptDir

Set-Location $repoRoot
python "tools\reset-competition.py"

Write-Host ""
Write-Host "按任意鍵關閉..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
