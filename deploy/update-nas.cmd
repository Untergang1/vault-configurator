@echo off
rem Windows blocks unsigned .ps1 files from synced/network folders (RemoteSigned). This runs the script
rem for this one process only, without changing the system execution policy.
pwsh -NoProfile -ExecutionPolicy Bypass -File "%~dp0update-nas.ps1" %*
if errorlevel 9009 powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0update-nas.ps1" %*
