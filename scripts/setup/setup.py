"""
setup.py - Project initialization and environment setup script for WasteVision

This script handles the initial setup of the WasteVision project, including:
- Creating necessary directory structure
- Setting up virtual environments for different models
- Generating activation scripts for environment management
- Creating utility scripts for project maintenance

The script uses configuration from config.json to determine:
- Virtual environment names and Python versions
- Required directory structure
- Model-specific configurations
"""

import os
import sys
from pathlib import Path
from .activation_script import create_activate_script
from .clean_script import create_clean_script
from ..utils.utils import (
    setup_project_directories,
    create_virtual_environments,
    load_config,
    get_project_path
)

if __name__ == "__main__":
    # Load project configuration from config.json
    config = load_config()

    # Set up paths and environment configuration
    default_venv = config['venv_name']
    project_dir = get_project_path()
    env_project_path = project_dir
    workon_home = project_dir / "venvs"
    env_suffixes = config['venv_suffix']

    # Get virtual environment name from user or use default
    venv_name = input(
        f"Enter the base name for your virtual environment "
        f"(Press Enter for default '{default_venv}'): "
    ) or default_venv
    
    # Create virtual environments directory
    Path(workon_home).mkdir(parents=True, exist_ok=True)

    # Set up project directory structure
    if not setup_project_directories(project_dir):  
        print("Failed to setup directories", file=sys.stderr)
        sys.exit(1)
       
    # Create virtual environments for each model type
    if not create_virtual_environments(
        venv_name=venv_name,
        suffixes=env_suffixes,
        workon_home=workon_home,
        project_path=env_project_path
    ):
        print("Failed to create virtual environments", file=sys.stderr)
        sys.exit(1)
    
    # Determine platform-specific script settings
    if sys.platform == "win32":
        is_windows: bool = True
        script_suffix = ".bat"
    else:
        is_windows: bool = False
        script_suffix = ".sh"

    # Generate environment activation script
    activate_script_path = os.path.join(project_dir, f"activate_env{script_suffix}")
    if not create_activate_script(
        venv_name=venv_name,
        workon_home=workon_home,
        env_suffixes=env_suffixes,
        output_path=activate_script_path,
        is_windows=is_windows
    ):
        print("Failed to create activation script", file=sys.stderr)
        sys.exit(1)

    # Create project cleanup utility script
    clean_script_path = os.path.join(project_dir, f"clean_project{script_suffix}")
    if not create_clean_script(
        project_dir=project_dir,
        output_path=clean_script_path,
        is_windows=is_windows
    ):
        print("Warning: Failed to create clean script", file=sys.stderr)

    # Display setup completion summary
    print("\n=== Setup Summary ===")
    print(f"✓ Virtual environments created: "
          f"{', '.join([f'{venv_name}_{suffix[0]}' for suffix in env_suffixes])}")
    print(f"✓ Activation script: {activate_script_path}")
    print(f"✓ Clean script: {clean_script_path}")
    print("\nSetup completed successfully!")


