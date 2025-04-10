@echo off
setlocal enabledelayedexpansion
cd %~dp0

echo Select the virtual environment to activate:
echo 1. YOLO Environment
echo 2. ViT Environment
echo 3. SSD Environment
echo 4. Fast R-CNN Environment

set COUNTER=4
set CHOICE_OPTIONS=1234

rem Read custom_venvs.txt and generate options dynamically
if exist "C:\Users\afons\Documents\Unv\PESTI\WasteVision\envs\custom_venvs.txt" (
  for /f "tokens=*" %%i in ('type "C:\Users\afons\Documents\Unv\PESTI\WasteVision\envs\custom_venvs.txt"') do (
    set /a COUNTER+=1
    echo !COUNTER!. Custom Environment: %%i
    set CHOICE_OPTIONS=!CHOICE_OPTIONS!!COUNTER!
  )
)

set /a ADD_CUSTOM_OPTION=COUNTER+1
set /a EXIT_OPTION=COUNTER+2
echo !ADD_CUSTOM_OPTION!. Add Custom Venv
echo !EXIT_OPTION!. Exit
set CHOICE_OPTIONS=!CHOICE_OPTIONS!!ADD_CUSTOM_OPTION!!EXIT_OPTION!

choice /c !CHOICE_OPTIONS!AB /n /m "Enter your choice: (1-!EXIT_OPTION!, !ADD_CUSTOM_OPTION! for Add, !EXIT_OPTION! for Exit)"
set CHOICE=%errorlevel%

if %CHOICE%==1 (
  set VENV_PATH=wastevision/wv-venv_yolo
  goto activate
)
if %CHOICE%==2 (
  set VENV_PATH=wastevision/wv-venv_vit
  goto activate
)
if %CHOICE%==3 (
  set VENV_PATH=wastevision/wv-venv_ssd
  goto activate
)
if %CHOICE%==4 (
  set VENV_PATH=wastevision/wv-venv_fast-rcc
  goto activate
)

set INDEX=4
if exist "C:\Users\afons\Documents\Unv\PESTI\WasteVision\envs\custom_venvs.txt" (
  for /f "tokens=*" %%j in ('type "C:\Users\afons\Documents\Unv\PESTI\WasteVision\envs\custom_venvs.txt"') do (
    set /a INDEX+=1
    if %CHOICE%==!INDEX! (
      set VENV_PATH=%%j
      goto activate
    )
  )
)

if %CHOICE%==!ADD_CUSTOM_OPTION! (
  set /p VENV_PATH="Enter the custom path to the virtual environment: "
  set /p NEW_VENV_NAME="Enter a name for the environment: "
  if not defined NEW_VENV_NAME set NEW_VENV_NAME=%VENV_PATH%
  echo %NEW_VENV_NAME% >> "C:\Users\afons\Documents\Unv\PESTI\WasteVision\envs\custom_venvs.txt"
  set VENV_PATH=%NEW_VENV_NAME%
  goto activate
)
if %CHOICE%==!EXIT_OPTION! (
  echo Exiting...
  exit /b
)

:activate
echo Activating virtual environment %VENV_PATH%...
call workon %VENV_PATH%
echo Virtual environment activated.
cmd /k
