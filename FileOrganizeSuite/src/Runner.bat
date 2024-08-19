@echo off

:: Set the directory of the batch file as the working directory
SET "mypath=%~dp0"

:: Set the path to your Python script
SET "python_script=%mypath%FileOrganizeSuite.py"

:: Try running with 'python'
python "%python_script%"
IF ERRORLEVEL 9009 (
    cls
    :: If 'python' fails (error code 9009 means 'command not found'), try running with 'py'
    py "%python_script%"
    IF ERRORLEVEL 9009 (
        cls
        echo Error_7
        echo Oops! Something went wrong. Please help us improve by reporting this issue on GitHub: https://github.com/makisHr03/FileOrganizeSuite/issues
        pause
        exit /b 1
    )
)
