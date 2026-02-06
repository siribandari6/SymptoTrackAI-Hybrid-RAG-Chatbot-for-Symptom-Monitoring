@echo off
cd /d "%~dp0"..\..\
echo ========================================
echo SymptoTrackAI - Setup and Run
echo ========================================
echo.

REM Activate the virtual environment using UV
echo [1/3] Activating virtual environment (UV with Python 3.8.10)...
if exist my-project\Scripts\activate.bat (
    call my-project\Scripts\activate.bat
    echo Virtual environment activated successfully!
) else (
    echo ERROR: Virtual environment not found!
    echo Creating virtual environment using UV with Python 3.8.10...
    uv venv my-project --python 3.8.10
    if %errorlevel% neq 0 (
        echo ERROR: Failed to create virtual environment!
        echo Please ensure UV is installed and Python 3.8.10 is available
        pause
        exit /b 1
    )
    call my-project\Scripts\activate.bat
    echo Virtual environment created and activated!
)
echo.

REM Install requirements using UV
echo [2/3] Installing dependencies from requirements.txt using UV...
if exist requirements.txt (
    uv pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo ERROR: Failed to install requirements!
        pause
        exit /b 1
    )
    echo Dependencies installed successfully!
) else (
    echo WARNING: requirements.txt not found, skipping installation...
)
echo.

REM Run the Django server
echo [3/3] Starting Django development server...
echo.
python manage.py runserver --noreload

REM Keep window open on exit
pause
