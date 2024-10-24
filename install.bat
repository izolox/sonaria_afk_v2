@echo off
echo Installing dependencies...
REM Check if Python is installed
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python is not installed. Please install Python and try again.
    exit /b 1
)

REM Create a virtual environment
python -m venv venv
IF %ERRORLEVEL% NEQ 0 (
    echo Failed to create virtual environment.
    exit /b 1
)

REM Activate the virtual environment
call venv\Scripts\activate

REM Install required packages
IF EXIST requirements.txt (
    pip install -r requirements.txt
    IF %ERRORLEVEL% NEQ 0 (
        echo Failed to install required packages.
        exit /b 1
    )
) ELSE (
    echo requirements.txt not found.
    exit /b 1
)

echo Installation complete.