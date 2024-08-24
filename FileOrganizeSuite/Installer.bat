@echo off
:: Check if the script is running with admin privileges
net session >nul 2>&1
if %errorlevel% neq 0 (
    :: Inform the user that the script is not running with admin privileges
    echo The script is not running with administrator privileges!
    set /p "choice=Do you want to run this script with administrative privileges to manage FileOrganizeSuite? (y/n): "
    goto check_admin_access
)

goto options

:check_admin_access
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
        echo If you want to uninstall FileOrganizeSuite, please run the script as administrator!
        pause
        exit /b
    )
)

:options
:: Display menu options
echo 1. Install
echo 2. Uninstall
echo 3. Exit
set /p "choice_menu=Choose an option (1, 2, or 3): "
goto menu

:menu
:: Handle user menu choice
if "%choice_menu%"=="1" goto install
if "%choice_menu%"=="2" goto uninstall
if "%choice_menu%"=="3" goto exit_menu
echo Invalid choice. Please choose 1, 2, or 3.
pause
cls
goto options

:install
:: Define variables
SET "mypath=%~dp0"
set "runner_path=%mypath%src\Runner.bat"
set "upgrader_path=%mypath%src\Upgrader.py"
set "icon_file_path=%mypath%src\icon.ico"
set "python_file_path=%mypath%src\FileOrganizeSuite.py"
set "destination_path=C:\Program Files (x86)\FileOrganizeSuite"
set "shortcut_path=C:\ProgramData\Microsoft\Windows\Start Menu\Programs\FileOrganizeSuite.lnk"
set "target_path_shortcut=%destination_path%\Runner.bat"
set "shortcut_name=FileOrganizeSuite"
set "icon_path=%destination_path%\icon.ico"

:: Create destination directory if it does not exist
if not exist "%destination_path%" (
    mkdir "%destination_path%"
)

:: Copy the files
copy "%python_file_path%" "%destination_path%"
if errorlevel 1 (
    echo Error_1
    echo Oops! Something went wrong. Please help us improve by reporting this issue on GitHub: https://github.com/makisHr03/FileOrganizeSuite/issues
    pause
    exit /b
)

copy "%runner_path%" "%destination_path%"
if errorlevel 1 (
    echo Error_2
    echo Oops! Something went wrong. Please help us improve by reporting this issue on GitHub: https://github.com/makisHr03/FileOrganizeSuite/issues
    pause
    exit /b
)

copy "%upgrader_path%" "%destination_path%"
if errorlevel 1 (
    echo Error_3
    echo Oops! Something went wrong. Please help us improve by reporting this issue on GitHub: https://github.com/makisHr03/FileOrganizeSuite/issues
    pause
    exit /b
)

copy "%icon_file_path%" "%destination_path%"
if errorlevel 1 (
    echo Error_4
    echo Oops! Something went wrong. Please help us improve by reporting this issue on GitHub: https://github.com/makisHr03/FileOrganizeSuite/issues
    pause
    exit /b
)

:: Create a shortcut
echo Set oWS = WScript.CreateObject("WScript.Shell") > temp_create_shortcut.vbs
echo sLinkFile = "%shortcut_path%" >> temp_create_shortcut.vbs
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> temp_create_shortcut.vbs
echo oLink.TargetPath = "%target_path_shortcut%" >> temp_create_shortcut.vbs
echo oLink.IconLocation = "%icon_path%" >> temp_create_shortcut.vbs
echo oLink.Save >> temp_create_shortcut.vbs

cscript //nologo temp_create_shortcut.vbs
del temp_create_shortcut.vbs

if not exist "%shortcut_path%" (
    echo Error_5
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
set "destination_path=C:\Program Files (x86)\FileOrganizeSuite"
set "start_menu_path=C:\ProgramData\Microsoft\Windows\Start Menu\Programs"

:: Remove the installed files
rd /s /q "%destination_path%"
if errorlevel 1 (
    cls
    echo Error_6
    echo Oops! Something went wrong. Please help us improve by reporting this issue on GitHub: https://github.com/makisHr03/FileOrganizeSuite/issues
    pause
    exit /b
)

del "%start_menu_path%\FileOrganizeSuite.lnk"
if errorlevel 1 (
    cls
    echo Error_7
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
