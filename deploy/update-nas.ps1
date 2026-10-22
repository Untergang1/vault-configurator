# Publish the working copy, make the NAS redeploy it, wait until the NAS runs exactly this build, then run the
# end-to-end smoke test against it. Everything happens from the PC; nothing to do on the NAS after setup.
#
# Settings come from working-files\nas.env (never published), lines like:
#   NAS_URL=http://<nas>:8765
#   DOCKHAND_WEBHOOK=http://<dockhand>/api/git/webhook/<repositoryId>     (optional: without it, wait for the cron)
#   DOCKHAND_SECRET=<the secret Dockhand generated for that webhook>        (optional)
param([switch]$SkipPublish, [int]$TimeoutMinutes = 25)
$ErrorActionPreference = "Stop"
$app = Split-Path $PSScriptRoot -Parent
$envFile = Join-Path (Split-Path $app -Parent) "working-files\nas.env"
$cfg = @{}
if (Test-Path $envFile) { Get-Content $envFile | Where-Object { $_ -match '^\s*([A-Z_]+)\s*=\s*(.+?)\s*$' } | ForEach-Object { $cfg[$Matches[1]] = $Matches[2] } }
$nas = $cfg["NAS_URL"]; if (-not $nas) { throw "set NAS_URL in $envFile (see deploy/README.md)" }
$py = (Get-Command python -ErrorAction SilentlyContinue).Source
if (-not $py) { $py = "$env:LOCALAPPDATA\Microsoft\WindowsApps\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\python.exe" }

if (-not $SkipPublish) { & (Join-Path $app "publish-github.ps1") -Message "Update" }
$want = (& $py (Join-Path $app "version.py")).Trim()
"local build: $want"

# the NAS pulls the image GitHub Actions builds from the pushed commit: wait for that build first
$public = Join-Path (Split-Path (Split-Path $app -Parent) -Parent) "vault-configurator-public"
$sha = (git -C $public rev-parse HEAD).Trim()
$run = $null
for ($i = 0; $i -lt 30 -and -not $run; $i++) {
    $run = gh run list --repo marcelfarres/vault-configurator --workflow docker --commit $sha --json databaseId --jq '.[0].databaseId' 2>$null
    if (-not $run) { Start-Sleep 5 }
}
if ($run) { "waiting for image build (run $run)"; gh run watch $run --repo marcelfarres/vault-configurator --exit-status | Out-Null; if ($LASTEXITCODE) { throw "image build failed: gh run view $run --repo marcelfarres/vault-configurator --log-failed" } }
else { "no image build found for $sha (nothing new published?); redeploying the current image" }

if ($cfg["DOCKHAND_WEBHOOK"]) {
    $body = '{"ref":"refs/heads/main"}'
    $headers = @{ "X-GitHub-Event" = "push" }
    if ($cfg["DOCKHAND_SECRET"]) {
        $hmac = New-Object System.Security.Cryptography.HMACSHA256 (,[Text.Encoding]::UTF8.GetBytes($cfg["DOCKHAND_SECRET"]))
        $headers["X-Hub-Signature-256"] = "sha256=" + (-join ($hmac.ComputeHash([Text.Encoding]::UTF8.GetBytes($body)) | ForEach-Object { $_.ToString("x2") }))
    }
    $r = Invoke-WebRequest -UseBasicParsing -Method POST -Uri $cfg["DOCKHAND_WEBHOOK"] -Body $body -ContentType "application/json" -Headers $headers -SkipHttpErrorCheck
    "webhook: HTTP $($r.StatusCode)"
} else { "no DOCKHAND_WEBHOOK set: waiting for Dockhand's scheduled sync" }

$deadline = (Get-Date).AddMinutes($TimeoutMinutes)
do {
    Start-Sleep 20
    try { $got = (Invoke-RestMethod "$nas/api/meta" -TimeoutSec 15).build } catch { $got = "(down: rebuilding?)" }
    "NAS build: $got"
} until ($got -eq $want -or (Get-Date) -gt $deadline)
if ($got -ne $want) { throw "the NAS did not reach build $want within $TimeoutMinutes minutes" }

& $py -X utf8 (Join-Path $PSScriptRoot "smoke_test.py") $nas
