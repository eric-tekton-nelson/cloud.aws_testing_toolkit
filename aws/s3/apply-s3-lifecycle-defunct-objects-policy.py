import boto3
from botocore.exceptions import ProfileNotFound

def get_input(prompt):
    return input(prompt).strip()

def enable_bucket_versioning(s3, bucket_name):
    # Check the current versioning status
    try:
        versioning_status = s3.get_bucket_versioning(Bucket=bucket_name)
        if versioning_status.get('Status') == 'Enabled':
            print(f"Versioning is already enabled for {bucket_name}.")
        else:
            # Enable versioning if not enabled
            s3.put_bucket_versioning(
                Bucket=bucket_name,
                VersioningConfiguration={
                    'Status': 'Enabled'
                }
            )
            print(f"Versioning has been enabled for {bucket_name}.")
    except Exception as e:
        print(f"An error occurred while enabling versioning: {str(e)}")

def main():
    # Get inputs from the user
    bucket_name = get_input("Enter the S3 bucket name: ")
    profile_name = get_input("Enter the AWS SSO profile name: ")
    region_name = get_input("Enter the AWS region: ")

    # Set up the session with the specified profile and region
    try:
        session = boto3.Session(profile_name=profile_name, region_name=region_name)
        s3 = session.client('s3')
    except ProfileNotFound:
        print(f"The profile '{profile_name}' was not found. Please check the profile name.")
        return

    # Enable versioning for the bucket
    enable_bucket_versioning(s3, bucket_name)

    # Define the lifecycle policy
    lifecycle_policy = {
        "Rules": [
            {
                "ID": "Expire noncurrent with size less than 1 byte",
                "Filter": {
                    "ObjectSizeLessThan": 1
                },
                "Status": "Enabled",
                "NoncurrentVersionExpiration": {
                    "NewerNoncurrentVersions": 10,
                    "NoncurrentDays": 30
                }
            }
        ]
    }

    # Apply the lifecycle policy to the specified bucket
    try:
        s3.put_bucket_lifecycle_configuration(
            Bucket=bucket_name,
            LifecycleConfiguration=lifecycle_policy
        )
        print(f"Applied lifecycle policy to {bucket_name} in region {region_name} using profile {profile_name}.")
    except Exception as e:
        print(f"An error occurred while applying the lifecycle policy: {str(e)}")

if __name__ == "__main__":
    main()
