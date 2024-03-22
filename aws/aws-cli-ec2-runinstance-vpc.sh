#!/bin/bash
# Based on VPC vpc-0e47dee32a67e7219 / main-ue2-vpc-0001

# Launch instances in mue2-public-az2a
aws ec2 run-instances --image-id <ami-image> --instance-type <type> --security-group-ids <sg-id> --subnet-id <subnet> --key-name <kms-key-id> --user-data file://<path>

# Launch instances in mue2-public-az2b
aws ec2 run-instances --image-id <ami-image> --instance-type <type> --security-group-ids <sg-id> --subnet-id <subnet> --key-name <kms-key-id> --user-data file://<path>

# Launch instances in mue2-private-az2a
aws ec2 run-instances --image-id <ami-image> --instance-type <type> --security-group-ids <sg-id> --subnet-id <subnet> --key-name <kms-key-id> --user-data file://<path>

# Terminate instances
aws ec2 terminate-instances --instance-ids <value> <value>
