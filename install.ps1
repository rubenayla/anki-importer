# Requires PowerShell 5.1 or later (comes with Windows 10+)

Write-Host "Starting installation..."

# --- 1. Check for Python ---
$pythonCmd = ""
if (Get-Command python3 -ErrorAction SilentlyContinue) {
    $pythonCmd = "python3"
    Write-Host "Python 3 found: $((Get-Command python3).Source)"
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
    $pythonCmd = "python"
    Write-Host "Python found: $((Get-Command python).Source)"
} else {
    Write-Error "Error: Python 3 is not installed. Please install Python 3 to proceed."
    Write-Host "You can download it from https://www.python.org/downloads/"
    exit 1
}

# --- 2. Install Poetry if not present ---
if (-not (Get-Command poetry -ErrorAction SilentlyContinue)) {
    Write-Host "Poetry not found. Installing Poetry..."
    # Use the official recommended installation method for PowerShell
    Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing | $pythonCmd -
    
    Write-Host "Poetry installed. You might need to restart your PowerShell session or add Poetry to your PATH manually if 'poetry' command is not found."
    Write-Host "Typically, Poetry installs executables in $HOME\AppData\Roaming\Python\Scripts or similar."
    
    # Attempt to add to PATH for current session
    $env:Path += ";$HOME\AppData\Roaming\Python\Scripts"
    if (-not (Get-Command poetry -ErrorAction SilentlyContinue)) {
        Write-Warning "Poetry command still not found in PATH. Please add $HOME\AppData\Roaming\Python\Scripts to your PATH manually."
    }
} else {
    Write-Host "Poetry found: $(poetry --version)"
}

# --- 3. Install project dependencies with Poetry ---
Write-Host "Installing project dependencies with Poetry..."
poetry install

Write-Host "Installation complete!"
Write-Host ""
Write-Host "To run the Anki Importer, use the following command:"
Write-Host "poetry run python main.py"
Write-Host ""
Write-Host "For example, to list Anki models:"
Write-Host "poetry run python main.py --list-models"
Write-Host ""
Write-Host "To import questions using your config.yml:"
Write-Host "poetry run python main.py"
