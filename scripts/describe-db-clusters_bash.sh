#!/bin/bash

# Define a function to retrieve and save RDS clusters information
get_rds_clusters_info() {
    # Get current date and time in the format YYYY-MM-DD-HH-MM-SS
    current_datetime=$(date +%Y-%m-%d-%H-%M-%S)
    
    # Execute AWS CLI command and save output to a file with current date and time
    aws rds describe-db-clusters --region us-east-1 --profile admin_production | tail -n +2 > "${current_datetime}_clusters.json"
}

# Execute the function
get_rds_clusters_info

