# Paper Export Scripts

Automatically convert all WE4FREE papers to PDF, DOCX, and HTML formats.

## Quick Start

### Windows (PowerShell - Recommended)
```powershell
.\scripts\export_papers.ps1
```

### Windows/Mac/Linux (Bash)
```bash
bash scripts/export_papers.sh
```

## First-Time Setup

1. **Install Pandoc:**
   - Windows: `winget install --id JohnMacFarlane.Pandoc`
   - Or download: https://pandoc.org/installing.html

2. **Run the script:**
   ```powershell
   .\scripts\export_papers.ps1
   ```

3. **Find your exports:**
   All converted files will be in `WE4FREE/papers/exports/`

## What Gets Generated

For each paper (A through E):
- `paper_X.pdf` - PDF with table of contents
- `paper_X.docx` - Microsoft Word format
- `paper_X.html` - Standalone HTML

## Usage in Future Sessions

Just run:
```powershell
.\scripts\export_papers.ps1
```

The script will:
- Check if pandoc is installed
- Create exports directory if needed
- Convert all papers
- Show you what was generated

## For Claude

When user asks to export papers, run:
```bash
cd /workspace && powershell -File scripts/export_papers.ps1
```

Or if pandoc not installed yet:
```bash
winget install --id JohnMacFarlane.Pandoc
```
