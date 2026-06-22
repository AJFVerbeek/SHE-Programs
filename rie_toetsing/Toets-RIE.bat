@echo off
REM ============================================================
REM  RI&E-toets-tool - begeleide start voor Windows
REM  Dubbelklik dit bestand. Het stelt vragen en voert daarna
REM  de toetsing zelf uit. Je hoeft geen commando's te typen.
REM ============================================================

cd /d "%~dp0"
echo(
echo ==========================================
echo    RI^&E toetsen - begeleide start
echo ==========================================
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

REM --- 2. Virtuele omgeving + installatie (eenmalig) ---
if not exist ".venv\Scripts\activate.bat" (
    echo Eerste keer: omgeving aanmaken...
    python -m venv .venv
)
call ".venv\Scripts\activate.bat"
rie-toets --version >nul 2>nul
if errorlevel 1 (
    echo Eerste keer: tool installeren ^(kan even duren^)...
    python -m pip install -e . >nul
)

REM --- 3. API-sleutel uit .env laden ---
if exist ".env" (
    for /f "usebackq tokens=1,* delims==" %%a in (".env") do (
        if /i "%%a"=="ANTHROPIC_API_KEY" set "ANTHROPIC_API_KEY=%%b"
    )
)
if not "%ANTHROPIC_API_KEY%"=="" goto :have_key
echo(
echo Er is nog geen API-sleutel gevonden.
set /p KEY=Plak je Claude-sleutel (of laat leeg voor een proefversie):
set "KEY=%KEY:"=%"
if not "%KEY%"=="" set "ANTHROPIC_API_KEY=%KEY%"
:have_key
set "DRYRUN=0"
if "%ANTHROPIC_API_KEY%"=="" set "DRYRUN=1"

echo(
echo ------------------------------------------------------------
echo  Tip: je kunt een bestand in dit venster SLEPEN; dan wordt
echo  het pad automatisch ingevuld. Daarna op Enter drukken.
echo ------------------------------------------------------------
echo(

REM --- 4. Vragen stellen ---
:vraag_rie
set "RIE="
set /p RIE=RI^&E-bestand (verplicht):
set "RIE=%RIE:"=%"
if "%RIE%"=="" (
    echo Geef een bestand op.
    goto :vraag_rie
)
if not exist "%RIE%" (
    echo Bestand niet gevonden: %RIE%
    goto :vraag_rie
)

set "PVA="
set /p PVA=Plan van Aanpak (optioneel, Enter om over te slaan):
set "PVA=%PVA:"=%"

set "ORG="
set /p ORG=Naam van de organisatie:
set "ORG=%ORG:"=%"
if "%ORG%"=="" set "ORG=Onbekend"

set "OUT=toetsrapport.docx"
set /p OUT=Naam uitvoerbestand [toetsrapport.docx]:
set "OUT=%OUT:"=%"
if "%OUT%"=="" set "OUT=toetsrapport.docx"

echo(
echo ------------------------------------------------------------
if "%DRYRUN%"=="1" (
    echo  Geen API-sleutel: er wordt een PROEFVERSIE ^(leeg sjabloon^) gemaakt.
) else (
    echo  De toetsing wordt nu uitgevoerd. Dit duurt 1 tot enkele minuten.
)
echo ------------------------------------------------------------
echo(

REM --- 5. Toetsing uitvoeren ---
if "%DRYRUN%"=="1" (
    if "%PVA%"=="" (
        rie-toets "%RIE%" --org "%ORG%" --dry-run -o "%OUT%"
    ) else (
        rie-toets "%RIE%" --pva "%PVA%" --org "%ORG%" --dry-run -o "%OUT%"
    )
) else (
    if "%PVA%"=="" (
        rie-toets "%RIE%" --org "%ORG%" -o "%OUT%"
    ) else (
        rie-toets "%RIE%" --pva "%PVA%" --org "%ORG%" -o "%OUT%"
    )
)

echo(
if errorlevel 1 (
    echo [FOUT] Er ging iets mis. Lees de meldingen hierboven.
    echo(
    pause
    exit /b 1
)

echo Klaar! Het rapport staat in: %OUT%
echo(
set /p OPEN=Wil je het rapport nu openen? (j/n):
if /i "%OPEN%"=="j" start "" "%OUT%"
echo(
pause
