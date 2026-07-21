# Verplaatst een afgerond dossier van "2_Lopende dossiers" naar
# "5_Afgeronde dossiers". Het dossier gaat integraal mee (alle submappen).
#
# Gebruik (PowerShell):
#   .\Archiveer-Dossier.ps1 -Root "C:\...\P176_2 Arboned Toetsingen" -Dossier "525 Synthos (Andre)"
#
# De naam mag ook gedeeltelijk zijn; bij precies een treffer wordt die verplaatst:
#   .\Archiveer-Dossier.ps1 -Dossier "Synthos"

param(
    [Parameter(Mandatory = $true)][string]$Dossier,
    [string]$Root = (Get-Location).Path
)

$lopend = Join-Path $Root "2_Lopende dossiers"
$afgerond = Join-Path $Root "5_Afgeronde dossiers"

foreach ($map in @($lopend, $afgerond)) {
    if (-not (Test-Path $map)) {
        Write-Error "Map niet gevonden: $map (draai eerst Maak-Mapstructuur.ps1)"
        exit 1
    }
}

$treffers = @(Get-ChildItem -Path $lopend -Directory | Where-Object { $_.Name -like "*$Dossier*" })

if ($treffers.Count -eq 0) {
    Write-Error "Geen dossier gevonden dat '$Dossier' bevat in '2_Lopende dossiers'."
    exit 1
}
if ($treffers.Count -gt 1) {
    Write-Host "Meerdere treffers, geef een specifiekere naam op:" -ForegroundColor Yellow
    $treffers | ForEach-Object { Write-Host "  $($_.Name)" }
    exit 1
}

$bron = $treffers[0]
$doel = Join-Path $afgerond $bron.Name

if (Test-Path $doel) {
    Write-Error "Bestaat al in het archief: $($bron.Name)"
    exit 1
}

Move-Item -Path $bron.FullName -Destination $doel
Write-Host "Gearchiveerd: $($bron.Name) -> 5_Afgeronde dossiers" -ForegroundColor Green
