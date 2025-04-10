import os
import subprocess
import sys
from pathlib import Path

def run_command(command, shell=True):
    """Run a command and return its output."""
    result = subprocess.run(command, shell=shell, text=True, capture_output=True)
    if result.returncode != 0:
        print(f"Warning: Command '{command}' failed with error: {result.stderr}")
    return result.stdout.strip()

def check_and_install_virtualenvwrapper():
    """Check if virtualenvwrapper is installed and install it if not."""
    print("Checking if virtualenvwrapper is installed...")
    result = subprocess.run(
        [python_path, "-m", "pip", "show", "virtualenvwrapper-win"], 
        shell=True, 
        capture_output=True
    )
    
    if result.returncode != 0:
        print("virtualenvwrapper-win is not installed. Installing now...")
        subprocess.run([python_path, "-m", "pip", "install", "virtualenvwrapper-win"], shell=True)
    else:
        print("virtualenvwrapper-win is already installed.")

def create_directories():
    """Create the project directory structure."""
    print("Creating project directories...")
    directories = [
        "generate_input",
        "generate_output",
        "generate_output/models",
        "generate_output/logs",
        "training_output",
        "dataset",
        "dataset/test",
        "dataset/train",
        "dataset/valid"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

def create_virtual_environments():
    """Create the required virtual environments."""
    env_suffixes = ["yolo", "vit", "ssd", "fast-rcc"]
    
    for suffix in env_suffixes:
        env_name = f"{venv_name}_{suffix}"
        print(f"Creating virtual environment named '{env_name}'...")
        try:
            subprocess.run(f"mkvirtualenv {env_name} --python={python_path}", shell=True, check=True)
        except subprocess.CalledProcessError:
            print(f"Warning: Failed to create virtual environment '{env_name}'")

def create_activate_script():
    """Create the activate_env.bat script."""
    print("Generating activate_env.bat...")
    
    # Create empty custom_venvs.txt if it doesn't exist
    if not os.path.exists("custom_venvs.txt"):
        with open({workon_home}+"\custom_venvs.txt", "w") as f:
            pass
    
    with open("activate_env.bat", "w") as f:
        f.write(f"""@echo off
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
if exist "{workon_home}\\custom_venvs.txt" (
  for /f "tokens=*" %%i in ('type "{workon_home}\\custom_venvs.txt"') do (
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
  set VENV_PATH={venv_name}_yolo
  goto activate
)
if %CHOICE%==2 (
  set VENV_PATH={venv_name}_vit
  goto activate
)
if %CHOICE%==3 (
  set VENV_PATH={venv_name}_ssd
  goto activate
)
if %CHOICE%==4 (
  set VENV_PATH={venv_name}_fast-rcc
  goto activate
)

set INDEX=4
if exist "{workon_home}\\custom_venvs.txt" (
  for /f "tokens=*" %%j in ('type "{workon_home}\\custom_venvs.txt"') do (
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
  echo %NEW_VENV_NAME% >> "{workon_home}\\custom_venvs.txt"
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
""")

if __name__ == "__main__":
    # Get Python path from user
    default_python = sys.executable
    python_path = input(f"Enter the path to your Python executable (Press Enter for default '{default_python}'): ") or default_python
    
    # Get virtual environment name from user
    default_venv = "wastevision/wv-venv"
    venv_name = input(f"Enter the base name for your virtual environment (Press Enter for default '{default_venv}'): ") or default_venv
    
    # Set up environment variables
    current_dir = os.getcwd()
    workon_home = os.path.join(current_dir, "envs")
    os.environ["VIRTUALENVWRAPPER_PYTHON"] = python_path
    os.environ["WORKON_HOME"] = workon_home
    os.environ["VIRTUALENVWRAPPER_VIRTUALENV"] = f"{python_path} -m virtualenv"
    
    # Create workon_home directory if it doesn't exist
    if not os.path.exists(workon_home):
        os.makedirs(workon_home)
    
    # Run setup steps
    check_and_install_virtualenvwrapper()
    create_directories()
    create_virtual_environments()
    create_activate_script()
    
    # Activate the first virtual environment
    print("Activating the virtual environment...")
    os.system("call activate_env.bat")
    
    print(f"Virtual environment {venv_name} is activated. You can reactivate it in the future by running 'activate_env.bat'.")