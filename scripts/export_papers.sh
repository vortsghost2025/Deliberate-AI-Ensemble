#!/bin/bash
# WE4FREE Paper Export Script
# Automatically converts all papers to readable formats

echo "WE4FREE Paper Export"
echo "===================="
echo ""

# Check if pandoc is installed
if ! command -v pandoc &> /dev/null; then
    echo "❌ Pandoc not installed"
    echo ""
    echo "To install pandoc on Windows:"
    echo "1. Download from: https://pandoc.org/installing.html"
    echo "2. Or use winget: winget install --id JohnMacFarlane.Pandoc"
    echo "3. Or use chocolatey: choco install pandoc"
    echo ""
    echo "After installation, run this script again."
    exit 1
fi

echo "✓ Pandoc found"
echo ""

# Create output directory
mkdir -p WE4FREE/papers/exports
echo "✓ Created exports directory"
echo ""

# Convert each paper
for paper in WE4FREE/papers/paper_*.md; do
    filename=$(basename "$paper" .md)
    echo "Converting $filename..."

    # To PDF
    pandoc "$paper" -o "WE4FREE/papers/exports/${filename}.pdf" \
        --pdf-engine=xelatex \
        -V geometry:margin=1in \
        --number-sections \
        --toc

    # To DOCX
    pandoc "$paper" -o "WE4FREE/papers/exports/${filename}.docx" \
        --toc \
        --number-sections

    # To HTML
    pandoc "$paper" -o "WE4FREE/papers/exports/${filename}.html" \
        --standalone \
        --toc \
        --css=github-markdown.css

    echo "  ✓ PDF, DOCX, HTML created"
done

echo ""
echo "✓ All papers exported to WE4FREE/papers/exports/"
echo ""
echo "Generated files:"
ls -lh WE4FREE/papers/exports/
