@echo off
echo Stopping SupoClip services...

REM Kill Node / Frontend
taskkill /f /im node.exe >nul 2>&1

REM Kill Python / Backend / Worker
taskkill /f /im uvicorn.exe >nul 2>&1
taskkill /f /im arq.exe >nul 2>&1

REM Kill Redis
taskkill /f /im redis-server.exe >nul 2>&1

REM Stop PostgreSQL service
net stop supoclip_pgsql >nul 2>&1

echo All SupoClip services stopped.
pause
