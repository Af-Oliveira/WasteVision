import os
import subprocess
import sys
from pathlib import Path
from typing import List, Union, Optional
from .activation_script import create_activate_script
from .clean_script import create_clean_script
from .update_script import create_update_script
from ..utils.utils import confirm, create_directories, create_virtual_environments


def setup_project_directories(project_dir: str) -> bool:
    """Handle the complete directory creation process with verification"""
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
    project_root = Path(project_dir)
    print("\n=== Project Directory Setup ===")
    print(f"Base location: {project_root.resolve()}")
    
    # Verify we can write to the location
    try:
        test_file = project_root / ".permission_test"
        test_file.touch()
        test_file.unlink()
    except PermissionError:
        print(f"Error: No write permissions in {project_root}", file=sys.stderr)
        return False
    
    # Show directory tree preview
    print("\nDirectory structure to be created:")
    for dir_path in directories:
        print(f"  {project_root / dir_path}")
    
    if not confirm("Create these directories?", default=True):
        print("Directory creation cancelled.")
        return False
    
    # Actual creation with error handling
    try:
        create_directories(
            base_path=project_root,
            directories=directories,
            verbose=True,
            exist_ok=True  # We want to know if directories already exist
        )
        
        # Verification step
        missing = []
        for dir_path in directories:
            if not (project_root / dir_path).exists():
                missing.append(str(project_root / dir_path))
        
        if missing:
            print("\nWarning: Some directories weren't created:", file=sys.stderr)
            for path in missing:
                print(f"  - {path}", file=sys.stderr)
            return False
            
        print("\n✓ All directories created successfully")
        return True
        
    except Exception as e:
        print(f"\nError during directory creation: {e}", file=sys.stderr)
        return False


if __name__ == "__main__":
    # Get Python path from user
    default_python = sys.executable
    python_path = input(f"Enter the path to your Python executable (Press Enter for default '{default_python}'): ") or default_python
    
    # Get virtual environment name from user
    default_venv = "wastevision/wv-venv"
    venv_name = input(f"Enter the base name for your virtual environment (Press Enter for default '{default_venv}'): ") or default_venv
    
    # Set up environment variables
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.abspath(os.path.join(script_dir, "../../"))
    workon_home = os.path.join(project_dir, "envs")
    
     # Create workon_home directory if it doesn't exist
    Path(workon_home).mkdir(parents=True, exist_ok=True)

    if not setup_project_directories(project_dir):  # Make sure this function accepts base path
        print("Failed to setup directories", file=sys.stderr)
        sys.exit(1)
    
        # Create virtual environments
    env_suffixes = ["yolo", "vit", "ssd", "fast-rcc"]
    if not create_virtual_environments(
        venv_name=venv_name,
        python_path=python_path,
        suffixes=env_suffixes,
        workon_home=workon_home
    ):
        print("Failed to create virtual environments", file=sys.stderr)
        sys.exit(1)
    
    # Create activation script
    activate_script_path = os.path.join(project_dir, "activate_env.bat")
    if not create_activate_script(
        venv_name=venv_name,
        workon_home=workon_home,
        env_suffixes=env_suffixes,
        output_path=activate_script_path
    ):
        print("Failed to create activation script", file=sys.stderr)
        sys.exit(1)

     # Create utility scripts
    if not create_clean_script(
        project_dir=project_dir,
        output_path=os.path.join(project_dir, "clean_project.bat")
    ):
        print("Warning: Failed to create clean script", file=sys.stderr)

    if not create_update_script(
        venv_name=venv_name,
        workon_home=workon_home,
        env_suffixes=env_suffixes,
        output_path=os.path.join(project_dir, "update_deps.bat")
    ):
        print("Warning: Failed to create update script", file=sys.stderr)

    print("\n=== Setup Summary ===")
    print(f"✓ Virtual environments created: {', '.join([f'{venv_name}_{suffix}' for suffix in env_suffixes])}")
    print(f"✓ Activation script: {activate_script_path}")
    print(f"✓ Clean script: {os.path.join(script_dir, 'clean_project.bat')}")
    print(f"✓ Update script: {os.path.join(script_dir, 'update_deps.bat')}")
    print("\nSetup completed successfully!")

 # Activate environment
    print("\n=== Environment Activation ===")
    if sys.platform == "win32":
        try:
            # Use absolute path to ensure reliability
            os.system(f'call "{activate_script_path}"')
        except Exception as e:
            print(f"Failed to activate environment: {e}")
    else:
        # Linux/Mac users need to source the script manually
        #TODO: Provide a more user-friendly way to activate the environment for Linux/Mac users
        print("On Linux/Mac, please source the environment manually")
        print(f"Suggested command: source {workon_home}/{venv_name}_yolo/bin/activate")