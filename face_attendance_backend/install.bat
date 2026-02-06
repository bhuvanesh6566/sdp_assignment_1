@echo off
title Installing Face Attendance Dependencies
color 0B

cd /d "%~dp0"

echo ============================================
echo   Installing Face Attendance Dependencies
echo ============================================
echo.
echo This will install:
echo   - Flask and Flask-SQLAlchemy
echo   - PyMySQL (MySQL connector)
echo   - face-recognition library
echo   - numpy and dlib
echo.
echo This may take 5-10 minutes...
echo.

pause

REM Check Python
where py >nul 2>nul
if %errorlevel% equ 0 (
    set PYTHON_CMD=py
) else (
    where python >nul 2>nul
    if %errorlevel% equ 0 (
        set PYTHON_CMD=python
    ) else (
        echo ERROR: Python is not installed or not in PATH
        echo Please install Python 3.8+ first
        pause
        exit /b 1
    )
)

echo Using: %PYTHON_CMD%
echo.

echo [1/3] Upgrading pip...
%PYTHON_CMD% -m pip install --upgrade pip
echo.

echo [2/3] Installing dependencies...
%PYTHON_CMD% -m pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Installation failed!
    echo.
    echo Common issues:
    echo   - On Windows, you may need Visual C++ Build Tools for dlib
    echo   - Try: pip install cmake
    echo   - Then run this script again
    echo.
    pause
    exit /b 1
)

echo.
echo [3/3] Verifying installation...
%PYTHON_CMD% -c "import flask; import face_recognition; print('✓ All packages installed successfully!')"

if %errorlevel% equ 0 (
    echo.
    echo ============================================
    echo   Installation Complete!
    echo ============================================
    echo.
    echo Next steps:
    echo   1. Update MySQL password in setup_database.py
    echo   2. Run: python setup_database.py
    echo   3. Update config.py with MySQL credentials
    echo   4. Run: python check_config.py
    echo   5. Start backend: python app.py
    echo.
) else (
    echo.
    echo WARNING: Some packages may not be installed correctly
    echo Check the error messages above
    echo.
)

pause
