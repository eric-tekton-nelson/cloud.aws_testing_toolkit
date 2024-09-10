import boto3
import os

# Prompt the user for AWS SSO profile, region, and S3 bucket name
aws_profile = input("Enter your AWS SSO profile name: ")
aws_region = input("Enter the AWS region (e.g., us-east-1): ")
bucket_name = input("Enter the S3 bucket name: ")

# Set AWS profile and region
os.environ['AWS_PROFILE'] = aws_profile
os.environ['AWS_REGION'] = aws_region

# Initialize a session using boto3
session = boto3.Session(profile_name=aws_profile, region_name=aws_region)
s3 = session.client('s3')

# Define the lifecycle policy with Expiration days set to (3 years)
lifecycle_policy = {
    'Rules': [
        {
            'ID': 'Life Cycle for S3 versioned data older than 90 days and then transitioned to Glacier for 3 yrs',
            'Status': 'Enabled',
            'Filter': {
                'Prefix': ""  # Applies the rule to all objects in the bucket
            },
            'NoncurrentVersionExpiration': {
                'NoncurrentDays': 365,  # Expire non-current versions after 1 year
                'NewerNoncurrentVersions': 10
            },
            'NoncurrentVersionTransitions': [
                {
                    'NoncurrentDays': 90,  # Transition non-current versions to Glacier after 90 days
                    'StorageClass': 'GLACIER_IR'
                }
            ],
            'Expiration': {
                'Days': 1096  # Expiration set to (3 years) for current versions
            }
        }
    ]
}

# Function to enable versioning for the S3 bucket
def enable_versioning(bucket_name):
    try:
        response = s3.put_bucket_versioning(
            Bucket=bucket_name,
            VersioningConfiguration={
                'Status': 'Enabled'
            }
        )
        print(f'Versioning enabled for bucket: {bucket_name}')
    except Exception as e:
        print(f'Error enabling versioning: {e}')

# Function to apply lifecycle policy to the S3 bucket
def apply_lifecycle_policy(bucket_name):
    try:
        response = s3.put_bucket_lifecycle_configuration(
            Bucket=bucket_name,
            LifecycleConfiguration=lifecycle_policy
        )
        print(f'Lifecycle policy applied successfully to {bucket_name}.')
    except Exception as e:
        print(f'Error applying lifecycle policy: {e}')

# Enable versioning and apply lifecycle policy
enable_versioning(bucket_name)
apply_lifecycle_policy(bucket_name)
