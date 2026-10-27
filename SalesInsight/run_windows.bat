@echo off
setlocal
cd /d "%~dp0"
echo.
echo ==========================================
echo   SalesInsight - Local Dashboard Launcher
echo ==========================================
echo.
where python >nul 2>nul
if errorlevel 1 (
    echo ERROR: Python was not found.
    echo Install Python 3.10 or newer from https://www.python.org/downloads/
    echo During installation, tick "Add python.exe to PATH".
    pause
    exit /b 1
)
python --version
if not exist ".venv\Scripts\python.exe" (
    echo Creating virtual environment...
    python -m venv .venv
    if errorlevel 1 (
        echo ERROR: Could not create the virtual environment.
        echo Check your Python installation and permissions.
        pause
        exit /b 1
    )
)
echo Installing or checking dependencies...
".venv\Scripts\python.exe" -m pip install --upgrade pip
if errorlevel 1 (
    echo ERROR: pip upgrade failed. Check your internet connection.
    pause
    exit /b 1
)
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Requirements installation failed.
    echo Check your internet connection, then run this file again.
    pause
    exit /b 1
)
echo Starting SalesInsight. Keep this window open while using the dashboard.
".venv\Scripts\python.exe" -m streamlit run app.py
if errorlevel 1 (
    echo The app stopped with an error. Review the message above.
    pause
    exit /b 1
)
endlocal
