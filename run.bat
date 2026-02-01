@echo off
REM Universal File Converter - Start Script for Windows

echo Starting Universal File Converter...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

echo Python found
python --version

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -q -r requirements.txt

REM Create necessary directories
if not exist "uploads\" mkdir uploads
if not exist "converted\" mkdir converted

REM Start the application
echo.
echo Starting Flask application...
echo Open your browser and navigate to: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.

python app.py
