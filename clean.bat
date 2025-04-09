@echo off
setlocal

echo This will clean temporary files and cached data.
set /p CONFIRM="Are you sure you want to continue? ^(y/n^): "

if /i "%CONFIRM%"=="y" (
    echo Cleaning project directories...
    
    :: Clean Python cache files
    del /s /q *.pyc
    rmdir /s /q __pycache__ 2>nul
    
    :: Clean output directories but leave the folders
    del /s /q generate_output\*
    del /s /q training_output\*
    
    echo Cleanup complete.
) else (
    echo Cleanup cancelled.
)

endlocal
