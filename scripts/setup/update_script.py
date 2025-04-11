import os
from pathlib import Path
from typing import List, Union

def create_update_script(
    venv_name: str,
    output_path: Union[str, Path] = "update_deps.bat",
    env_suffixes: List[str] = ["yolo", "vit", "ssd", "fast-rcc"],
    workon_home: Union[str, Path] = None
) -> bool:
    """
    Creates a batch script to update project dependencies across multiple environments.
    
    Args:
        venv_name: Base name of virtual environment
        output_path: Where to save the batch file
        env_suffixes: List of environment suffixes
        workon_home: Path to virtual environments directory
        
    Returns:
        bool: True if script was created successfully
    """
    try:
        output_path = Path(output_path).resolve()
        if workon_home:
            workon_home = Path(workon_home).resolve()
        
        print(f"Creating dependency update script at: {output_path}")

        script_content = """@echo off
setlocal enabledelayedexpansion
cd %~dp0

"""
        if workon_home:
            script_content += f'set "WORKON_HOME={workon_home}"\n\n'

        script_content += """echo ===================================
echo         ENVIRONMENT UPDATER
echo ===================================

echo Select the environment to update:
"""

        # Add environment options
        for i, suffix in enumerate(env_suffixes, 1):
            script_content += f"echo {i}. {suffix.upper()} Environment\n"
        
        # Add "All environments" option
        all_option = len(env_suffixes) + 1
        script_content += f"echo {all_option}. ALL Environments\n"
        
        # Add exit option
        exit_option = all_option + 1
        script_content += f"echo {exit_option}. Exit\n"

        # Generate choice options
        choice_options = "".join(str(i) for i in range(1, exit_option+1))
        script_content += f"""
choice /c {choice_options} /n /m "Enter your choice (1-{exit_option}): "
set CHOICE=%errorlevel%
"""

        # Individual environment update cases
        for i, suffix in enumerate(env_suffixes, 1):
            env_name = f"{venv_name}_{suffix}"
            env_path = f"%WORKON_HOME%\\{env_name}" if workon_home else env_name
            activate_path = f"{env_path}\\Scripts\\activate.bat"
            
            script_content += f"""
if %CHOICE%=={i} (
    echo.
    echo [INFO] Updating {env_name} environment...
    if exist "{activate_path}" (
        call "{activate_path}"
        echo [INFO] Upgrading pip...
        python -m pip install --upgrade pip
        echo [INFO] Upgrading setuptools...
        pip install --upgrade setuptools
        echo [INFO] Environment updated successfully.
        pause
        exit /b 0
    ) else (
        echo [ERROR] Environment {env_name} not found.
        echo [INFO] Expected location: {activate_path}
        pause
        exit /b 1
    )
)
"""

        # All environments option
        script_content += f"""
if %CHOICE%=={all_option} (
    echo.
    echo [INFO] Updating ALL environments...
    set SUCCESS=0
"""

        # Add each environment update
        for suffix in env_suffixes:
            env_name = f"{venv_name}_{suffix}"
            env_path = f"%WORKON_HOME%\\{env_name}" if workon_home else env_name
            activate_path = f"{env_path}\\Scripts\\activate.bat"
            
            script_content += f"""
    echo.
    echo [INFO] Processing {env_name}...
    if exist "{activate_path}" (
        call "{activate_path}"
        echo [INFO] Upgrading pip...
        python -m pip install --upgrade pip
        echo [INFO] Upgrading setuptools...
        pip install --upgrade setuptools
        echo [INFO] {env_name} updated successfully.
    ) else (
        echo [ERROR] Environment {env_name} not found
        set SUCCESS=1
    )
"""

        script_content += """
    if !SUCCESS!==0 (
        echo.
        echo [SUCCESS] All environments updated successfully.
    ) else (
        echo.
        echo [WARNING] Some environments could not be updated.
    )
    pause
    exit /b !SUCCESS!
)
"""

        # Exit option
        script_content += f"""
if %CHOICE%=={exit_option} (
    echo.
    echo Exiting without updates...
    exit /b 0
)

echo.
echo [ERROR] Invalid choice: %CHOICE%
pause
exit /b 1
"""

        with open(output_path, "w", newline='\r\n', encoding='ascii') as f:
            f.write(script_content)
        
        print(f"[SUCCESS] Update script created successfully at {output_path}")
        return True
        
    except Exception as e:
        print(f"[ERROR] Failed to create update script: {e}")
        return False