@echo off
echo Starting SupoClip Local Stack...

REM 1. Start PostgreSQL Service
echo Starting PostgreSQL...
net start supoclip_pgsql >nul 2>&1

REM 2. Start Redis (if not running)
echo Starting Redis...
tasklist /fi "imagename eq redis-server.exe" | findstr /i "redis-server.exe" >nul
if %errorlevel% neq 0 (
    start "SupoClip Redis" /min "C:\Users\Administrator\.gemini\antigravity\scratch\tools\redis\redis-server.exe" "C:\Users\Administrator\.gemini\antigravity\scratch\tools\redis\redis.windows.conf"
)

REM 3. Set PATH and PYTHONPATH
set "PATH=%PATH%;C:\Users\Administrator\.gemini\antigravity\bin"
set "PYTHONPATH=src;."

REM 4. Start Backend API
echo Starting Backend API (Port 8000)...
cd /d "C:\Users\Administrator\.gemini\antigravity\scratch\supoclip\backend"
start "SupoClip Backend" cmd /k ".venv\Scripts\python.exe -m uvicorn src.main:app --host 127.0.0.1 --port 8000"

REM 5. Start Worker
echo Starting ARQ Worker...
start "SupoClip Worker" cmd /k ".venv\Scripts\arq.exe src.workers.tasks.WorkerSettings"

REM 6. Start Frontend
echo Starting Frontend (Port 3107)...
cd /d "C:\Users\Administrator\.gemini\antigravity\scratch\supoclip\frontend"
start "SupoClip Frontend" cmd /k "pnpm run dev"

echo.
echo ======================================================
echo SupoClip is running!
echo Frontend UI:  http://localhost:3107
echo Backend Docs: http://127.0.0.1:8000/docs
echo ======================================================
pause
