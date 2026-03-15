# WE4FREE Paper Export Script (PowerShell)
# Automatically converts all papers to readable formats

Write-Host "WE4FREE Paper Export" -ForegroundColor Cyan
Write-Host "====================" -ForegroundColor Cyan
Write-Host ""

# Check if pandoc is installed
$pandocInstalled = Get-Command pandoc -ErrorAction SilentlyContinue

if (-not $pandocInstalled) {
    Write-Host "❌ Pandoc not installed" -ForegroundColor Red
    Write-Host ""
    Write-Host "To install pandoc on Windows:" -ForegroundColor Yellow
    Write-Host "1. Download from: https://pandoc.org/installing.html"
    Write-Host "2. Or use winget: winget install --id JohnMacFarlane.Pandoc"
    Write-Host "3. Or use chocolatey: choco install pandoc"
    Write-Host ""
    Write-Host "After installation, run this script again."
    exit 1
}

Write-Host "✓ Pandoc found" -ForegroundColor Green
Write-Host ""

# Create output directory
$exportDir = "WE4FREE\papers\exports"
if (-not (Test-Path $exportDir)) {
    New-Item -ItemType Directory -Path $exportDir | Out-Null
}
Write-Host "✓ Created exports directory" -ForegroundColor Green
Write-Host ""

# Convert each paper
$papers = Get-ChildItem -Path "WE4FREE\papers\paper_*.md"

foreach ($paper in $papers) {
    $filename = $paper.BaseName
    Write-Host "Converting $filename..." -ForegroundColor Cyan

    # To PDF
    pandoc $paper.FullName -o "$exportDir\${filename}.pdf" `
        --pdf-engine=xelatex `
        -V geometry:margin=1in `
        --number-sections `
        --toc

    # To DOCX
    pandoc $paper.FullName -o "$exportDir\${filename}.docx" `
        --toc `
        --number-sections

    # To HTML
    pandoc $paper.FullName -o "$exportDir\${filename}.html" `
        --standalone `
        --toc `
        --self-contained

    Write-Host "  ✓ PDF, DOCX, HTML created" -ForegroundColor Green
}

Write-Host ""
Write-Host "✓ All papers exported to $exportDir" -ForegroundColor Green
Write-Host ""
Write-Host "Generated files:" -ForegroundColor Cyan
Get-ChildItem -Path $exportDir | Format-Table Name, Length, LastWriteTime
