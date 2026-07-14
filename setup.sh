#!/bin/bash
# Diablo Setup Script for Linux/macOS

echo "[+] Diablo Proxy Tool - Setup Script"
echo "[+] Installing dependencies..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "[!] Python 3 is not installed. Please install Python 3.6 or higher."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "[!] pip3 is not installed. Installing pip..."
    python3 -m ensurepip --upgrade
fi

# Install requirements
echo "[+] Installing required packages..."
pip3 install -r requirements.txt

# Make script executable
chmod +x diablo.py

# Create alias (optional)
echo "[+] Creating alias 'diablo'..."
echo "alias diablo='python3 $(pwd)/diablo.py'" >> ~/.bashrc
echo "alias diablo='python3 $(pwd)/diablo.py'" >> ~/.zshrc 2>/dev/null

echo "[+] Setup complete!"
echo "[+] Run Diablo with: python3 diablo.py"
echo "[+] Or use the alias: diablo"