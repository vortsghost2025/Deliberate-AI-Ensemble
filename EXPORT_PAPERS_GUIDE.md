# WE4FREE Papers - Export Guide

## Quick Export (Choose Your Method)

### Method 1: View on GitHub (No Setup Required) ⭐ RECOMMENDED
All papers display perfectly on GitHub with formatting intact:
- https://github.com/vortsghost2025/Deliberate-AI-Ensemble/blob/master/WE4FREE/papers/paper_A.md
- https://github.com/vortsghost2025/Deliberate-AI-Ensemble/blob/master/WE4FREE/papers/paper_B.md
- https://github.com/vortsghost2025/Deliberate-AI-Ensemble/blob/master/WE4FREE/papers/paper_C.md
- https://github.com/vortsghost2025/Deliberate-AI-Ensemble/blob/master/WE4FREE/papers/paper_D.md
- https://github.com/vortsghost2025/Deliberate-AI-Ensemble/blob/master/WE4FREE/papers/paper_E.md

### Method 2: VS Code Preview (Built-in)
1. Open any `paper_X.md` in VS Code
2. Press `Ctrl+Shift+V` (or `Cmd+Shift+V` on Mac)
3. Preview opens with perfect formatting
4. Right-click preview → "Open Preview to the Side"

### Method 3: Export to PDF/Word (Requires Pandoc)

**First time setup:**
```bash
# Restart your terminal first (so PATH updates), then run:
cd /c/workspace
pandoc WE4FREE/papers/paper_A.md -o paper_A.pdf
pandoc WE4FREE/papers/paper_A.md -o paper_A.docx
```

**For Claude to run automatically:**
```bash
# I'll run this command when you ask me to export papers:
cd /c/workspace/WE4FREE/papers && \
for paper in paper_*.md; do \
  pandoc "$paper" -o "exports/${paper%.md}.html" --standalone --toc --self-contained; \
done
```

## What I Set Up For You

**Scripts created (ready to use once PATH updates):**
- `scripts/export_papers.bat` - Windows batch script
- `scripts/export_papers.ps1` - PowerShell script
- `scripts/export_papers.sh` - Bash script

**After restarting your terminal, just run:**
```bash
cd /c/workspace
./scripts/export_papers.bat
```

## For Future Sessions

**When you want me to export papers, just say:**
"Export the papers"

**I'll automatically:**
1. Check if pandoc is available
2. Create exports directory
3. Convert all 5 papers to HTML/PDF/DOCX
4. Tell you where they are

## Current Recommendation

Until you restart your terminal, use **GitHub links** or **VS Code Preview** (`Ctrl+Shift+V`).
Both work perfectly right now with zero setup.
