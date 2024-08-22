#!/bin/bash

aws ec2 describe-instances --region=<region> --filters "Name=instance-state-name,Values=running" --query "Reservations[*].Instances[*].[InstanceId,InstanceType,Tags[?Key=='Name'].Value|[0],PrivateIpAddress]" --output table --profile=<aws+profile> >> describe_ec2.txt
