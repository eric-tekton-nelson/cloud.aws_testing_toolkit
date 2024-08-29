import json
import csv

def extract_failures(json_file, csv_file):
    # Read the JSON data from the file
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    # Navigate to the "fail" results
    fail_results = data.get("response", {}).get("data", {}).get("results", {}).get("fail", [])
    
    # Open the CSV file for writing
    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        
        # Write the header
        header = ['id', 'name', 'resourceType', 'displayName', 'accountId']
        writer.writerow(header)
        
        # Write the fail results
        for item in fail_results:
            row = [
                item.get('id', ''),
                item.get('name', ''),
                item.get('resourceType', ''),
                item.get('displayName', ''),
                item.get('accountId', '')
            ]
            writer.writerow(row)

if __name__ == "__main__":
    # Prompt the user for the JSON input file and the CSV output file
    json_file = input("Enter the JSON input file name (including .json extension): ")
    csv_file = input("Enter the desired CSV output file name (including .csv extension): ")
    
    # Convert JSON to CSV
    try:
        extract_failures(json_file, csv_file)
        print(f"Successfully converted fail results from {json_file} to {csv_file}")
    except FileNotFoundError:
        print(f"Error: The file {json_file} does not exist. Please check the file name and try again.")
    except json.JSONDecodeError:
        print(f"Error: The file {json_file} is not a valid JSON file. Please check the file content and try again.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
