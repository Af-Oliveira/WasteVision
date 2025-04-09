@echo off
setlocal

:: Use the virtual environment's pip directly
set VENV_NAME=wastevision/wv-venv
echo Updating dependencies from requirements.txt...
call "%~dp0%VENV_NAME%\Scripts\pip" install -r requirements.txt --upgrade

echo Dependencies updated successfully.
endlocal
