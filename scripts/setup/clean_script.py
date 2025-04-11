import os
from pathlib import Path

def create_clean_script(project_dir: str, output_path: Path = "clean_project.bat") -> bool:
    """
    Creates a batch script to clean project cache and temporary files.
    
    Args:
        project_root: Path to project root directory
        output_path: Where to save the batch file
        
    Returns:
        bool: True if script was created successfully
    """
    try:
        project_root = Path(project_dir)
        project_root = project_root.resolve()
        output_path = Path(output_path).resolve()
        
        print(f"Creating clean script at: {output_path}")

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

        with open(output_path, "w", newline='\r\n') as f:
            f.write(content)
        
        print(f"✓ Clean script created successfully")
        return True
        
    except Exception as e:
        print(f"✗ Failed to create clean script: {e}")
        return False