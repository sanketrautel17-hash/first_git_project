@echo off
echo Starting UserHub Frontend...
echo.
echo Make sure your backend is running on http://127.0.0.1:8000
echo.

cd /d "%~dp0"

if not exist "node_modules" (
    echo × node_modules not found!
    echo Please run install.bat first or execute: npm install
    echo.
    pause
    exit /b 1
)

call npm run dev

pause
