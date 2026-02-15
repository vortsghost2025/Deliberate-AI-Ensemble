# Enhanced Paper Export - Quick Reference

## For Claude (Auto-Export in Future Sessions)

When user says "export papers" or "export the papers", run:

```bash
cd /c/workspace && cmd //c "scripts\export_papers_enhanced.bat"
```

Or in PowerShell context:
```powershell
cd C:\workspace && powershell -File scripts\export_papers_enhanced.ps1
```

## What Gets Fixed

**Previous issues:**
- ❌ Math equations not rendering (showed as raw TeX)
- ❌ Code blocks had minimal styling
- ❌ Tables looked plain
- ❌ No proper syntax highlighting

**Now fixed:**
- ✅ Math equations render properly with MathJax
- ✅ GitHub-style code blocks (gray backgrounds)
- ✅ Properly formatted tables
- ✅ Syntax highlighting for code
- ✅ ASCII diagrams preserved
- ✅ Clean, professional appearance

## For Manual Export

**Windows (recommended):**
```cmd
cd C:\workspace
scripts\export_papers_enhanced.bat
```

**PowerShell:**
```powershell
cd C:\workspace
.\scripts\export_papers_enhanced.ps1
```

## Output Location

All files in: `WE4FREE\papers\exports\`

**Each paper generates:**
- `.html` - Web page with MathJax, GitHub styling
- `.docx` - Microsoft Word document

## Testing the Export

After running, check:
1. Open `exports/paper_A.html` in browser
2. Math equations should be properly formatted (not raw TeX)
3. Code blocks should have gray backgrounds
4. Tables should look like actual tables
5. ASCII diagrams should be preserved

## First Run

```powershell
cd C:\workspace
.\scripts\export_papers_enhanced.ps1
```

Then open `WE4FREE\papers\exports\paper_A.html` to verify everything looks good.
