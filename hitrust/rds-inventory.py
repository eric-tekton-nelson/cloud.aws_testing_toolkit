import boto3
import sys
from botocore.exceptions import ProfileNotFound
from datetime import datetime
import os

def get_profile_session(profile_name):
    try:
        session = boto3.Session(profile_name=profile_name)
        # Test the credentials
        session.client('sts').get_caller_identity()
        return session
    except ProfileNotFound:
        print(f"Error: AWS Profile '{profile_name}' not found!")
        sys.exit(1)
    except Exception as e:
        print(f"Error connecting with profile '{profile_name}': {str(e)}")
        sys.exit(1)

def get_all_regions(session, default_region='us-east-1'):
    # Initialize EC2 client with a default region
    ec2_client = session.client('ec2', region_name=default_region)
    return [region['RegionName'] for region in ec2_client.describe_regions()['Regions']]

def get_all_rds_instances(session, output_file, source_region):
    # Get list of all regions using the session
    regions = get_all_regions(session, source_region)
    
    # Function to write to both console and file
    def write_output(message):
        print(message)
        output_file.write(message + "\n")
    
    # Iterate through each region
    for region in regions:
        write_output(f"\nRegion: {region}")
        write_output("=" * 50)
        
        try:
            # Create RDS client for the current region using the session
            rds_client = session.client('rds', region_name=region)
            
            # Get all DB instances in the current region
            instances = rds_client.describe_db_instances()
            
            if not instances['DBInstances']:
                write_output("No RDS instances found")
                continue
                
            # Print details for each instance
            for instance in instances['DBInstances']:
                write_output(f"DB Identifier: {instance['DBInstanceIdentifier']}")
                write_output(f"DB Type: {instance['Engine']} {instance['EngineVersion']}")
                write_output(f"Status: {instance['DBInstanceStatus']}")
                write_output(f"Size: {instance['DBInstanceClass']}")
                write_output(f"Storage: {instance['AllocatedStorage']} GB")
                write_output(f"Endpoint: {instance.get('Endpoint', {}).get('Address', 'N/A')}")
                write_output(f"Created: {instance['InstanceCreateTime'].strftime('%Y-%m-%d %H:%M:%S')}")
                write_output(f"Multi-AZ: {instance['MultiAZ']}")
                write_output(f"Public Accessible: {instance['PubliclyAccessible']}")
                write_output("------------------------")
                
        except Exception as e:
            write_output(f"Error in region {region}: {str(e)}")

def main():
    # Create filename with current date
    current_date = datetime.now().strftime('%Y%m%d')
    filename = f"rds-inventory-{current_date}.txt"
    
    # Get available profiles
    available_profiles = boto3.Session().available_profiles
    
    if not available_profiles:
        print("No AWS profiles found. Please configure AWS credentials first.")
        sys.exit(1)

    # Print available profiles
    print("Available AWS Profiles:")
    for profile in available_profiles:
        print(f"- {profile}")
    
    # Prompt for profile name
    profile_name = input("\nEnter AWS profile name to use: ").strip()
    
    if profile_name not in available_profiles:
        print(f"Error: Profile '{profile_name}' not found in available profiles!")
        sys.exit(1)
    
    # Get session with the selected profile
    session = get_profile_session(profile_name)
    
    # Get available regions and prompt for source region
    # Use us-east-1 initially to get list of regions
    available_regions = get_all_regions(session, 'us-east-1')
    print("\nAvailable Regions:")
    for region in available_regions:
        print(f"- {region}")
    
    while True:
        source_region = input("\nEnter the region you are running this script from: ").strip()
        if source_region in available_regions:
            break
        print(f"Error: '{source_region}' is not a valid region. Please choose from the list above.")
    
    print(f"\nUsing AWS Profile: {profile_name}")
    print(f"Source Region: {source_region}")
    
    # Open file and get RDS instances
    with open(filename, 'w') as output_file:
        # Write header information
        header = (f"RDS Inventory Report\n"
                 f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                 f"AWS Profile: {profile_name}\n"
                 f"Source Region: {source_region}\n")
        print(header)
        output_file.write(header)
        
        # Get RDS instances using the session
        get_all_rds_instances(session, output_file, source_region)
    
    print(f"\nInventory has been saved to: {os.path.abspath(filename)}")

if __name__ == "__main__":
    main()