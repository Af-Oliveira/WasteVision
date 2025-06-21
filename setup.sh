#!/bin/bash

# -----------------------------------------------------------------------------
# WasteVision Project - Linux/Mac Setup Script
# This script locates a Python interpreter and runs the main setup routine.
# It automates environment and directory creation for the project.
# -----------------------------------------------------------------------------

echo "Running Python setup script..."

# Try to find a Python executable by checking common names
for py in python python3 py; do
    if command -v $py > /dev/null 2>&1; then
        echo "Found Python ($py)"
        $py -m scripts.setup.setup
        exit 0
    fi
done

# If no Python executable was found, print a message and try to list installed versions
echo "Python not found in PATH. Installed Python versions:"
ls /usr/bin/python* 2>/dev/null || echo "(Could not list Python versions)"

# Prompt the user to manually enter the full path to their Python executable
echo "Python not found. Please specify the full path to your Python executable."
read -p "Enter full path to python executable: " PYTHON_PATH

# Check if the provided path is executable
if [ -x "$PYTHON_PATH" ]; then
    echo "Running setup.py with specified Python executable..."
    "$PYTHON_PATH" -m scripts.setup.setup
    echo
else
    echo "Could not find Python at the specified path."
    echo "Please install Python and try again, or manually edit the path in this script."
    exit 1
fi