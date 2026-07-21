# Start een nieuw klantdossier in "2_Lopende dossiers" met de vaste
# submapindeling (1_Input, 2_Beoordeling, 3_Rapport, 4_Verzonden).
# Kiest automatisch het eerstvolgende vrije dossiernummer op basis van
# de mappen in "2_Lopende dossiers" en "5_Afgeronde dossiers".
#
# Gebruik (PowerShell):
#   .\Nieuw-Dossier.ps1 -Root "C:\...\P176_2 Arboned Toetsingen" -Klant "Bakkerij Jansen" -Adviseur "Marcel"
#
# Optioneel een vast nummer opgeven:
#   .\Nieuw-Dossier.ps1 -Klant "Bakkerij Jansen" -Adviseur "Marcel" -Nummer 540

param(
    [Parameter(Mandatory = $true)][string]$Klant,
    [Parameter(Mandatory = $true)][string]$Adviseur,
    [string]$Root = (Get-Location).Path,
    [int]$Nummer = 0
)

$lopend = Join-Path $Root "2_Lopende dossiers"
$afgerond = Join-Path $Root "5_Afgeronde dossiers"

if (-not (Test-Path $lopend)) {
    Write-Error "Map '2_Lopende dossiers' niet gevonden onder: $Root (draai eerst Maak-Mapstructuur.ps1)"
    exit 1
}

if ($Nummer -eq 0) {
    # Hoogste bestaande dossiernummer zoeken in lopende en afgeronde dossiers
    $hoogste = 0
    foreach ($bron in @($lopend, $afgerond)) {
        if (Test-Path $bron) {
            Get-ChildItem -Path $bron -Directory | ForEach-Object {
                if ($_.Name -match '^(\d+)') {
                    $n = [int]$Matches[1]
                    if ($n -gt $hoogste) { $hoogste = $n }
                }
            }
        }
    }
    $Nummer = $hoogste + 1
}

$naam = "{0} {1} ({2})" -f $Nummer, $Klant, $Adviseur
$dossier = Join-Path $lopend $naam

if (Test-Path $dossier) {
    Write-Error "Dossier bestaat al: $naam"
    exit 1
}

foreach ($sub in @("1_Input", "2_Beoordeling", "3_Rapport", "4_Verzonden")) {
    New-Item -ItemType Directory -Path (Join-Path $dossier $sub) -Force | Out-Null
}

Write-Host "Nieuw dossier aangemaakt: 2_Lopende dossiers\$naam" -ForegroundColor Green
