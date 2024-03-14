#!/bin/zsh

# Prompt for AWS profile name
read -p "Enter AWS profile name: " profile_name

# Prompt for DB cluster identifier
read -p "Enter DB cluster identifier: " db_cluster_identifier

# Prompt for new master password
read -s -p "Enter new master password: " new_password
echo

# Change the password
echo "Changing the master password..."
aws rds modify-db-cluster --db-cluster-identifier $db_cluster_identifier --master-user-password $new_password --profile $profile_name

if [ $? -eq 0 ]; then
    echo "Password changed successfully."
else
    echo "Failed to change the password. Please check your inputs and try again."
fi
