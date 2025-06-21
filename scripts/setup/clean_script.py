"""
clean_script.py - Project cleanup script generator for WasteVision

This module creates platform-specific cleanup scripts that remove:
- Python cache files (__pycache__, .pyc, .pyo)
- Jupyter notebook checkpoints
- VS Code cache files
- Training output files and directories
- Other temporary files generated during development

The script handles both Windows (.bat) and Unix-like (.sh) systems
and ensures proper line endings and permissions for each platform.
"""

import os
from pathlib import Path

def create_clean_script(
    project_dir: str, 
    output_path: Path = "clean_project.sh", 
    is_windows: bool = False
) -> bool:
    """
    Creates a platform-specific script to clean project cache and temporary files.

    This function generates either a Windows batch file (.bat) or a Unix shell 
    script (.sh) that removes various temporary files and directories commonly
    generated during Python development and model training.
    
    Args:
        project_dir: Path to the project root directory where cleanup will occur
        output_path: Where to save the generated script file (default: clean_project.sh)
        is_windows: If True, creates a Windows batch script, otherwise Unix shell script
        
    Returns:
        bool: True if script was created successfully, False if any errors occurred
        
    Example:
        ```python
        create_clean_script(
            project_dir="C:/MyProject",
            output_path="cleanup.bat",
            is_windows=True
        )
        ```
    """
    try:
        # Resolve absolute paths
        project_root = Path(project_dir)
        project_root = project_root.resolve()
        output_path = Path(output_path).resolve()
        
        print(f"Creating clean script at: {output_path}")

        # Generate Windows batch script
        if is_windows:
            content = f"""@echo off
REM Clean project cache and temporary files
echo Cleaning project at: {project_root}

REM Python cache files
echo Removing __pycache__ directories...
for /r {project_root} %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"

REM Python compiled files
echo Removing .pyc and .pyo files...
del /s /q {project_root}\\*.pyc
del /s /q {project_root}\\*.pyo

REM Jupyter notebook checkpoints
echo Removing .ipynb_checkpoints...
for /r {project_root} %%d in (.ipynb_checkpoints) do @if exist "%%d" rd /s /q "%%d"

REM VS Code cache
echo Removing VS Code cache...
if exist "{project_root}\\.vscode\\*.cache" del /q "{project_root}\\.vscode\\*.cache"

REM Training outputs
echo Cleaning training outputs...
if exist "{project_root}\\training_output\\*" (
    del /s /q "{project_root}\\training_output\\*.*"
)

echo Cleanup complete!
pause
"""
        # Generate Unix shell script
        else:
            content = f"""#!/bin/bash
# Clean project cache and temporary files
echo "Cleaning project at: {project_root}"

# Python cache files
echo "Removing __pycache__ directories..."
find "{project_root}" -type d -name "__pycache__" -exec rm -rf {{}} +

# Python compiled files
echo "Removing .pyc and .pyo files..."
find "{project_root}" -type f -name "*.pyc" -delete
find "{project_root}" -type f -name "*.pyo" -delete

# Jupyter notebook checkpoints
echo "Removing .ipynb_checkpoints..."
find "{project_root}" -type d -name ".ipynb_checkpoints" -exec rm -rf {{}} +

# VS Code cache
echo "Removing VS Code cache..."
find "{project_root}/.vscode" -type f -name "*.cache" -delete 2>/dev/null

# Training outputs
echo "Cleaning training outputs..."
if [ -d "{project_root}/training_output" ]; then
    find "{project_root}/training_output" -mindepth 1 -delete
fi

echo "Cleanup complete!"
read -p "Press enter to continue..."
"""
        # Write the script with appropriate line endings
        with open(output_path, "w", newline='\n' if not is_windows else '\r\n') as f:
            f.write(content)
        
        # Make Unix scripts executable
        if not is_windows:
            os.chmod(output_path, 0o755)
        
        print(f"✓ Clean script created at {output_path}")
        print("\n")
        return True
        
    except Exception as e:
        print(f"✗ Failed to create clean script: {e}")
        print("\n")
        return False