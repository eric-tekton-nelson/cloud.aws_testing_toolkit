import csv

# Prompt the user for the input and output file names
input_file_path = input("Enter the name of the input text file (e.g., instances.txt): ")
output_file_path = input("Enter the name of the output CSV file (e.g., instances.csv): ")

try:
    # Read the text file
    with open(input_file_path, 'r') as file:
        lines = file.readlines()

    # Process the lines to remove the prefix "EC2 / ", unnecessary whitespace, and blank lines
    instance_ids = []
    for line in lines:
        stripped_line = line.strip()
        if stripped_line.startswith("EC2 / "):
            instance_id = stripped_line[len("EC2 / "):]
        else:
            instance_id = stripped_line
        if instance_id:
            instance_ids.append(instance_id)

    # Write the instance IDs to a CSV file
    with open(output_file_path, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        # Write header row
        csvwriter.writerow(['Instance ID'])
        # Write instance IDs
        for instance_id in instance_ids:
            csvwriter.writerow([instance_id])

    print(f"CSV file '{output_file_path}' has been created successfully.")

except FileNotFoundError:
    print(f"Error: The file '{input_file_path}' does not exist. Please check the file name and try again.")
except Exception as e:
    print(f"An error occurred: {e}")
