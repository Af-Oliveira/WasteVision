@echo off
setlocal enabledelayedexpansion
cd %~dp0

:: Set environment variables
set "WORKON_HOME=C:\Users\afons\Documents\Work\PESTI\WasteVision\envs"

echo Select the virtual environment to activate:
echo 1. YOLO Environment
echo 2. VIT Environment
echo 3. SSD Environment
echo 4. FAST-RCC Environment
echo 5. Exit

choice /c 12345 /n /m "Enter your choice (1-5): "
set CHOICE=%errorlevel%

if %CHOICE%==1 (
    echo Activating wastevision/wv-venv_yolo...
    if exist "C:\Users\afons\Documents\Work\PESTI\WasteVision\envs\wastevision\wv-venv_yolo\Scripts\activate.bat" (
        call "C:\Users\afons\Documents\Work\PESTI\WasteVision\envs\wastevision\wv-venv_yolo\Scripts\activate.bat"
        echo [SUCCESS] Virtual environment wastevision/wv-venv_yolo activated.
        cmd /k
        goto :EOF
    ) else (
        echo [ERROR] Environment wastevision/wv-venv_yolo not found at C:\Users\afons\Documents\Work\PESTI\WasteVision\envs\wastevision\wv-venv_yolo
        pause
        goto :EOF
    )
)

if %CHOICE%==2 (
    echo Activating wastevision/wv-venv_vit...
    if exist "C:\Users\afons\Documents\Work\PESTI\WasteVision\envs\wastevision\wv-venv_vit\Scripts\activate.bat" (
        call "C:\Users\afons\Documents\Work\PESTI\WasteVision\envs\wastevision\wv-venv_vit\Scripts\activate.bat"
        echo [SUCCESS] Virtual environment wastevision/wv-venv_vit activated.
        cmd /k
        goto :EOF
    ) else (
        echo [ERROR] Environment wastevision/wv-venv_vit not found at C:\Users\afons\Documents\Work\PESTI\WasteVision\envs\wastevision\wv-venv_vit
        pause
        goto :EOF
    )
)

if %CHOICE%==3 (
    echo Activating wastevision/wv-venv_ssd...
    if exist "C:\Users\afons\Documents\Work\PESTI\WasteVision\envs\wastevision\wv-venv_ssd\Scripts\activate.bat" (
        call "C:\Users\afons\Documents\Work\PESTI\WasteVision\envs\wastevision\wv-venv_ssd\Scripts\activate.bat"
        echo [SUCCESS] Virtual environment wastevision/wv-venv_ssd activated.
        cmd /k
        goto :EOF
    ) else (
        echo [ERROR] Environment wastevision/wv-venv_ssd not found at C:\Users\afons\Documents\Work\PESTI\WasteVision\envs\wastevision\wv-venv_ssd
        pause
        goto :EOF
    )
)

if %CHOICE%==4 (
    echo Activating wastevision/wv-venv_fast-rcc...
    if exist "C:\Users\afons\Documents\Work\PESTI\WasteVision\envs\wastevision\wv-venv_fast-rcc\Scripts\activate.bat" (
        call "C:\Users\afons\Documents\Work\PESTI\WasteVision\envs\wastevision\wv-venv_fast-rcc\Scripts\activate.bat"
        echo [SUCCESS] Virtual environment wastevision/wv-venv_fast-rcc activated.
        cmd /k
        goto :EOF
    ) else (
        echo [ERROR] Environment wastevision/wv-venv_fast-rcc not found at C:\Users\afons\Documents\Work\PESTI\WasteVision\envs\wastevision\wv-venv_fast-rcc
        pause
        goto :EOF
    )
)

if %CHOICE%==5 (
    echo Exiting...
    exit /b
)

echo Invalid choice: %CHOICE%
pause
exit /b
