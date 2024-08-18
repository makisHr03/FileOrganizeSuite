@echo off
:: Check if the script is running with admin privileges
:: Use 'net session' to check for administrative privileges
net session >nul 2>&1
if %errorlevel% neq 0 (
    :: Inform the user that the script is not running with admin privileges
    echo The script is not running with administrator privileges!
    set /p "choice=Do you want to run this script with administrative privileges to uninstall AppSync? (y/n): "
    goto admin_access


:admin_access
    :: Check user's choice to rerun with admin privileges
    if /i "%choice%" equ "y" (
        :: Create a VBScript to request admin privileges
        echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
        echo UAC.ShellExecute "cmd.exe", "/c ""%~s0"" %*", "", "runas", 1 >> "%temp%\getadmin.vbs"
        
        :: Execute the VBScript and delete it
        "%temp%\getadmin.vbs"
        del "%temp%\getadmin.vbs"
        exit /b
    ) else (
        echo If you want to uninstall AppSync, please run the script as administrator!
        pause
        exit /b
    )
)

goto options


:options
:: Display menu options
echo 1. Install
echo 2. Uninstall
echo 3. Exit
set /p "choice_menu=Choose an option (1 or 3): "
goto menu

:menu
:: Handle user menu choice
if "%choice_menu%"=="1" goto install
if "%choice_menu%"=="2" goto uninstall
if "%choice_menu%"=="3" goto exit_menu
echo Invalid choice. Please choose 1 or 3.
goto options

:install
:: Define variables
SET "mypath=%~dp0"
set "runner=%mypath%source_code\Runner.bat"
set "icon_file=%mypath%source_code\icon.ico"
set "source_file=%mypath%source_code\FileOrganizeSuite.py"
set "source_shortcut=%mypath%source_code\FileOrganizeSuite.lnk"
set "destination_dir=C:\Program Files (x86)\FileOrganizeSuite"
set "start_menu_dir=C:\ProgramData\Microsoft\Windows\Start Menu\Programs"

:: Create destination directory if it does not exist
if not exist "%destination_dir%" (
    mkdir "%destination_dir%"
)

:: Copy the Python file

copy "%source_file%" "%destination_dir%"
if errorlevel 1 (
    echo Error_1
    echo Oops! Something went wrong. Please help us improve by reporting this issue on GitHub: https://github.com/makisHr03/FileOrganizeSuite/issues
    pause
    exit /b
)

copy "%runner%" "%destination_dir%"
if errorlevel 1 (
    echo Error_2
    echo Oops! Something went wrong. Please help us improve by reporting this issue on GitHub: https://github.com/makisHr03/FileOrganizeSuite/issues
    pause
    exit /b
)

:: Copy the shortcut
copy "%source_shortcut%" "%start_menu_dir%"
if errorlevel 1 (
    echo Error_3
    echo Oops! Something went wrong. Please help us improve by reporting this issue on GitHub: https://github.com/makisHr03/FileOrganizeSuite/issues
    pause
    exit /b
)

copy "%icon_file%" "%destination_dir%"
if errorlevel 1 (
    echo Error_4
    echo Oops! Something went wrong. Please help us improve by reporting this issue on GitHub: https://github.com/makisHr03/FileOrganizeSuite/issues
    pause
    exit /b
)

cls
echo Program has been installed successfully.
pause
exit /b

:uninstall
:: Define variables
SET "mypath=%~dp0"
set "source_file=%mypath%FileOrganizeSuite.py"
set "source_shortcut=%mypath%FileOrganizeSuite.lnk"
set "destination_dir=C:\Program Files (x86)\FileOrganizeSuite"
set "start_menu_dir=C:\ProgramData\Microsoft\Windows\Start Menu\Programs"

:: Remove the installed files
rd /s /q "%destination_dir%"
if errorlevel 1 (
    cls
    echo Error_5
    echo Oops! Something went wrong. Please help us improve by reporting this issue on GitHub: https://github.com/makisHr03/FileOrganizeSuite/issues
    pause
    exit /b
)

del "%start_menu_dir%\FileOrganizeSuite.lnk"
if errorlevel 1 (
    cls
    echo Error_6
    echo Oops! Something went wrong. Please help us improve by reporting this issue on GitHub: https://github.com/makisHr03/FileOrganizeSuite/issues
    pause
    exit /b
)


cls
echo Program has been uninstalled successfully.
pause
exit /b


:exit_menu
    exit /b
