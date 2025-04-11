import os
import sys
from typing import Union, List, Optional
from pathlib import Path

def create_activate_script(
    venv_name: str,
    workon_home: Union[str, Path],
    env_suffixes: List[str] = ["yolo", "vit", "ssd", "fast-rcc"],
    output_path: Union[str, Path] = "activate_env.bat"
) -> bool:
    """
    Create a Windows batch script for activating virtual environments
    using the same approach as create_virtual_environments.
    
    Args:
        venv_name: Base name for virtual environments
        workon_home: Path to WORKON_HOME directory
        env_suffixes: List of environment suffixes
        output_path: Where to save the script
        
    Returns:
        bool: True if script was created successfully
    """
    workon_home = Path(workon_home).resolve()
    output_path = Path(output_path).resolve()
    
    print(f"\nGenerating activation script: {output_path}")

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
        script_content += f"echo {i}. {suffix.upper()} Environment\n"

    # Add exit option
    exit_option = len(env_suffixes) + 1
    script_content += f"echo {exit_option}. Exit\n"

    # Generate choice options
    choice_options = "".join(str(i) for i in range(1, len(env_suffixes)+1)) + str(exit_option)
    script_content += f"""
choice /c {choice_options} /n /m "Enter your choice (1-{exit_option}): "
set CHOICE=%errorlevel%
"""

    # Environment activation cases - directly using paths similar to create_virtual_environments
    for i, suffix in enumerate(env_suffixes, 1):
        env_name = f"{venv_name}_{suffix}"
        env_path = workon_home / env_name
        activate_path = env_path / "Scripts" / "activate.bat"
        
        script_content += f"""
if %CHOICE%=={i} (
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
if %CHOICE%=={exit_option} (
    echo Exiting...
    exit /b
)

echo Invalid choice: %CHOICE%
pause
exit /b
"""

    try:
        with open(output_path, "w", newline='\r\n', encoding='ascii') as f:  # ASCII encoding
            f.write(script_content)
        
        print(f"✓ Activation script created at {output_path}")
        return True
    except Exception as e:
        print(f"✗ Failed to create activation script: {e}")
        return False