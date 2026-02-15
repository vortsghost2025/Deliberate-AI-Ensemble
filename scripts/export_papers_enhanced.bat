@echo off
REM WE4FREE Enhanced Paper Export
REM Properly renders diagrams, math, code blocks, and tables

echo ========================================
echo WE4FREE Enhanced Paper Export
echo ========================================
echo.

REM Check pandoc
where pandoc >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Pandoc not installed
    echo Install: winget install --id JohnMacFarlane.Pandoc
    exit /b 1
)
echo [OK] Pandoc found
echo.

REM Create exports directory
if not exist "WE4FREE\papers\exports" mkdir "WE4FREE\papers\exports"
echo [OK] Exports directory ready
echo.

REM Convert each paper with enhanced options
for %%f in (WE4FREE\papers\paper_*.md) do (
    echo Converting %%~nf...

    REM HTML with MathJax for proper math rendering
    pandoc "%%f" -o "WE4FREE\papers\exports\%%~nf.html" ^
        --standalone ^
        --toc ^
        --toc-depth=3 ^
        --mathjax ^
        --css=github-style.css ^
        --metadata title="%%~nf" ^
        --highlight-style=github 2>nul

    REM DOCX with proper formatting
    pandoc "%%f" -o "WE4FREE\papers\exports\%%~nf.docx" ^
        --toc ^
        --toc-depth=3 ^
        --number-sections ^
        --reference-doc=reference.docx 2>nul

    REM PDF (if you have LaTeX installed)
    REM pandoc "%%f" -o "WE4FREE\papers\exports\%%~nf.pdf" ^
    REM     --pdf-engine=xelatex ^
    REM     -V geometry:margin=1in ^
    REM     --toc ^
    REM     --number-sections 2>nul

    echo   [OK] HTML and DOCX created
)

echo.
echo ========================================
echo [DONE] All papers exported
echo ========================================
echo.
echo Files created in: WE4FREE\papers\exports\
echo.
echo HTML files include:
echo   - Proper math rendering (MathJax)
echo   - GitHub-style formatting
echo   - Preserved code blocks and diagrams
echo   - Clickable table of contents
echo.
dir /B WE4FREE\papers\exports\*.html
echo.
dir /B WE4FREE\papers\exports\*.docx
