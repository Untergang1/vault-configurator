# Sync this folder (the tool only, never the archive, never generated assets) into the public GitHub
# repository checkout next to the archive folder, commit and push. The Forgejo repo at the parent
# level keeps the full, private, self-contained copy.
param(
    [string]$Public = (Join-Path (Split-Path (Split-Path $PSScriptRoot -Parent) -Parent) "vault-configurator-public"),
    [string]$Message = "Sync from the working copy"
)
$ErrorActionPreference = "Stop"
if (-not (Test-Path (Join-Path $Public ".git"))) {
    gh auth setup-git | Out-Null   # git pushes over https with the gh login
    git clone https://github.com/marcelfarres/vault-configurator.git $Public
    if ($LASTEXITCODE -ne 0) { throw "clone failed" }
}
# robocopy mirrors the tree; excluded: generated pictures, caches, outputs, scratch, the unfinished static experiment
robocopy $PSScriptRoot $Public /MIR /XD assets cache output __pycache__ static .git /XF gen_static_data.py archive-path.txt /NFL /NDL /NJH /NJS | Out-Null
if ($LASTEXITCODE -ge 8) { throw "robocopy failed ($LASTEXITCODE)" }
Push-Location $Public
git add -A
git update-index --chmod=+x start.sh "Start VAULT (Mac).command" "Start VAULT (Linux).sh"  # Windows has no exec bit to copy
if (git status --porcelain) { git commit -q -m $Message; git push origin main } else { "nothing to publish" }
Pop-Location
