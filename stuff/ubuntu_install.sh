#!/bin/bash

# Update system repositories and upgrade packages
echo "Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install Python3 and PIP
echo "Installing Python3 and pip..."
sudo apt install python3 python3-pip -y

# Check if Python3 and pip are installed
python3 --version
pip3 --version

# Install required Python libraries
echo "Installing required Python libraries..."
pip3 install markdown2 requests

# Install Anki - using the official package from the Anki website
echo "Installing Anki..."
cd /tmp
wget https://github.com/ankitects/anki/releases/download/2.1.49/anki-2.1.49-linux-amd64.tar.bz2
tar xjf anki-2.1.49-linux-amd64.tar.bz2
cd anki-2.1.49-linux-amd64
sudo ./install.sh

# Instructions to install AnkiConnect plugin
echo "Please open Anki, go to Tools -> Add-ons -> Get Add-ons..."
echo "Enter the following code to install AnkiConnect: 2055492159"

# Reminder to check Anki setup
echo "Please ensure Anki is running with AnkiConnect enabled on port 8765."
echo "Ensure you have a deck created in Anki and match the deck_name variable in the script."

# Optional: Instructions to download and set up the AnkiMdImporter script
# echo "Downloading AnkiMdImporter..."
# wget {URL_to_AnkiMdImporter_script}
# echo "AnkiMdImporter downloaded. Please configure it according to your needs."

echo "Setup complete. You are now ready to use AnkiMdImporter."
