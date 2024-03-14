import boto3
import subprocess
import re

def list_tables_in_cluster(cluster_id, region, username, password, database_name, aws_profile):
    # Create an RDS client
    session = boto3.Session(profile_name=aws_profile)
    rds_client = session.client('rds', region_name=region)

    # Describe the DB clusters to get the cluster endpoint
    print("constructing db cluster response...",end="\n")
    response = rds_client.describe_db_clusters(DBClusterIdentifier=cluster_id)
    print("Response:", response)  # Debug output
    print("\n")

    # Extract the cluster endpoint
    print("constructing db cluster endpoint string...")
    endpoint_string = response['DBClusters'][0]['Endpoint']
    print("Endpoint String:", endpoint_string)  # Debug output
    print("\n")

    # cluster_endpoint = None  # Initialize cluster_endpoint

    # Extract address and port using regular expressions
    # print("constructing cluster endpoint...")
    # match = re.match(r'^(.*?):(\d+)$', endpoint_string)  # : in required
    # if match:
    #     address, port = match.group(1), match.group(2)
    #     cluster_endpoint = {'Address': address, 'Port': port}
    #     print("Cluster Endpoint:", cluster_endpoint)  # Debug output
    # else:
    #     print("Error: Unable to extract address and port from endpoint")
    #     # Handle the case where address and port cannot be extracted

    # Ensure that cluster_endpoint is defined before using it
    if endpoint_string:
        # Construct the connection string for MySQL client
        print("constructing connection string...")
        # connection_string = f"mysql -h {cluster_endpoint['Address']} -P {cluster_endpoint['Port']} -u {username} -p{password}"
        connection_string = "mysql -h {} -u {} -p{}".format(endpoint_string,username,password)
        print("db connection string is: ")
        print(connection_string)
        print("\n")
    else:
        print("Error: Unable to construct connection string because cluster_endpoint is not defined")
        # Handle the case where cluster_endpoint is not defined


    # List tables using MySQL client
    # command = f"mysql -h {cluster_endpoint['Address']} -P {cluster_endpoint['Port']} -u {username} -p'{password}' -e 'use {database_name}; show tables;'"
    command = f"{connection_string} -e 'use {database_name}; show tables;'"
    tables = subprocess.check_output(command, shell=True).decode('utf-8')
    
    # Print the tables
    print("Tables in the database:")
    print(tables)

def main():
    # Prompt user for input
    aws_profile = input("Enter your AWS profile name: ")
    cluster_id = input("Enter the cluster ID: ")
    region = input("Enter the region: ")
    username = input("Enter the username: ")
    password = input("Enter the password: ")
    database_name = input("Enter the database name: ")

    # Call function with user-provided inputs
    list_tables_in_cluster(cluster_id, region, username, password, database_name, aws_profile)

if __name__ == "__main__":
    main()