import os
import sys
from typing import Union, List, Optional
from pathlib import Path

def create_activate_script(
    venv_name: str,
    workon_home: Union[str, Path],
    env_suffixes: List[str],
    output_path: Union[str, Path] = "activate_env.sh",
    is_windows: bool = False
) -> bool:
    """
    Create an activation script for virtual environments.
    Creates .bat for Windows or .sh for Mac/Linux.
    
    Args:
        venv_name: Base name for virtual environments
        workon_home: Path to WORKON_HOME directory
        env_suffixes: List of environment suffixes
        output_path: Where to save the script
        is_windows: If True, creates a Windows batch script
        
    Returns:
        bool: True if script was created successfully
    """
    workon_home = Path(workon_home).resolve()
    output_path = Path(output_path).resolve()
    
    print(f"Creating activation script at: {output_path}")

    if is_windows:
        # Generate the batch script content
        script_content = f"""@echo off
setlocal enabledelayedexpansion
cd %~dp0

:: Set environment variables
set "WORKON_HOME={workon_home}"

echo Select the virtual environment to activate:
"""

        # Add predefined environments
        for i, suffix in enumerate(env_suffixes, 1):
            script_content += f"echo {i}. {suffix[0].upper()} Environment\n"

        # Add exit option
        exit_option = len(env_suffixes) + 1
        script_content += f"echo {exit_option}. Exit\n"

        # Generate choice options
        choice_options = "".join(str(i) for i in range(1, len(env_suffixes)+1)) + str(exit_option)
        script_content += f"""
choice /c {choice_options} /n /m "Enter your choice (1-{exit_option}): "
set "CHOICE=%errorlevel%"
"""

        # Environment activation cases
        for i, suffix in enumerate(env_suffixes, 1):
            env_name = f"{venv_name}_{suffix[0]}"
            env_path = workon_home / env_name
            activate_path = env_path / "Scripts" / "activate.bat"
            
            script_content += f"""
if "%CHOICE%"=="{i}" (
    echo Activating {env_name}...
    if exist "{activate_path}" (
        call "{activate_path}"
        echo [SUCCESS] Virtual environment {env_name} activated.
        cmd /k
        goto :EOF
    ) else (
        echo [ERROR] Environment {env_name} not found at {env_path}
        pause
        goto :EOF
    )
)
"""

        # Exit case
        script_content += f"""
if "%CHOICE%"=="{exit_option}" (
    echo Exiting...
    exit /b
)

echo Invalid choice: %CHOICE%
pause
exit /b
"""
    else:
        # Generate shell script content
        script_content = f"""#!/bin/bash
cd "$(dirname "$0")"

# Set environment variables
export WORKON_HOME="{workon_home}"

echo "Select the virtual environment to activate:"
"""

        # Add predefined environments
        for i, suffix in enumerate(env_suffixes, 1):
            script_content += f'echo "{i}. {suffix[0].upper()} Environment"\n'

        # Add exit option
        exit_option = len(env_suffixes) + 1
        script_content += f'echo "{exit_option}. Exit"\n'

        script_content += """
read -p "Enter your choice (1-{exit_option}): " choice
""".format(exit_option=exit_option)

        # Environment activation cases
        for i, suffix in enumerate(env_suffixes, 1):
            env_name = f"{venv_name}_{suffix[0]}"
            env_path = workon_home / env_name
            activate_path = env_path / "bin" / "activate"
            
            script_content += f"""
if [ "$choice" -eq {i} ]; then
    echo "Activating {env_name}..."
    if [ -f "{activate_path}" ]; then
        source "{activate_path}"
        exec bash --norc
    else
        echo "[ERROR] Environment {env_name} not found at {env_path}"
        read -p "Press enter to continue..."
        exit 1
    fi
fi
"""

        # Exit case
        script_content += f"""
if [ "$choice" -eq {exit_option} ]; then
    echo "Exiting..."
    exit 0
fi

echo "Invalid choice: $choice"
read -p "Press enter to continue..."
exit 1
"""

    try:
        with open(output_path, "w", newline='\n', encoding='utf-8') as f:
            f.write(script_content)
        
        if not is_windows:
            # Make the shell script executable
            os.chmod(output_path, 0o755)
        
        print(f"✓ Activation script created at {output_path}")
        print("\n")
        return True
    except Exception as e:
        print(f"✗ Failed to create activation script: {e}")
        print("\n")
        return False