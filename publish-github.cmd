@echo off
rem See deploy\update-nas.cmd: runs the .ps1 for this process only, the system execution policy is untouched.
pwsh -NoProfile -ExecutionPolicy Bypass -File "%~dp0publish-github.ps1" %*
if errorlevel 9009 powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0publish-github.ps1" %*
