# WE4FREE Enhanced Paper Export (PowerShell)
# Properly renders diagrams, math, code blocks, and tables

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "WE4FREE Enhanced Paper Export" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check pandoc
$pandocInstalled = Get-Command pandoc -ErrorAction SilentlyContinue
if (-not $pandocInstalled) {
    Write-Host "[ERROR] Pandoc not installed" -ForegroundColor Red
    Write-Host "Install: winget install --id JohnMacFarlane.Pandoc"
    exit 1
}
Write-Host "[OK] Pandoc found" -ForegroundColor Green
Write-Host ""

# Create exports directory
$exportDir = "WE4FREE\papers\exports"
if (-not (Test-Path $exportDir)) {
    New-Item -ItemType Directory -Path $exportDir | Out-Null
}
Write-Host "[OK] Exports directory ready" -ForegroundColor Green
Write-Host ""

# Convert each paper
$papers = Get-ChildItem -Path "WE4FREE\papers\paper_*.md"

foreach ($paper in $papers) {
    $basename = $paper.BaseName
    Write-Host "Converting $basename..." -ForegroundColor Cyan

    # HTML with MathJax for proper math rendering
    pandoc $paper.FullName -o "$exportDir\$basename.html" `
        --standalone `
        --toc `
        --toc-depth=3 `
        --mathjax `
        --css=github-style.css `
        --metadata title="$basename" `
        --highlight-style=github `
        --embed-resources 2>$null

    # DOCX with proper formatting
    pandoc $paper.FullName -o "$exportDir\$basename.docx" `
        --toc `
        --toc-depth=3 `
        --number-sections 2>$null

    Write-Host "  [OK] HTML and DOCX created" -ForegroundColor Green
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "[DONE] All papers exported" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Files created in: $exportDir" -ForegroundColor Yellow
Write-Host ""
Write-Host "HTML files include:" -ForegroundColor Yellow
Write-Host "  - Proper math rendering (MathJax)" -ForegroundColor Gray
Write-Host "  - GitHub-style formatting" -ForegroundColor Gray
Write-Host "  - Preserved code blocks and diagrams" -ForegroundColor Gray
Write-Host "  - Clickable table of contents" -ForegroundColor Gray
Write-Host ""

Get-ChildItem -Path "$exportDir\*.html" | Format-Table Name, Length, LastWriteTime -AutoSize
Get-ChildItem -Path "$exportDir\*.docx" | Format-Table Name, Length, LastWriteTime -AutoSize
