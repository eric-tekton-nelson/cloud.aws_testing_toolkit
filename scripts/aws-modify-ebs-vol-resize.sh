#!/bin/bash

# aws ec2 modify-volume --volume-id your-volume-id --size your-new-size
aws ec2 modify-volume --volume-id vol-08c199f10c7f7bd29 --size 100GiB
