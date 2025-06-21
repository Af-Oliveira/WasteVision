@echo off
REM -----------------------------------------------------------------------------
REM WasteVision Project - Windows Setup Script
REM This script finds a Python interpreter and runs the main setup routine.
REM It helps automate environment and directory creation for the project.
REM -----------------------------------------------------------------------------

echo Running Python setup script...

REM Try to find Python in the standard locations using 'where'
where python >nul 2>&1
if %errorlevel% equ 0 (
    echo Found Python in PATH
    python -m scripts.setup.setup
    goto end
)

REM Try to find the Python launcher 'py'
where py >nul 2>&1
if %errorlevel% equ 0 (
    echo Found Python (py launcher) in PATH
    py -m scripts.setup.setup
    goto end
)

REM If Python was not found, prompt the user for the full path to python.exe
echo Python not found in PATH. Please specify the full path to your Python executable.
set /p PYTHON_PATH="Enter full path to python.exe: "

REM Check if the provided path exists and is executable
if exist "%PYTHON_PATH%" (
    echo Running setup.py with specified Python executable...
    "%PYTHON_PATH%" -m scripts.setup.setup
    echo.
) else (
    echo Could not find Python at the specified path.
    echo Please install Python and try again, or manually edit the path in this script.
    pause
    exit /b 1
)

:end
REM -----------------------------------------------------------------------------
REM End of setup script
REM -----------------------------------------------------------------------------
