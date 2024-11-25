@echo off
REM Detect the current directory of this script
set "CURRENT_DIR=%~dp0"

REM Change to the script directory
cd /d "%CURRENT_DIR%"

REM Check if nginx.exe exists
if exist nginx.exe (
    echo Found nginx.exe in %CURRENT_DIR%
    
    REM Check if Nginx is already running
    tasklist /FI "IMAGENAME eq nginx.exe" | find /I "nginx.exe" >nul
    if %ERRORLEVEL% equ 0 (
        echo Nginx is already running.
        REM Reload Nginx configuration
        nginx.exe -s reload
        echo Nginx configuration reloaded successfully.
    ) else (
        echo Nginx is not running.
        REM Start Nginx
        start nginx.exe
        echo Starting Nginx...
        
        REM Wait for a short moment to ensure Nginx starts properly
        timeout /t 2 >nul
    )
) else (
    echo Error: nginx.exe not found in %CURRENT_DIR%.
    echo Please ensure the script is placed in the Nginx directory.
    pause
    exit /b 1
)

REM Indicate the script has finished
echo Script completed.
pause
