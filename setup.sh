#!/bin/bash
echo "Running Python setup script..."

# Check for various Python executable names
for py in python python3 py; do
    if command -v $py > /dev/null 2>&1; then
        echo "Found Python ($py)"
        $py -m scripts.setup.setup
        exit 0
    fi
done

echo "Python not found in PATH. Installed Python versions:"
# Try to list Python versions (works on some systems)
ls /usr/bin/python* 2>/dev/null || echo "(Could not list Python versions)"

echo "Python not found. Please specify the full path to your Python executable."
read -p "Enter full path to python executable: " PYTHON_PATH

if [ -x "$PYTHON_PATH" ]; then
    echo "Running setup.py with specified Python executable..."
    "$PYTHON_PATH" -m scripts.setup.setup
    echo
else
    echo "Could not find Python at the specified path."
    echo "Please install Python and try again, or manually edit the path in this script."
    exit 1
fi