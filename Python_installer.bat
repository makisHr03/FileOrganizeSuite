@echo off
setlocal

:: Check if Python is installed
python --version >nul 2>&1

if %errorlevel% neq 0 (
    py --version >nul 2>&1
)


:: If Python is not installed, errorlevel will be set to 1
if %errorlevel% neq 0 (
    echo Python is not installed.
    set /p install="Do you want to install Python? (y/n): "
    goto install_python
) else (
    echo Python is already installed.
    pause
    exit /b
)

:install_python
if /i "%install%"=="yes" (
    echo Installing Python...
    winget install Python.Python.3.12
    if %errorlevel% neq 0 (
        echo Error_8
        echo Failed to install Python. Please install it manually from: https://www.python.org/downloads/
        pause
        exit /b 1
    ) else (
        echo Python has been installed successfully.
    )
) else if /i "%install%"=="y" (
    echo Installing Python...
    winget install Python.Python.3.12
    if %errorlevel% neq 0 (
        echo Error_8
        echo Failed to install Python. Please install it manually from: https://www.python.org/downloads/
        pause
        exit /b 1
    ) else (
        echo Python has been installed successfully.
    )
) else (
    echo Python installation aborted by the user.
    pause
    exit /b 1
)

:: End script
pause
