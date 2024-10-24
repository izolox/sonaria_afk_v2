@echo off
IF NOT EXIST venv\Scripts\activate.bat (
    call install.bat
    IF %ERRORLEVEL% NEQ 0 (
        echo Failed to install dependencies.
        exit /b 1
    )
)
call venv\Scripts\activate
python main.py
pause