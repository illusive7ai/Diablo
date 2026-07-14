@echo off
echo [+] Diablo Proxy Tool - Setup Script
echo [+] Installing dependencies...

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [!] Python is not installed. Please install Python 3.6 or higher.
    pause
    exit /b 1
)

:: Check if pip is installed
pip --version >nul 2>&1
if errorlevel 1 (
    echo [!] pip is not installed. Installing pip...
    python -m ensurepip --upgrade
)

:: Install requirements
echo [+] Installing required packages...
pip install -r requirements.txt

echo [+] Setup complete!
echo [+] python diablo.py
pause