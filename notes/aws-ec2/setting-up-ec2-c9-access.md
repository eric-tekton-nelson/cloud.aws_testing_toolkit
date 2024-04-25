# Layout

## VPC

Setup a standard vpc with 2 pub subnets, 2 priv subnets, sgs, rts, and ngw as required.

## Cloud9 

Cloud9 cloudformation template will create a default security group for your c9 env

In:
- Config: HTTP, Port: 80, Source: pub sg that you will use for other test ec2s
- Config: SSH, Port: 20, Source: pub sg that you will use for other test ec2s

## Test EC2s

For testing purposes, just create simple free tier t2.micros, but add them to the security group below.

### create a security group for ec2 prior to creating ec2 instances

- Config: HTTP, Port: 80, Source: from c9 sg
- Config: SSH, Port: 20, Source: from c9 sg
- Config: custom TCP, Port 8181, Source: from c9 sg
- Config: HTTPS, Port 443, Source: all
- Config: All ICMP - IPv4, Port all, Source: from c9 sg
- Config: SSH, Port: 22, Source: local ip address xxx/32

# EC2 IAM profile

Before you create the test EC2s you need to create an IAM Instance Profile enabling 'AmazonSSMManagedInstanceCore' managed policy.

Select that IAM Instance Profile to enable EC2 Instance Connect via SSM

## testing

aws ssm describe-instance-information --instance-information-filter-list key=InstanceIds,valueSet=<instance-id>

## check security group for EC2

To ensure that the security group associated with your EC2 instance allows outbound traffic on port 443 (HTTPS) to communicate with AWS Systems Manager, you can follow these steps:

## Create VPC endpoint

Create a VPC endpoint specifically of type EC2 Instance Connect.  Then it will show up in the options for endpoint in EC2 Instance Connect diaglog.

## Reachability Analyzer

Check VPC Reachability Analyzer and run from Internet Gateway for VPC in question to specific EC2.  Run as TCP protocol.  Run analysis.

## Then I realized... why not use C9?

You can do everything you need via ssh between c9 instance and EC2 or other svcs.  First, just connect to EC2 via SSM Manager (not SSH or Instance Connect), there are two users: ssm-user, and ec2-user.  
Just switch to ec2-user and add ssh key to ~/.ssh.  Then you'll be able to ssh from c9.

Login:  `ssh -i ~/.ssh/id_ed25519_c9_token_20240417 ec2-user@10.0.1.XXX`

ssh -i ~/.ssh/id_ed25519_c9_token_20240417 ec2-user@10.0.1.159

# Tabs and line endings issues

If you paste python code from windows you get intentation errors.  

Windows:
Upper Right Preferences Cog>Code Editor (ACE)>New File Line Endings:
- Windows (CRLF) to end lines with a carriage return and then a line feed.

Unix/Linux:
Upper Right Preferences Cog>Code Editor (ACE)>New File Line Endings:
- Unix (LF) to end lines with just a line feed.

# Connecting to EC2 using SSM Session Manager

## Add EC2_Core_Functionality IAM role to EC2

- Make sure the IAM role has `AmazonSSMManagedInstanceCore` AWS Managed Policy
- Ensure that the EC2 instance is assigned an IAM role with the necessary permissions to interact with the Systems Manager. 
- This role should include policies that allow actions like ssm:SendCommand, ssm:GetParameters, and other related permissions.

## Make sure SSM Agent is running on client EC2

