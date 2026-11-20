param(
    [Parameter(Mandatory = $true)]
    [string]$VideoUrl,

    [string]$OutputName = "YouTube文字起こし"
)

$workspace = Split-Path -Parent $MyInvocation.MyCommand.Path
$toolDir = Join-Path $workspace ".tools"
$outputDir = Join-Path $workspace "outputs"

New-Item -ItemType Directory -Force -Path $toolDir, $outputDir | Out-Null

if (-not (Test-Path (Join-Path $toolDir "yt_dlp"))) {
    python -m pip install --disable-pip-version-check --target $toolDir yt-dlp
    if ($LASTEXITCODE -ne 0) {
        throw "yt-dlpの準備に失敗しました。"
    }
}

$env:PYTHONPATH = $toolDir
$template = Join-Path $outputDir "$OutputName.%(ext)s"

python -m yt_dlp `
    --skip-download `
    --write-auto-subs `
    --sub-langs ja `
    --sub-format vtt `
    --output $template `
    $VideoUrl

if ($LASTEXITCODE -ne 0) {
    throw "YouTube字幕の取得に失敗しました。字幕が提供されていない動画の可能性があります。"
}

Get-ChildItem -LiteralPath $outputDir -Filter "$OutputName*.vtt" |
    Select-Object Name, FullName, Length
