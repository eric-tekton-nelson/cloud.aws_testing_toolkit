import paramiko
import requests
import sys

def get_metadata_token():
    try:
        url = 'http://169.254.169.254/latest/api/token'
        headers = {'X-aws-ec2-metadata-token-ttl-seconds': '21600'}
        response = requests.put(url, headers=headers)
        response.raise_for_status()
        print("Metadata token retrieved successfully.")
        return response.text
    except requests.RequestException as e:
        print("Failed to retrieve metadata token:", e)
        sys.exit(1)

def get_instance_metadata(token, data_type):
    try:
        url = f'http://169.254.169.254/latest/meta-data/{data_type}'
        headers = {'X-aws-ec2-metadata-token': token}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        print(f"Successfully retrieved {data_type}.")
        return response.text
    except requests.RequestException as e:
        print(f"Failed to retrieve {data_type}:", e)
        sys.exit(1)

def ssh_command(ssh_client, command):
    try:
        stdin, stdout, stderr = ssh_client.exec_command(command)
        err = stderr.read().decode()
        if err:
            raise Exception(err)
        out = stdout.read().decode()
        print(f"Executed command '{command}' successfully.")
        return out
    except Exception as e:
        print(f"Error executing command '{command}':", e)
        sys.exit(1)

def main():
    host = input("Enter the host IP address: ")
    username = "ec2-user"
    key_path = input("Enter the path to your private key file: ")

    # Initialize and setup SSH client
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh_client.connect(hostname=host, username=username, key_filename=key_path)
        print("SSH connection established.")
    except Exception as e:
        print("Failed to establish SSH connection:", e)
        sys.exit(1)

    try:
        token = get_metadata_token()
        instance_id = get_instance_metadata(token, 'instance-id')
        ami_id = get_instance_metadata(token, 'ami-id')
        instance_type = get_instance_metadata(token, 'instance-type')

        commands = [
            'sudo yum update -y',
            'sudo yum install -y httpd',
            'sudo systemctl start httpd',
            'sudo systemctl enable httpd'
        ]

        for command in commands:
            ssh_command(ssh_client, command)

        html_content = f"""
        <html>
        <head>
            <title>EC2 Instance Metadata</title>
        </head>
        <body>
            <h1>EC2 Instance Metadata</h1>
            <p>Instance ID: {instance_id}</p>
            <p>AMI ID: {ami_id}</p>
            <p>Instance Type: {instance_type}</p>
        </body>
        </html>
        """
                
        ssh_command(ssh_client, f'echo "{html_content}" | sudo tee /var/www/html/index.html')
        
    finally:
        ssh_client.close()
        print("SSH connection closed.")

if __name__ == "__main__":
    main()
