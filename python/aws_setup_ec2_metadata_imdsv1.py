import subprocess
import sys

def fetch_metadata(url):
    try:
        result = subprocess.run(['curl', url], capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error fetching URL {url}: {e}", file=sys.stderr)
        return None

def run_command(command, success_message, error_message, ssh_prefix):
    """Execute a shell command over SSH"""
    try:
        subprocess.run(ssh_prefix + command, check=True)
        print(success_message)
    except subprocess.CalledProcessError:
        print(error_message, file=sys.stderr)

# Example SSH setup
ssh_key_path = input("Enter the path to your SSH key (e.g., ~/.ssh/id_rsa): ")
ec2_uri = input("Enter the URI of the EC2 instance (e.g., ec2-user@10.0.1.159): ")
ssh_prefix = ['ssh', '-i', ssh_key_path, ec2_uri]

# Installation and setup of HTTP server (Apache) via subprocess over SSH
print("Installation and setup of HTTP server (Apache)...")
run_command(['sudo', 'yum', 'update', '-y'], "System packages updated.", "Failed to update system packages.", ssh_prefix)
run_command(['sudo', 'yum', 'install', '-y', 'httpd'], "Apache installed.", "Failed to install Apache.", ssh_prefix)
