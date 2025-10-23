@echo off
REM YUSEARCH - Automated Setup Script for Windows
REM This script automatically sets up the entire application

echo ================================================
echo   YUSEARCH - Automated Setup
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python 3 is not installed
    echo Please install Python 3.11+ from https://www.python.org/
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo Error: Node.js is not installed
    echo Please install Node.js 18+ from https://nodejs.org/
    exit /b 1
)

echo [OK] Python and Node.js found
echo.

REM Step 1: Setup Backend
echo [1/4] Setting up Backend...
cd backend

echo   Creating Python virtual environment...
python -m venv venv

echo   Activating virtual environment...
call venv\Scripts\activate.bat

echo   Installing Python dependencies...
pip install -q --upgrade pip
pip install -q -r requirements.txt

echo [OK] Backend dependencies installed
echo.

REM Step 2: Configure Environment
echo [2/4] Configuring Environment...

if not exist .env (
    copy .env.example .env
    echo.
    echo IMPORTANT: You need to add your API keys to backend\.env
    echo.
    echo Required:
    echo - ANTHROPIC_API_KEY ^(get free at https://console.anthropic.com/^)
    echo.
    echo Optional:
    echo - SERPER_API_KEY ^(get free at https://serper.dev/^)
    echo.

    notepad .env
) else (
    echo [OK] .env file already exists
)

cd ..
echo.

REM Step 3: Setup Frontend
echo [3/4] Setting up Frontend...
cd frontend

echo   Installing Node.js dependencies...
call npm install --silent

echo [OK] Frontend dependencies installed
echo.

cd ..

REM Step 4: Create start script
echo [4/4] Creating start scripts...

REM Create start script
(
echo @echo off
echo echo Starting YUSEARCH...
echo echo.
echo.
echo echo Starting backend on http://localhost:8000
echo start "YUSEARCH Backend" cmd /k "cd backend && venv\Scripts\activate && uvicorn app.main:app --host 0.0.0.0 --port 8000"
echo.
echo timeout /t 3 /nobreak ^>nul
echo.
echo echo Starting frontend on http://localhost:5173
echo start "YUSEARCH Frontend" cmd /k "cd frontend && npm run dev"
echo.
echo echo ================================================
echo echo   YUSEARCH is running!
echo echo ================================================
echo echo.
echo echo   Frontend: http://localhost:5173
echo echo   Backend:  http://localhost:8000
echo echo   API Docs: http://localhost:8000/docs
echo echo.
echo echo Close the terminal windows to stop services
echo echo.
) > start.bat

REM Create stop script
(
echo @echo off
echo echo Stopping YUSEARCH...
echo taskkill /FI "WINDOWTITLE eq YUSEARCH Backend*" /F ^>nul 2^>^&1
echo taskkill /FI "WINDOWTITLE eq YUSEARCH Frontend*" /F ^>nul 2^>^&1
echo echo YUSEARCH stopped
) > stop.bat

echo [OK] Start scripts created
echo.

REM Setup complete
echo ================================================
echo   Setup Complete!
echo ================================================
echo.
echo To start YUSEARCH:
echo   start.bat
echo.
echo To stop YUSEARCH:
echo   stop.bat
echo.
echo Or use Docker:
echo   docker-compose up
echo.
echo Don't forget to add your API keys to backend\.env!
echo.

pause
