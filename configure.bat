@echo off
REM YUSEARCH - API Key Configuration Helper for Windows

echo ================================================
echo   YUSEARCH - API Key Configuration
echo ================================================
echo.

cd backend

REM Check if .env exists
if not exist .env (
    echo Creating .env file...
    copy .env.example .env
)

echo To use YUSEARCH, you need an Anthropic API key.
echo.
echo How to get your FREE Anthropic API key:
echo    1. Visit: https://console.anthropic.com/
echo    2. Sign up for a free account
echo    3. Go to 'API Keys' section
echo    4. Click 'Create Key'
echo    5. Copy the key
echo.
echo Opening Anthropic Console in your browser...
echo.

start https://console.anthropic.com/settings/keys

echo.
pause
echo.

REM Get Anthropic API key
echo Enter your Anthropic API key:
set /p anthropic_key="Key: "

REM Update .env file using PowerShell
if not "%anthropic_key%"=="" (
    powershell -Command "(Get-Content .env) -replace 'ANTHROPIC_API_KEY=.*', 'ANTHROPIC_API_KEY=%anthropic_key%' | Set-Content .env"
    echo [OK] Anthropic API key saved!
) else (
    echo [!] No key entered, skipping...
)

echo.
echo ================================================
echo.

REM Ask about Serper API
echo Optional: Add Serper API key for better Google search
echo.
echo How to get FREE Serper API key ^(optional but recommended^):
echo    1. Visit: https://serper.dev/
echo    2. Sign up ^(2,500 free searches/month^)
echo    3. Copy your API key
echo.

set /p add_serper="Do you want to add Serper API key? (y/n): "

if /i "%add_serper%"=="y" (
    start https://serper.dev/

    echo.
    echo Enter your Serper API key:
    set /p serper_key="Key: "

    if not "!serper_key!"=="" (
        powershell -Command "(Get-Content .env) -replace 'SERPER_API_KEY=.*', 'SERPER_API_KEY=!serper_key!' | Set-Content .env"
        echo [OK] Serper API key saved!
    )
) else (
    echo [i] Skipping Serper API key ^(you can add it later^)
)

cd ..

echo.
echo ================================================
echo   Configuration Complete!
echo ================================================
echo.
echo Your API keys are saved in: backend\.env
echo.
echo Next steps:
echo   1. Run: start.bat
echo   2. Open: http://localhost:5173
echo   3. Generate your first report!
echo.

pause
