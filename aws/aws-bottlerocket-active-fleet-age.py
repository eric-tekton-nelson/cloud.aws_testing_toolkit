import boto3
from datetime import datetime, timezone
from tabulate import tabulate

# Prompt user for AWS profile, region, and output file name
aws_profile = input("Enter the AWS profile name: ")
aws_region = input("Enter the AWS region: ")
output_file_name = input("Enter the name of the output file (e.g., output_file.txt): ")

# Use the specified profile
session = boto3.Session(profile_name=aws_profile)

# Initialize a session using Amazon EC2 in the specified region
ec2 = session.client('ec2', region_name=aws_region)

# Retrieve running EC2 instances and filter for Bottlerocket instances
response = ec2.describe_instances(
    Filters=[
        {'Name': 'instance-state-name', 'Values': ['running']},
        {'Name': 'platform-details', 'Values': ['Bottlerocket']}
    ]
)

# Process the response to list instance IDs and their ages
instances = []
for reservation in response['Reservations']:
    for instance in reservation['Instances']:
        instance_id = instance['InstanceId']
        launch_time = instance['LaunchTime']
        
        # Calculate the age of the instance
        now = datetime.now(timezone.utc)
        age = now - launch_time
        
        instances.append({
            'InstanceId': instance_id,
            'LaunchTime': launch_time,
            'Age (days)': age.days
        })

# Prepare data for tabulate
table_data = [
    [inst['InstanceId'], inst['LaunchTime'], inst['Age (days)']] for inst in instances
]

# Print the results to the console
print(tabulate(table_data, headers=["InstanceId", "LaunchTime", "Age (days)"], tablefmt="pretty"))

# Write the results to the specified output file
with open(output_file_name, 'w') as file:
    file.write(tabulate(table_data, headers=["InstanceId", "LaunchTime", "Age (days)"], tablefmt="pretty"))

print(f"Output has been written to {output_file_name}")
