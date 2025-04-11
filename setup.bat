@echo off
echo Running Python setup script...

:: Try to find Python in the standard locations
where python >nul 2>&1
if %errorlevel% equ 0 (
    echo Found Python
    python -m scripts.setup.setup
    goto end
)

where py >nul 2>&1
if %errorlevel% equ 0 (
    echo Found Python (py launcher) 
    py -m scripts.setup.setup
    goto end
)

echo Python not found . Please specify the full path to your Python executable.
set /p PYTHON_PATH="Enter full path to python.exe: "

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
echo Setup completed.
pause