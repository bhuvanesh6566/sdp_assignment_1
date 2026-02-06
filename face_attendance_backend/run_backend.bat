@echo off
title Face Attendance Backend
color 0A

cd /d "%~dp0"

echo ============================================
echo   Face Attendance Backend Server
echo   http://localhost:5000
echo ============================================
echo.

REM Check if Python is available
where py >nul 2>nul
if %errorlevel% equ 0 (
    set PYTHON_CMD=py
) else (
    where python >nul 2>nul
    if %errorlevel% equ 0 (
        set PYTHON_CMD=python
    ) else (
        echo ERROR: Python is not installed or not in PATH
        echo Please install Python 3.8+ and try again
        pause
        exit /b 1
    )
)

echo Using: %PYTHON_CMD%
echo.

REM Optional: Check config before starting
echo Checking configuration...
%PYTHON_CMD% check_config.py
if %errorlevel% neq 0 (
    echo.
    echo WARNING: Configuration check failed!
    echo You may need to:
    echo   1. Run setup_database.py to create the database
    echo   2. Update config.py with correct MySQL credentials
    echo.
    pause
)

echo.
echo Starting Flask backend...
echo Press Ctrl+C to stop the server
echo.

%PYTHON_CMD% app.py

if %errorlevel% neq 0 (
    echo.
    echo Backend stopped with an error.
    echo Check the error messages above.
    pause
)
