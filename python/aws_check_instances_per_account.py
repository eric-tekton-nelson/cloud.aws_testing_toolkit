import csv
import subprocess
import json

# Prompt the user for the input CSV file name
input_file_path = input("Enter the name of the input CSV file (e.g., instances.csv): ")

# Read the CSV file
instance_ids = []
try:
    with open(input_file_path, mode='r') as file:
        csv_reader = csv.reader(file)
        # Skip the header row
        next(csv_reader)
        for row in csv_reader:
            if row:
                instance_ids.append(row[0].strip())
except FileNotFoundError:
    print(f"Error: The file '{input_file_path}' does not exist. Please check the file name and try again.")
    exit(1)
except Exception as e:
    print(f"An error occurred while reading the file: {e}")
    exit(1)

# Function to check instance details using AWS CLI
def check_instance(instance_id):
    try:
        # Execute AWS CLI command to describe the instance
        result = subprocess.run(
            ['aws', 'ec2', 'describe-instances', '--instance-ids', instance_id, '--query', 'Reservations[].Instances[]', '--output', 'json'],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            instances = json.loads(result.stdout)
            if instances:
                return instances[0]  # Return the first instance details
            else:
                return None
        else:
            print(f"Error describing instance {instance_id}: {result.stderr}")
            return None
    except Exception as e:
        print(f"An error occurred while describing the instance {instance_id}: {e}")
        return None

# Check each instance and print details if found
for instance_id in instance_ids:
    instance_details = check_instance(instance_id)
    if instance_details:
        print(f"Instance {instance_id} is in the account. Details: {json.dumps(instance_details, indent=2)}")
    else:
        print(f"Instance {instance_id} is not found in the account or an error occurred.")
