"""
install_reqs.py - YOLOv8 Requirements Installer

This module provides functionality to install YOLOv8 dependencies from a pyproject.toml
file into a specified virtual environment. Features:

- GUI-based configuration using custom form inputs
- Automatic detection of pyproject.toml location
- Virtual environment detection and validation
- Support for optional dependency groups (extras)
- Comprehensive error handling and user feedback
- Quiet mode for automated installations

The script can be run directly for interactive use or imported as a module
for programmatic dependency management.
"""

import sys
import argparse
from pathlib import Path
from typing import Optional, Dict, Any, List, Union
from scripts.utils.utils import install_requirements_from_toml, get_venv_python_path, get_project_path
from scripts.utils.ui.form import FormGenerator
from scripts.utils.ui.popup import PopupManager
from scripts.utils.ui.input import Input

def find_toml_file() -> Optional[Path]:
    """
    Locate the pyproject.toml file in the Ultralytics repository.
    
    Searches for the TOML file in the expected third_party/ultralytics directory
    relative to the project root.
    
    Returns:
        Optional[Path]: Path to pyproject.toml if found, None otherwise
    """
    project_root = get_project_path()
    ultralytics_dir = project_root / "third_party" / "ultralytics"
    toml_path = ultralytics_dir / "pyproject.toml"
    return toml_path if toml_path.exists() else None

def install_reqs(args: Union[Dict[str, Any], argparse.Namespace]) -> bool:
    """
    Install YOLO requirements into a specific virtual environment.
    
    Handles the installation of dependencies defined in pyproject.toml,
    including optional extras. Supports both dictionary and argparse.Namespace
    inputs for flexibility in calling contexts.
    
    Args:
        args: Configuration containing:
            - toml-path: Path to pyproject.toml file
            - venv-python: Path to Python executable in virtual environment
            - extras: Optional dependency groups to install
            - quiet: Suppress verbose output if True
    
    Returns:
        bool: True if installation succeeded, False otherwise
        
    Raises:
        Various exceptions from underlying pip operations are caught and logged
    """
    if isinstance(args, argparse.Namespace):
        args = vars(args)
    
    verbose = not args.get('quiet', False)
    
    try:
        toml_path = Path(args['toml-path']) if args.get('toml-path') else find_toml_file()
        venv_python = Path(args['venv-python']) if args.get('venv-python') else get_venv_python_path()

        # Validate required files exist
        if not toml_path or not toml_path.exists():
            print("Error: Could not find pyproject.toml", file=sys.stderr)
            return False
        if not venv_python or not venv_python.exists():
            print("Error: Invalid Python executable", file=sys.stderr)
            return False

        return install_requirements_from_toml(
            toml_path, 
            venv_python, 
            extras=args.get('extras'), 
            verbose=verbose
        )
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return False

def run() -> bool:
    """
    Main entry point providing a GUI interface for requirements installation.
    
    Features:
    - Form-based input for installation parameters
    - Automatic detection of TOML file and virtual environment
    - Input validation and constraints
    - Visual feedback for installation status
    - Error handling with user-friendly messages
    
    Returns:
        bool: True if installation completed successfully, False otherwise
    """
    # Initialize paths and available options
    toml_path = find_toml_file()
    venv_python = get_venv_python_path()
    
    # Define available extra dependency groups
    available_extras = ["export", "dev", "solutions", "logging", "extras", "None"]
    
    # Configure form inputs with validation and defaults
    toml_input = Input("toml-path").path('file').default(str(toml_path)) if toml_path else Input("toml_path").path('file')
    venv_input = Input("venv-python").path('file').default(str(venv_python)) if venv_python else Input("venv_python").path('file')
    extras_input = Input("extras").options(available_extras).allow_empty(True)
    quiet_input = Input("quiet").type(bool).default(False)
    
    # Create and configure the installation form
    form = FormGenerator(title="YOLO Requirements Installation",window_width=500, window_height=460)
    popup_manager = PopupManager()
    form.add_input(toml_input)
    form.add_input(venv_input)
    form.add_input(extras_input)
    form.add_input(quiet_input)
    
    try:
        # Display form and get user input
        form_results = form.show()

        # Handle form cancellation
        if not form_results:
            popup_manager.show_message(
                title="Warning!", 
                message="Installation cancelled by user",
                consoleprompt=True
            )
            return False

        # Perform installation with selected configuration
        success = install_reqs(form_results)
        if success:
            popup_manager.show_message(
                title="Success!", 
                message="Requirements installed successfully!",
                consoleprompt=True
            )
        else:
            popup_manager.show_alert(
                title="Error!", 
                message="Failed to install requirements",
                consoleprompt=True
            )

        return success
    except Exception as e:
        # Handle unexpected errors
        popup_manager.show_alert(
                title="Error!", 
                message=(f"\nInstallation failed: {str(e)}"),
                consoleprompt=True
        )
        return False
