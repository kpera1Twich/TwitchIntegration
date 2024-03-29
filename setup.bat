@echo off

set exitCode=0
set exitReason=""


::Check for Admin Privileges as some requirements need them to be installed
net session >nul 2>&1
if %errorlevel% neq 0 (
    set /p exitCode=1
    set .p exitReason="Not running with admin privileges"
)


::Install external requirements
powershell -Command "Install-PackageProvider -Name NuGet -MinimumVersion 2.8.5.201 -Force"
powershell -Command "Install-Module -Name AudioDeviceCmdlets -Confirm:$False -Force"
if %errorlevel% neq 0 (
    set /p exitCode=2
    set /p exitReason="Could not install AudioDeviceCmdlets"
)


::Make a venv
cd "%~dp0"
py -m venv venv
if %errorlevel% neq 0 (
    set /p exitCode=3
    set /p exitReason="Could not create venv"
)


::Install python packages
.\venv\Scripts\activate && py -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    set /p exitCode=4
    set /p exitReason="Could not install python requirements"
)


::Final setup
copy /y configs.json configs-user.json


:Exit
    echo exitReason
    echo "Press enter to exit"
    pause >nul
    exit /b exitCode
