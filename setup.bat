@echo off
echo Running Python setup script...

:: Try to find Python in the standard locations
where python >nul 2>&1
if %errorlevel% equ 0 (
    python setup.py
    goto end
)

where py >nul 2>&1
if %errorlevel% equ 0 (
    py setup.py
    goto end
)

echo Python not found in PATH. Please specify the full path to your Python executable.
set /p PYTHON_PATH="Enter full path to python.exe: "

if exist "%PYTHON_PATH%" (
    "%PYTHON_PATH%" setup.py
) else (
    echo Could not find Python at the specified path.
    echo Please install Python and try again, or manually edit the path in this script.
    pause
)

:end
echo Setup completed.
pause