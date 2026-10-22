#!/usr/bin/env bash
# Shared by "Start VAULT (Mac).command" and "Start VAULT (Linux).sh": installs uv once (asks first), asks for
# the VAULT archive folder once (system folder picker, else a typed path) and remembers it in
# archive-path.txt, then starts the configurator at http://localhost:8765 and opens the browser.
set -u
cd "$(dirname "$0")"

if ! command -v uv >/dev/null 2>&1; then
  export PATH="$HOME/.local/bin:$PATH"
fi
if ! command -v uv >/dev/null 2>&1; then
  echo
  echo 'The VAULT configurator needs "uv", a small tool that fetches Python and the libraries for you.'
  echo 'It installs into your own user folder.'
  read -r -p "Install uv now? [y/N] " yn
  case "$yn" in [yY]*) ;; *) echo "Nothing was installed. Get uv from https://docs.astral.sh/uv/"; exit 1 ;; esac
  curl -LsSf https://astral.sh/uv/install.sh | sh || { echo "uv could not be installed."; exit 1; }
  export PATH="$HOME/.local/bin:$PATH"
fi

# a git checkout updates itself; a downloaded zip simply runs the version it is
if [ -d .git ] && command -v git >/dev/null 2>&1; then git pull --ff-only --quiet >/dev/null 2>&1 || true; fi

valid() { [ -n "${1:-}" ] && [ -d "$1/01. DRAWERS" ]; }
pick() {
  local prompt='Choose your VAULT archive folder (the one holding 01. DRAWERS, 02. SUSTAINERS, 03. MODIFICATIONS)'
  if [ "$(uname)" = "Darwin" ]; then
    osascript -e "POSIX path of (choose folder with prompt \"$prompt\")" 2>/dev/null | sed 's:/$::'
  elif [ -n "${DISPLAY:-}${WAYLAND_DISPLAY:-}" ] && command -v zenity >/dev/null 2>&1; then
    zenity --file-selection --directory --title="$prompt" 2>/dev/null
  elif [ -n "${DISPLAY:-}${WAYLAND_DISPLAY:-}" ] && command -v kdialog >/dev/null 2>&1; then
    kdialog --getexistingdirectory "$HOME" --title "$prompt" 2>/dev/null
  else
    read -r -p "$prompt: " p; echo "$p"
  fi
}

ARCHIVE="$(cat archive-path.txt 2>/dev/null || true)"
until valid "$ARCHIVE"; do
  [ -n "$ARCHIVE" ] && echo "\"$ARCHIVE\" does not hold \"01. DRAWERS\"; pick the folder that contains it."
  ARCHIVE="$(pick)"
  [ -z "$ARCHIVE" ] && { echo "No folder chosen. Run this again when you have the archive at hand."; exit 1; }
  printf '%s\n' "$ARCHIVE" > archive-path.txt
done
export VAULT_ARCHIVE="$ARCHIVE"

echo
echo "Archive: $ARCHIVE   (delete archive-path.txt to choose another folder)"
echo "Starting at http://localhost:8765; your browser opens in a moment. The first start measures every part"
echo "once, which takes a few minutes. Leave this window open while you use it; close it to stop."
echo
exec uv run --quiet --python 3.13 --with numpy --with pypdf --with pillow python -X utf8 server.py "$@"
