@echo off
REM ============================================================
REM  RI&E-toets-tool - startscript voor Windows
REM  Dubbelklik dit bestand. Het installeert (eenmalig) alles
REM  en laat een venster achter waarin je 'rie-toets' kunt typen.
REM ============================================================

cd /d "%~dp0"
echo(
echo === RI^&E-toets-tool ===
echo(

REM --- 1. Python controleren ---
where python >nul 2>nul
if errorlevel 1 (
    echo [FOUT] Python is niet gevonden.
    echo Installeer Python 3.11+ via https://www.python.org/downloads/
    echo Vink bij de installatie "Add Python to PATH" aan.
    echo(
    pause
    exit /b 1
)

REM --- 2. Virtuele omgeving aanmaken (eenmalig) ---
if not exist ".venv\Scripts\activate.bat" (
    echo [1/3] Virtuele omgeving aanmaken...
    python -m venv .venv
)

REM --- 3. Omgeving activeren ---
call ".venv\Scripts\activate.bat"

REM --- 4. Tool installeren als 'rie-toets' nog niet werkt ---
rie-toets --version >nul 2>nul
if errorlevel 1 (
    echo [2/3] Tool installeren ^(kan even duren^)...
    python -m pip install -e . >nul
)

REM --- 5. API-sleutel uit .env laden (indien aanwezig) ---
if exist ".env" (
    for /f "usebackq tokens=1,* delims==" %%a in (".env") do (
        if /i "%%a"=="ANTHROPIC_API_KEY" set "ANTHROPIC_API_KEY=%%b"
    )
)

echo [3/3] Klaar.
echo(
rie-toets --version
echo(

if "%ANTHROPIC_API_KEY%"=="" (
    echo [LET OP] Geen API-sleutel gevonden.
    echo Maak een bestand .env met de regel:  ANTHROPIC_API_KEY=sk-ant-...
    echo of typ in dit venster:  set ANTHROPIC_API_KEY=sk-ant-...
    echo Zonder sleutel werkt alleen --dry-run.
) else (
    echo API-sleutel gevonden. Je kunt nu toetsen.
)

echo(
echo ------------------------------------------------------------
echo  Voorbeelden ^(typ hieronder en druk op Enter^):
echo(
echo   Test zonder sleutel:
echo     rie-toets RIE.pdf --org "Test B.V." --dry-run -o test.docx
echo(
echo   Echte toetsing:
echo     rie-toets RIE.pdf --pva PlanVanAanpak.pdf --org "Naam B.V." -o toetsrapport.docx
echo(
echo   Met AMM-sjabloon:
echo     rie-toets RIE.pdf --org "Naam B.V." --sjabloon AMM_SJABLOON.docx -o toetsrapport.docx
echo(
echo   Alle opties:  rie-toets --help
echo ------------------------------------------------------------
echo  Tip: leg je RIE- en PvA-bestanden in deze map ^(rie_toetsing^).
echo ------------------------------------------------------------
echo(

REM --- Laat het venster open met de omgeving actief ---
cmd /k
