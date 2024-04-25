#!/bin/bash

# Install git
sudo yum install -y git

# Clone the pyenv repository into the home directory
git clone https://github.com/pyenv/pyenv.git ~/.pyenv

# Set up pyenv environment variables
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.bashrc

# Source the bashrc to apply changes
. ~/.bashrc

# Install necessary libraries using yum for building Python
sudo yum install -y gcc zlib-devel bzip2 bzip2-devel readline-devel sqlite sqlite-devel openssl-devel xz xz-devel libffi-devel

# Install Python version using pyenv
pyenv install 3.12.2
pyenv global 3.12.2

# Install Python packages using pip
pip install boto3

# Script to install MySQL client on Fedora

# Step 1: Update the system
echo "Updating the system..."
sudo dnf update -y

# Step 2: Install MySQL client
echo "Installing MySQL client..."
sudo dnf -y localinstall https://dev.mysql.com/get/mysql80-community-release-el9-4.noarch.rpm
sudo dnf -y install mysql mysql-community-client
sudo dnf install mysql-community-server

# Step 3: Check the MySQL client version to verify installation
echo "Checking MySQL client version..."
mysql --version

if [ $? -eq 0 ]; then
    echo "MySQL client installed successfully."
else
    echo "Failed to install MySQL client."
fi
