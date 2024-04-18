#!/bin/bash

# install prerequisites
sudo apt-get update && sudo apt-get -y upgrade
# sudo apt-get -y install git binutils

# Adding amazon EFS repository - do this in dev directory
# git clone https://github.com/aws/efs-utils
# navigate to dev directory: cd /path/efs-utils
# ./build-deb.sh
# sudo apt-get -y install ./build/amazon-efs-utils*deb

# now install amazon-efs-utils should run cleanly
# sudo apt-get update
# sudo apt-get -y install amazon-efs-utils

# mount using Amazon EFS mount helper (get fs id from EFS details)
# No clue why, but this does not work, maybe issue with ubuntu
# mkdir ~/efs-dir  # EFS mount point dir
# sudo mount -t efs -o tls fs-06a3f05c08ae04b64.efs.us-east-2.amazonaws.com:/ ~/efs-dir

# mount using nfs4 utility
# this command can be found when selecting the "attach" button in EFS page on console
sudo mount -t nfs4 -o nfsvers=4.1,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2,noresvport 10.0.3.108:/ ~/efs-dir

# Unmount EFS file system
# sudo umoint ~/efs-dir