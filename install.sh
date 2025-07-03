#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

echo "Starting installation..."

# --- 1. Check for Python ---
if command -v python3 &>/dev/null;
then
    PYTHON_CMD="python3"
    echo "Python 3 found: $($PYTHON_CMD --version)"
elif command -v python &>/dev/null;
then
    PYTHON_CMD="python"
    echo "Python found: $($PYTHON_CMD --version)"
else
    echo "Error: Python 3 is not installed. Please install Python 3 to proceed."
    echo "You can download it from https://www.python.org/downloads/"
    exit 1
fi

# --- 2. Install Poetry if not present ---
if ! command -v poetry &>/dev/null;
then
    echo "Poetry not found. Installing Poetry..."
    # Use the official recommended installation method
    $PYTHON_CMD -m pip install poetry
    # Add Poetry to PATH for current session (and future if shell config is updated)
    # This might need user intervention or a shell restart, but for now, we'll assume it's added.
    # For a more robust solution, users might need to add it to their .bashrc/.zshrc
    echo "Poetry installed. You might need to restart your terminal or add Poetry to your PATH manually if 'poetry' command is not found."
    echo "Typically, Poetry installs executables in ~/.local/bin or similar."
    echo "Attempting to add to PATH for this session..."
    export PATH="$HOME/.local/bin:$PATH"
    if ! command -v poetry &>/dev/null;
    then
        echo "Warning: Poetry command still not found in PATH. Please add $HOME/.local/bin to your PATH manually."
        echo "Example: echo 'export PATH=\"$HOME/.local/bin:\$PATH\"' >> ~/.bashrc && source ~/.bashrc"
    fi
else
    echo "Poetry found: $(poetry --version)"
fi

# --- 3. Install project dependencies with Poetry ---
echo "Installing project dependencies with Poetry..."
poetry install

echo "Installation complete!"
echo ""
echo "To run the Anki Importer, use the following command:"
echo "poetry run python main.py"
echo ""
echo "For example, to list Anki models:"
echo "poetry run python main.py --list-models"
echo ""
echo "To import questions using your config.yml:"
echo "poetry run python main.py"
