import os
import subprocess
import sys
from pathlib import Path
from typing import Union, List, Optional

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
    python_path: str,
    suffixes: List[str] = ["yolo", "vit", "ssd", "fast-rcc"],
    workon_home: Optional[Union[str, Path]] = None
) -> bool:
    """
    Create multiple virtual environments using Python's built-in venv module.
    
    Args:
        venv_name: Base name for environments
        python_path: Path to Python interpreter
        suffixes: List of environment suffixes
        workon_home: WORKON_HOME directory (if not default)
    
    Returns:
        bool: True if all environments created successfully, False otherwise
    """
    print("\n=== Creating Virtual Environments ===")
    
    # Set WORKON_HOME if specified
    if workon_home:
        workon_home = Path(workon_home).resolve()
        os.environ["WORKON_HOME"] = str(workon_home)
    else:
        workon_home = Path(os.environ.get("WORKON_HOME", os.path.expanduser("~/.virtualenvs")))
    
    success = True
    created_count = 0
    
    for suffix in suffixes:
        env_name = f"{venv_name}_{suffix}"
        env_path = workon_home / env_name
        print(f"\nCreating environment: {env_name}")
        
        try:
            # Check if env already exists
            if env_path.exists():
                print(f"✓ Environment '{env_name}' already exists at {env_path}")
                created_count += 1
                continue
                
            # Create new environment using venv directly
            cmd = f'"{python_path}" -m venv "{env_path}"'
            run_command(cmd, check=True)
            print(f"✓ Successfully created: {env_name} at {env_path}")
            created_count += 1
            
            # Install basic packages (optional)
            pip_path = env_path / "Scripts" / "pip.exe" if sys.platform == "win32" else env_path / "bin" / "pip"
            wheel_cmd = f'"{pip_path}" install wheel'
            run_command(wheel_cmd, check=False)
            
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to create {env_name}: {e.stderr if hasattr(e, 'stderr') else str(e)}")
            success = False
        except Exception as e:
            print(f"✗ Unexpected error creating {env_name}: {str(e)}")
            success = False
    
    print(f"\nCreated {created_count}/{len(suffixes)} environments")
    return success
