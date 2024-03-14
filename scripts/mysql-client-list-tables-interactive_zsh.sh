#!/bin/zsh

# Prompt user for database connection details
echo -n "Enter Aurora DB endpoint: "
read host
echo -n "Enter Aurora DB port: "
read port
echo -n "Enter DB username: "
read user
echo -n "Enter DB password: "
read -s password
echo ""
echo -n "Enter DB name: "
read database

# MySQL command to list tables
mysql_command="SHOW TABLES;"

# Execute MySQL command
mysql_output=$(mysql -h "$host" -P "$port" -u "$user" -p"$password" -D "$database" -e "$mysql_command" 2>/dev/null)

# Check if MySQL command execution was successful
if [ $? -ne 0 ]; then
    echo "Error: Failed to execute MySQL command. Please check your connection details."
    exit 1
fi

# Print the list of tables
echo "Tables in $database:"
echo "$mysql_output"
