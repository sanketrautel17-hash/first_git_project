@echo off
echo Installing frontend dependencies...
echo.
echo Note: If this fails, please close and reopen your terminal, then run:
echo   cd frontend
echo   npm install
echo.
pause

cd /d "%~dp0"
call npm install

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✓ Dependencies installed successfully!
    echo.
    echo To start the development server, run:
    echo   npm run dev
) else (
    echo.
    echo × Installation failed. Please restart your terminal and try:
    echo   npm install
)

echo.
pause
