@echo off
title YouTube Rando Launcher
color 0a

echo [1/3] Checking Dependencies...
:: Ensures all libraries are ready
python -m pip install flask flask-cors google-api-python-client --quiet

echo [2/3] Launching Servers...

:: 1. Start the Flask Backend (Port 5000)
start "Backend API" cmd /k "python backend/app1.py"

:: 2. Start the Frontend Server (Port 8000)
:: We use 'pushd' to change directory safely and 'popd' to come back
start "Frontend Server" cmd /k "cd frontEnd && python -m http.server 8000"

echo [3/3] Opening your App...
:: Give the servers 3 seconds to fully wake up
timeout /t 3 /nobreak >nul

:: Open the browser using the HTTP address, NOT the file path
start "" "http://localhost:8000/youTubeRandomizerfull.html"

echo.
echo ====================================================
echo   ALL SYSTEMS GO! 
echo   Backend: http://localhost:5000
echo   Frontend: http://localhost:8000
echo ====================================================
pause