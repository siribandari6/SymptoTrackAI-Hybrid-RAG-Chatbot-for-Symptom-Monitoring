@echo off
cd /d "%~dp0"..\..\
echo ========================================
echo SymptoTrackAI - Docker Setup
echo ========================================
echo.

echo Building and starting Docker containers...
echo.

docker-compose up --build -d

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Failed to start Docker containers!
    echo Please ensure Docker Desktop is running.
    pause
    exit /b 1
)

echo.
echo ========================================
echo Docker containers started successfully!
echo ========================================
echo.
echo - Application URL: http://localhost:8000
echo - To view logs: docker-compose logs -f
echo - To stop: docker-compose down
echo.
echo Opening application in browser...
timeout /t 3 /nobreak > nul
start http://localhost:8000

pause
