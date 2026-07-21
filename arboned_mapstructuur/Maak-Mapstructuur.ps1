# Maakt het lege mapraamwerk aan voor "P176_2 ArboNed Toetsingen"
# volgens VOORSTEL_MAPSTRUCTUUR.md. Verplaatst of verwijdert niets:
# bestaande mappen en bestanden blijven ongemoeid.
#
# Gebruik (PowerShell):
#   .\Maak-Mapstructuur.ps1 -Root "C:\Users\<naam>\OneDrive - AMM Consultancy\...\P176_2 Arboned Toetsingen"
#
# Zonder -Root wordt de huidige map gebruikt.

param(
    [string]$Root = (Get-Location).Path
)

if (-not (Test-Path $Root)) {
    Write-Error "Map niet gevonden: $Root"
    exit 1
}

$mappen = @(
    "0_Beheer\Uren",
    "0_Beheer\Correspondentie",
    "0_Beheer\Overleg A&O-ers",
    "0_Beheer\Diversen",
    "1_Sjablonen\Toetsrapport",
    "1_Sjablonen\Prompts",
    "1_Sjablonen\Enquete",
    "1_Sjablonen\Logo en huisstijl",
    "1_Sjablonen\_Oude versies",
    "2_Lopende dossiers",
    "3_AI-pijplijn\1_Input",
    "3_AI-pijplijn\2_Beoordeeld",
    "3_AI-pijplijn\3_Toetsrapporten",
    "4_Enquetes",
    "5_Afgeronde dossiers",
    "6_Naslag"
)

# Dossiersjabloon: kopieren en hernoemen bij een nieuw dossier
$dossierSjabloon = "1_Sjablonen\_Nieuw dossier NNN Klantnaam (Adviseur)"
$mappen += @(
    "$dossierSjabloon\1_Input",
    "$dossierSjabloon\2_Beoordeling",
    "$dossierSjabloon\3_Rapport",
    "$dossierSjabloon\4_Verzonden"
)

$aangemaakt = 0
foreach ($map in $mappen) {
    $pad = Join-Path $Root $map
    if (-not (Test-Path $pad)) {
        New-Item -ItemType Directory -Path $pad -Force | Out-Null
        Write-Host "Aangemaakt: $map"
        $aangemaakt++
    }
    else {
        Write-Host "Bestaat al: $map" -ForegroundColor DarkGray
    }
}

Write-Host ""
Write-Host "Klaar. $aangemaakt map(pen) aangemaakt in: $Root" -ForegroundColor Green
Write-Host "Volg nu het migratieplan in VOORSTEL_MAPSTRUCTUUR.md (stap 2 t/m 9)."
