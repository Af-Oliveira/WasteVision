
import json
import os
import subprocess
from datetime import datetime
import sys
from pathlib import Path
from typing import Union, List, Optional
import logging


def load_config():
    """
    Loads the configuration from a JSON file.

    This function retrieves the configuration from a file located at 
    '../../config.json', relative to the directory of the script. It reads 
    the file and returns its contents as a Python dictionary.

    Raises:
        FileNotFoundError: If the configuration file does not exist at the expected path.
        json.JSONDecodeError: If the file exists but does not contain valid JSON.

    Returns:
        dict: The parsed configuration data from the JSON file.
    """
    script_dir = Path(__file__).parent
    config_path = (script_dir / '../../config.json').resolve()

    # Original behavior: Load and return the JSON config
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found at: {config_path}")
    with open(config_path, 'r') as f:
        return json.load(f)
    
def get_project_path() -> Path:
    """
    Returns the absolute path to the root of the project.
    Adjust the relative path depending on where utils.py is located.
    """
    return (Path(__file__).resolve().parent.parent.parent)  # assuming utils.py is in /project/subfolder/utils.py

def run_command(
    command: Union[str, List[str]],
    shell: bool = True,
    cwd: Optional[Union[str, Path]] = None,
    verbose: bool = True,
    check: bool = False
) -> str:
    """
    Enhanced command runner with better error handling.
    
    Args:
        command: Command to execute
        shell: Use system shell
        cwd: Working directory
        verbose: Print errors
        check: Raise exception on failure
        
    Returns:
        Command output
        
    Raises:
        subprocess.CalledProcessError: If check=True and command fails
    """
    kwargs = {
        'shell': shell,
        'text': True,
        'capture_output': True,
        'cwd': str(cwd) if cwd else None
    }
    
    try:
        result = subprocess.run(command, **kwargs)
        if verbose and result.returncode != 0:
            print(f"Command failed (code {result.returncode}): {' '.join(command) if isinstance(command, list) else command}",
                  file=sys.stderr)
            print(f"Error: {result.stderr.strip()}", file=sys.stderr)
            
        if check and result.returncode != 0:
            raise subprocess.CalledProcessError(result.returncode, command, result.stdout, result.stderr)
            
        return result.stdout.strip()
    
    except Exception as e:
        if verbose:
            print(f"Unexpected error running command: {e}", file=sys.stderr)
        raise

def confirm(prompt: str, default: bool = False) -> bool:
    """Get yes/no confirmation from user."""
    choices = " [Y/n] " if default else " [y/N] "
    while True:
        response = input(prompt + choices).strip().lower()
        if not response:
            return default
        if response in ('y', 'yes'):
            return True
        if response in ('n', 'no'):
            return False
        print("Please enter 'y' or 'n'")


def create_directories(
    base_path: Union[str, Path],
    directories: List[str],
    verbose: bool = True,
    exist_ok: bool = True
) -> None:
    """
    Create multiple directories relative to a base path.
    
    Args:
        base_path: Root directory for relative paths
        directories: List of directory paths (relative or absolute)
        verbose: Print status messages
        exist_ok: Don't raise error if directory exists (default: True)
    
    Raises:
        OSError: If directory creation fails (and exist_ok=False)
    """
    base_path = Path(base_path).resolve()
    if verbose:
        print(f"\nCreating directories in: {base_path}")
    
    created_count = 0
    for dir_path in directories:
        # Handle both relative and absolute paths correctly
        dir_path_obj = Path(dir_path)
        if dir_path_obj.is_absolute():
            full_path = dir_path_obj.resolve()
        else:
            full_path = (base_path / dir_path).resolve()
        
        dir_existed = full_path.exists() and full_path.is_dir()
        
        try:
            full_path.mkdir(parents=True, exist_ok=exist_ok)
            if verbose:
                if dir_existed:
                    print(f"• Already exists: {full_path}")
                else:
                    print(f"✓ Created: {full_path}")
                    created_count += 1
        except OSError as e:
            if verbose:
                print(f"✗ Failed to create {full_path}: {e}")
            if not exist_ok:
                raise
        except Exception as e:
            if verbose:
                print(f"✗ Unexpected error creating {full_path}: {e}")
            raise

    if verbose:
        print(f"\nCreated {created_count} new directories (of {len(directories)} total)")


def create_virtual_environments(
    venv_name: str,
    suffixes: List[str],
    workon_home: Optional[Union[str, Path]],
    project_path: Optional[Union[str, Path]]
) -> bool:
    """
    Create multiple virtual environments with optional post-activation script execution.
    Supports Windows (cmd/PowerShell) and Linux/Mac (bash).

    Args:
        venv_name: Base name for environments (e.g., "wastevision")
        suffixes: List of (suffix, python_version) tuples 
                 (e.g., [("yolov8", "3.11"), ("tf", "3.9")])
        workon_home: Directory for environments                  
        project_path: Optional path to project directory. If provided:
                     - Creates post-activation script to run main.py
                     - Modifies env activation to auto-run the script

    Returns:
        bool: True if all environments created successfully, False otherwise
    """
    print("\n=== Creating Virtual Environments ===")
    
    success = True
    created_count = 0
    
    for suffix in suffixes:
        env_name = f"{venv_name}_{suffix[0]}"
        env_path = workon_home / env_name
        print(f"\nCreating environment: {env_name}")
        
        try:
            # Check if env already exists
            if env_path.exists():
                print(f"✓ Environment '{env_name}' already exists at {env_path}")
                created_count += 1
                continue
                
            if sys.platform == "win32":
                cmd = f"python{suffix[1]} -m venv \"{env_path}\""
                activate_script = env_path / "Scripts" / "activate.bat"
                post_activate = env_path / "Scripts" / "post_activate.bat"
            else:
                cmd = f"python{suffix[1]} -m venv \"{env_path}\" --prompt=\"{env_name}\""
                activate_script = env_path / "bin" / "activate"
                post_activate = env_path / "bin" / "post_activate"

            run_command(cmd, check=True)

            # Set environment variables in the activation scripts
            if sys.platform == "win32":
                # Windows: Add to activate.bat
                with open(activate_script, "a") as f:
                    f.write(f"\nset VENV_NAME={env_name}\n")
                    f.write(f"set VENV_PATH={env_path}\n")
                    if project_path:
                        f.write(f"set VENV_MAIN={project_path}\n")
            else:
                # Linux/Mac: Add to activate
                with open(activate_script, "a") as f:
                    f.write(f'\nexport VENV_NAME="{env_name}"\n')
                    f.write(f'export VENV_PATH="{env_path}"\n')
                    if project_path:
                        f.write(f'export VENV_MAIN="{project_path}"\n')

            # Add auto-run logic if project_path is specified
            if project_path:
                project_root = Path(project_path).resolve()
                if sys.platform == "win32":
                    # Windows: Create post-activate.bat
                    with open(post_activate, "w") as f:
                        f.write("@echo off\n")
                        f.write(f"cd \"{project_root}\"\n")
                        f.write(f"python -m scripts.models.{suffix[0]}.main\n")
                    # Append to activate.bat
                    with open(activate_script, "a") as f:
                        f.write(f"\ncall \"{post_activate}\"\n")
                else:
                    # Linux/Mac: Create post_activate
                    with open(post_activate, "w") as f:
                        f.write("#!/bin/bash\n")
                        f.write(f"cd \"{project_root}\"\n")
                        f.write(f"python -m scripts.models.{suffix[0]}.main\n")
                    os.chmod(post_activate, 0o755)
                    # Append to activate
                    with open(activate_script, "a") as f:
                        f.write(f"\nsource \"{post_activate}\"\n")
        
            print(f"✓ Successfully created: {env_name} at {env_path}")
            created_count += 1

            # Install basic packages (optional)
            pip_path = env_path / "Scripts" / "pip.exe" if sys.platform == "win32" else env_path / "bin" / "pip"
            wheel_cmd = f'"{pip_path}" install wheel'
            tomli_cmd = f'"{pip_path}" install tomli'
            run_command(wheel_cmd, check=False)
            run_command(tomli_cmd, check=False)
            
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to create {env_name}: {e.stderr if hasattr(e, 'stderr') else str(e)}")
            success = False
        except Exception as e:
            print(f"✗ Unexpected error creating {env_name}: {str(e)}")
            success = False
    
    print(f"\nCreated {created_count}/{len(suffixes)} environments\n")
    return success



def install_requirements_from_toml(toml_path: Path, venv_python: Path, extras: Union[str, List[str]] = None, verbose: bool = True) -> bool:
    import tomli as toml
    """
    Install Python requirements from a pyproject.toml file into a specific virtual environment.
    Installs each package individually to isolate failures.
    
    Args:
        toml_path (Path): Path to the pyproject.toml file
        venv_python (Path): Path to the Python executable in the virtual environment
        extras (list, optional): List of extras to install (e.g., ['dev', 'export'])
        verbose (bool): Whether to print detailed information
        
    Returns:
        bool: True if all installations succeeded, False if any failed
    """
    try:   
        if verbose:
            print(f"Loading requirements from {toml_path}")
            print(f"Using Python from: {venv_python}")
        
        # Load the TOML file
        with open(toml_path, 'rb') as f:  # Note 'rb' mode for tomli
            data = toml.load(f)
        
        # Get dependencies
        dependencies = data.get('project', {}).get('dependencies', [])
        extras_require = data.get('project', {}).get('optional-dependencies', {})
        
        if verbose and extras_require:
            print(f"Available extras: {', '.join(extras_require.keys())}")
        
         # Normalize extras to always be a list
        if extras != "None":
            extras_list = [extras] if isinstance(extras, str) else extras
        else:
            extras_list = []

        # Combine base dependencies with selected extras
        requirements = dependencies.copy()
        if extras:
            for extra in extras_list:
                if extra in extras_require:
                    if verbose:
                        print(f"Including '{extra}' dependencies: {len(extras_require[extra])} packages")
                    requirements.extend(extras_require[extra])
                else:
                    print(f"Warning: Extra '{extra}' not found in the TOML file")
        
        # Install requirements one by one
        if requirements:
            if verbose:
                print(f"Installing {len(requirements)} packages into the virtual environment...")
            
            success = True
            pip_base = [str(venv_python), '-m', 'pip', 'install']
            
            for req in requirements:
                try:
                    if verbose:
                        print(f"  - Installing {req}...")
                    
                    run_command(
                        command=pip_base + [req],
                        shell=False,
                        verbose=verbose,
                        check=True
                    )
                    
                except subprocess.CalledProcessError as e:
                    print(f"Failed to install {req}: {e}")
                    success = False
                    if not confirm("Continue with remaining packages?", default=True):
                        return False
                    continue
                except Exception as e:
                    print(f"Unexpected error installing {req}: {e}")
                    success = False
                    if not confirm("Continue with remaining packages?", default=True):
                        return False
                    continue
            
            if verbose:
                if success:
                    print("All packages installed successfully!")
                else:
                    print("Installation completed with some failures")
            return success
        
        print("No requirements found in the TOML file.")
        return False
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except toml.TomlDecodeError:
        print(f"Error: Invalid TOML file - {toml_path}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    
    return False


def get_venv_python_path():
    """Get the path to the Python executable in the YOLO virtual environment.
    If no venv is found, asks user if they want to install dependencies globally.
    Returns None if user declines global installation."""
    
    # First check if we're already in a virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        # We're in a venv, use current Python
        return Path(sys.executable)
        
    # No venv found - ask about global installation
    print("\nNo active virtual environment detected.")
    if confirm("Do you want to install dependencies globally?", default=False):
        return Path(sys.executable)  # Use system Python
    else:
        print("Installation cancelled. Please activate a virtual environment first.")
        return None
    
def setup_project_directories(project_dir: Union[str,Path]) -> bool:
    """Handle the complete directory creation process with verification"""

    config = load_config()

    directories = config['directory_list']

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
    

def get_unique_dir(base_path: Path, base_name: str = "NewFolder") -> Path:
    """
    Get a unique directory path by appending a number if the base directory exists.
    
    Args:
        base_path: The parent directory where the new directory will be created
        base_name: The base name of the directory (default: "NewFolder")
    
    Returns:
        Path: A path that doesn't exist yet (e.g., "NewFolder2" if "NewFolder" exists)
    """
    counter = 1
    while True:
        if counter == 1:
            dir_name = base_name
        else:
            dir_name = f"{base_name}{counter}"
        
        target_path = base_path / dir_name
        if not target_path.exists():
            return target_path
        counter += 1