#!/bin/bash

# Prompt the user for the YAML file name
read -p "Please enter the YAML file name: " yaml_file

# Check if the file exists
if [ ! -f "$yaml_file" ]; then
  echo "Error: File '$yaml_file' not found."
  exit 1
fi

# Use yq to extract email addresses of people with MySQL roles
emails=$(yq e '.[] | select(.mysql.roles) | .email' "$yaml_file")

# Print the list of email addresses
echo "People with MySQL roles:"
echo "$emails"