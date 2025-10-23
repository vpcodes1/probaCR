@echo off
REM YUSEARCH - AUTOMATSKI CLOUD DEPLOYMENT (Windows)

cls

echo.
echo ============================================================
echo.
echo    YUSEARCH - AUTOMATSKI CLOUD DEPLOYMENT
echo.
echo    Ova skripta ce automatski deploy-ovati
echo    tvoju aplikaciju na cloud!
echo.
echo    Posle ovoga, dobijas URL koji dajes klijentima!
echo.
echo ============================================================
echo.

REM Proveri Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo [X] Node.js nije instaliran!
    echo Molim te instaliraj Node.js sa: https://nodejs.org/
    pause
    exit /b 1
)

echo [OK] Node.js pronadjen
echo.

REM Izbor platforme
echo Izaberi deployment platformu:
echo.
echo   1^) Railway + Vercel ^(PREPORUCENO - potpuno besplatno^)
echo   2^) Render.com ^(sve na jednom mestu^)
echo   3^) Docker
echo.

set /p choice="Izbor (1/2/3): "

if "%choice%"=="1" goto railway_vercel
if "%choice%"=="2" goto render
if "%choice%"=="3" goto docker

echo Nevazeći izbor!
pause
exit /b 1

:railway_vercel
echo.
echo ============================================================
echo   RAILWAY + VERCEL DEPLOYMENT
echo ============================================================
echo.

REM Instaliraj Railway CLI
echo [1/5] Instaliram Railway CLI...
call npm install -g @railway/cli
echo [OK] Railway CLI instaliran
echo.

REM Instaliraj Vercel CLI
echo [2/5] Instaliram Vercel CLI...
call npm install -g vercel
echo [OK] Vercel CLI instaliran
echo.

REM API ključ
echo [3/5] Konfiguracija API ključeva...
echo.
echo Trebas Anthropic API kljuc!
echo Ako nemas, registruj se ovde: https://console.anthropic.com/
echo.
set /p ANTHROPIC_KEY="Unesi Anthropic API kljuc: "
echo.

REM Backend deployment
echo [4/5] Deploy-ujem backend na Railway...
echo.
echo Otvaricu browser za Railway login...
echo Molim te uloguj se u Railway
echo.

cd backend

REM Napravi .env
(
echo ANTHROPIC_API_KEY=%ANTHROPIC_KEY%
echo SECRET_KEY=change-this-in-production-to-random-string
echo ALLOWED_ORIGINS=*
echo DATABASE_URL=sqlite+aiosqlite:///./yusearch.db
) > .env

REM Railway deploy
call railway login
call railway init
call railway up

echo.
echo [OK] Backend deploy-ovan!
echo.

cd ..

REM Frontend deployment
echo [5/5] Deploy-ujem frontend na Vercel...
echo.
echo Otvaricu browser za Vercel login...
echo Molim te uloguj se u Vercel
echo.

cd frontend

REM Vercel deploy
call vercel login
call vercel --prod

cd ..

echo.
echo ============================================================
echo   DEPLOYMENT ZAVRSEN!
echo ============================================================
echo.
echo Tvoja aplikacija je LIVE!
echo.
echo Proveri Vercel dashboard za URL: https://vercel.com/dashboard
echo Proveri Railway dashboard za backend: https://railway.app/dashboard
echo.
echo Daj Frontend URL klijentima!
echo.
pause
exit /b 0

:render
echo.
echo ============================================================
echo   RENDER.COM DEPLOYMENT
echo ============================================================
echo.
echo Za Render.com deployment:
echo.
echo 1. Idi na: https://render.com
echo 2. Klikni: New - Blueprint
echo 3. Connectuj svoj GitHub repo
echo 4. Izaberi fajl: render.yaml
echo 5. Dodaj Environment Variable:
echo    ANTHROPIC_API_KEY = tvoj-api-kljuc
echo 6. Klikni: Apply
echo.
echo Otvaricu browser...
start https://dashboard.render.com/select-repo?type=blueprint
echo.
echo Kada deployment zavri, dobijas URL!
echo.
pause
exit /b 0

:docker
echo.
echo ============================================================
echo   DOCKER DEPLOYMENT
echo ============================================================
echo.

REM Proveri Docker
docker --version >nul 2>&1
if errorlevel 1 (
    echo [X] Docker nije instaliran!
    echo Instaliraj Docker sa: https://www.docker.com/get-started
    pause
    exit /b 1
)

echo [OK] Docker pronadjen
echo.

REM API ključ
echo Konfiguracija...
echo.
set /p ANTHROPIC_KEY="Unesi Anthropic API kljuc: "
echo.

REM Napravi .env
cd backend
(
echo ANTHROPIC_API_KEY=%ANTHROPIC_KEY%
echo SECRET_KEY=change-this-in-production-to-random-string
echo ALLOWED_ORIGINS=*
echo DATABASE_URL=sqlite+aiosqlite:///./yusearch.db
) > .env
cd ..

REM Build
echo Building Docker images...
docker-compose build

echo.
echo [OK] Docker images built!
echo.
echo Za pokretanje lokalno:
echo   docker-compose up
echo.
echo Za deploy na cloud, push-uj images na Docker Hub ili koristи cloud platform.
echo.
pause
exit /b 0
