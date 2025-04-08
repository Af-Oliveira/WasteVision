@echo off
setlocal

:: Prompt for Python path with a default value
set PYTHON_PATH=python
set /p PYTHON_PATH="Enter the path to your Python executable (Press Enter for default 'python'): "

:: Prompt for virtual environment name with default 'ultralytics/ultralytics-venv'
set VENV_NAME=wastevision/wv-venv
set /p VENV_NAME="Enter the name for your virtual environment (Press Enter for default 'wastevision/wv-venv'): "

:: Create the virtual environment
echo Creating virtual environment named %VENV_NAME%...
"%PYTHON_PATH%" -m venv %VENV_NAME%

:: Create directories
echo Creating project directories...
:: Directory for input files used in generation process
mkdir generate_input
:: Directory for output files from generation process
mkdir generate_output
:: Directory to store trained models
mkdir models
:: Directory for training logs and output files
mkdir training_output
:: Main dataset directory
mkdir dataset
:: Test dataset split 
mkdir dataset\test
:: Training dataset split 
mkdir dataset\train
:: Validation dataset split 
mkdir dataset\valid

:: Generate the activate_env.bat file
echo Generating activate_env.bat...
(
echo @echo off
echo cd %%~dp0
echo set VENV_PATH=%VENV_NAME%
echo.
echo echo Activating virtual environment...
echo call "%%VENV_PATH%%\Scripts\activate"
echo echo Virtual environment activated.
echo cmd /k
) > activate_env.bat

echo Setup complete. Use 'activate_env.bat' to activate the virtual environment.

:: Call activate_env.bat to activate the virtual environment
echo Activating the virtual environment...
call activate_env.bat

echo Virtual environment %VENV_NAME% is activated. You can reactivate it in the future by running 'activate_env.bat'.
endlocal