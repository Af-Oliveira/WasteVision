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

:: Generate the update_deps.bat file
echo Generating update_deps.bat...
(
echo @echo off
echo setlocal
echo.
echo :: Use the virtual environment's pip directly
echo set VENV_NAME=%VENV_NAME%
echo echo Updating dependencies from requirements.txt...
echo call "%%~dp0%%VENV_NAME%%\Scripts\pip" install -r requirements.txt --upgrade
echo.
echo echo Dependencies updated successfully.
echo endlocal
) > update_deps.bat

:: Generate the clean.bat file
echo Generating clean.bat...
(
echo @echo off
echo setlocal
echo.
echo echo This will clean temporary files and cached data.
echo set /p CONFIRM="Are you sure you want to continue? ^(y/n^): "
echo.
echo if /i "%%CONFIRM%%"=="y" ^(
echo     echo Cleaning project directories...
echo.    
echo     :: Clean Python cache files
echo     del /s /q *.pyc
echo     rmdir /s /q __pycache__ 2^>nul
echo.    
echo     :: Clean output directories but leave the folders
echo     del /s /q generate_output\*
echo     del /s /q training_output\*
echo.    
echo     echo Cleanup complete.
echo ^) else ^(
echo     echo Cleanup cancelled.
echo ^)
echo.
echo endlocal
) > clean.bat

echo Setup complete. Additional utility scripts created: update_deps.bat and clean.bat

:: Install dependencies from requirements.txt
echo Installing dependencies from requirements.txt...
call "%VENV_NAME%\Scripts\activate" && pip install -r requirements.txt
echo Dependencies installed successfully.

:: Call activate_env.bat to activate the virtual environment
echo Activating the virtual environment...
call activate_env.bat

echo Virtual environment %VENV_NAME% is activated. You can reactivate it in the future by running 'activate_env.bat'.
endlocal