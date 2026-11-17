@echo off
setlocal
cd /d "%~dp0\..\.."

py -3.12 --version >nul 2>&1
if not errorlevel 1 (
    py -3.12 packaging\build_app.py
) else (
    py -3.11 --version >nul 2>&1
    if errorlevel 1 (
        echo Python 3.11 or 3.12 is required. Install 64-bit Python 3.11 or 3.12, then double-click this file again.
        pause
        exit /b 1
    )
    py -3.11 packaging\build_app.py
)

if errorlevel 1 (
    echo Build failed. Review the messages above.
    pause
    exit /b 1
)

echo Build finished. The executable is in dist\QuantumCircuitBuilder\.
pause
