#!/bin/bash

# Copy public key to distance EC2 instance
ssh-copy-id -i ~/.ssh/id_rsa.pub username@ec2-instance-ip

# Connect over ssh with key file "-i"
ssh -i ~/.ssh/path_to_c9_private_key_file ec2-user@10.0.x.x