@echo off
cd %~dp0
set VENV_PATH=wastevision/wv-venv

echo Activating virtual environment...
call "%VENV_PATH%\Scripts\activate"
echo Virtual environment activated.
cmd /k
