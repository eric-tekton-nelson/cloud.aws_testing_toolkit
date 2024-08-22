#!/bin/bash
#!/bin/bash

# Check if curl is installed, if not, install it
if ! command -v curl &> /dev/null; then
    echo "curl is not installed. Installing curl..."
    sudo apt update
    sudo apt install -y curl
fi

# Download AWS CLI version 2 installer
echo "Downloading AWS CLI version 2 installer..."
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"

# Unzip the installer
unzip awscliv2.zip

# Run the installer script
sudo ./aws/install

# Clean up downloaded files
rm -rf awscliv2.zip aws

echo "AWS CLI version 2 installation complete. You can run 'aws --version' to verify."

