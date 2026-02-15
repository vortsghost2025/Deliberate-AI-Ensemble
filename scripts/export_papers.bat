@echo off
REM WE4FREE Paper Export (Windows Batch)
REM Simple one-command export for all papers

echo WE4FREE Paper Export
echo ====================
echo.

REM Check if pandoc exists
where pandoc >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Pandoc not installed
    echo Install with: winget install --id JohnMacFarlane.Pandoc
    exit /b 1
)

echo [OK] Pandoc found
echo.

REM Create exports directory
if not exist "WE4FREE\papers\exports" mkdir "WE4FREE\papers\exports"
echo [OK] Exports directory ready
echo.

REM Convert each paper
for %%f in (WE4FREE\papers\paper_*.md) do (
    echo Converting %%~nf...

    REM PDF
    pandoc "%%f" -o "WE4FREE\papers\exports\%%~nf.pdf" --pdf-engine=xelatex -V geometry:margin=1in --number-sections --toc 2>nul

    REM DOCX
    pandoc "%%f" -o "WE4FREE\papers\exports\%%~nf.docx" --toc --number-sections 2>nul

    REM HTML
    pandoc "%%f" -o "WE4FREE\papers\exports\%%~nf.html" --standalone --toc --self-contained 2>nul

    echo   [OK] PDF, DOCX, HTML created
)

echo.
echo [DONE] All papers exported to WE4FREE\papers\exports\
echo.
dir /B WE4FREE\papers\exports\
