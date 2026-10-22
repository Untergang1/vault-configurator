@echo off
rem Double-click this to run the VAULT configurator on this computer. The first time it fetches what it needs
rem (a few minutes) and asks where your VAULT archive is; after that it just starts and opens
rem http://localhost:8765 in your browser. Closing this window stops it. Nothing leaves your machine.
title VAULT configurator
chcp 65001 >nul
cd /d "%~dp0"
setlocal enabledelayedexpansion

where uv >nul 2>nul
if errorlevel 1 (
  echo.
  echo The VAULT configurator needs "uv", a small tool that fetches Python and the libraries for you.
  echo It installs into your own user folder.
  echo.
  set /p yn="Install uv now? [y/N] "
  if /i not "!yn!"=="y" (
    echo Nothing was installed. You can install uv yourself from https://docs.astral.sh/uv/
    pause
    exit /b 1
  )
  powershell -NoProfile -ExecutionPolicy Bypass -Command "irm https://astral.sh/uv/install.ps1 | iex"
  set "PATH=%USERPROFILE%\.local\bin;%PATH%"
  where uv >nul 2>nul || (
    echo uv could not be installed. Install it from https://docs.astral.sh/uv/ and run this again.
    pause
    exit /b 1
  )
)

rem a git checkout updates itself; a downloaded zip simply runs the version it is
if exist ".git" (where git >nul 2>nul && git pull --ff-only --quiet >nul 2>nul)

rem the archive folder: remembered in archive-path.txt, asked for (once) with the Windows folder picker
set "ARCHIVE="
if exist "archive-path.txt" set /p ARCHIVE=<"archive-path.txt"
if defined ARCHIVE if not exist "!ARCHIVE!\01. DRAWERS\" set "ARCHIVE="
:ask
if not defined ARCHIVE (
  echo.
  echo Choose your VAULT archive folder: the one holding "01. DRAWERS", "02. SUSTAINERS" and "03. MODIFICATIONS".
  for /f "usebackq delims=" %%P in (`powershell -NoProfile -STA -Command "Add-Type -AssemblyName System.Windows.Forms; $d = New-Object System.Windows.Forms.FolderBrowserDialog; $d.Description = 'Choose your VAULT archive folder (the one holding 01. DRAWERS, 02. SUSTAINERS, 03. MODIFICATIONS)'; $d.ShowNewFolderButton = $false; $top = New-Object System.Windows.Forms.Form -Property @{TopMost = $true}; if ($d.ShowDialog($top) -eq 'OK') { $d.SelectedPath }"`) do set "ARCHIVE=%%P"
  if not defined ARCHIVE (
    echo No folder chosen. Run this again when you have the archive at hand.
    pause
    exit /b 1
  )
  if not exist "!ARCHIVE!\01. DRAWERS\" (
    echo "!ARCHIVE!" does not hold "01. DRAWERS". Pick the folder that contains it.
    set "ARCHIVE="
    goto ask
  )
  >"archive-path.txt" echo !ARCHIVE!
)
set "VAULT_ARCHIVE=!ARCHIVE!"

echo.
echo Archive: !ARCHIVE!   (delete archive-path.txt to choose another folder)
echo Starting at http://localhost:8765 - your browser opens in a moment. The first start measures every part
echo once, which takes a few minutes. Leave this window open while you use it; close it to stop.
echo.
uv run --quiet --python 3.13 --with numpy --with pypdf --with pillow python -X utf8 server.py %*
echo.
pause
