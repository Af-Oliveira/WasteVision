import os
import sys
from pathlib import Path
from .activation_script import create_activate_script
from .clean_script import create_clean_script
from ..utils.utils import setup_project_directories, create_virtual_environments, load_config, get_project_path

if __name__ == "__main__":
    # Get Python path from user
    config = load_config()

    # Get virtual environment name from user
    default_venv = config['venv_name']
    project_dir = get_project_path()

    env_project_path = project_dir
    workon_home = project_dir / "venvs"
    env_suffixes = config['venv_suffix']

    venv_name = input(f"Enter the base name for your virtual environment (Press Enter for default '{default_venv}'): ") or default_venv
    
     # Create workon_home directory 
    Path(workon_home).mkdir(parents=True, exist_ok=True)

    if not setup_project_directories(project_dir):  
        print("Failed to setup directories", file=sys.stderr)
        sys.exit(1)
       
    # Create virtual environments
    if not create_virtual_environments(
        venv_name=venv_name,
        suffixes=env_suffixes,
        workon_home=workon_home,
        project_path=env_project_path
    ):
        print("Failed to create virtual environments", file=sys.stderr)
        sys.exit(1)
    
    if sys.platform == "win32":
        is_windows: bool = True
        script_suffix = ".bat"
    else:
        is_windows: bool = False
        script_suffix = ".sh"


    # Create activation script
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

     # Create utility scripts
    clean_script_path = os.path.join(project_dir, f"clean_project{script_suffix}")
    if not create_clean_script(
        project_dir=project_dir,
        output_path=clean_script_path,
        is_windows=is_windows
    ):
        print("Warning: Failed to create clean script", file=sys.stderr)

    print("\n=== Setup Summary ===")
    print(f"✓ Virtual environments created: {', '.join([f'{venv_name}_{suffix[0]}' for suffix in env_suffixes])}")
    print(f"✓ Activation script: {activate_script_path}")
    print(f"✓ Clean script: {clean_script_path}")
    print("\nSetup completed successfully!")


      