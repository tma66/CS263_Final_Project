import sys
import json
import yaml

def parse_file(file_path):
    with open(file_path, 'r') as file:
        if file_path.endswith('.json'):
            return json.load(file)
        elif file_path.endswith('.yaml') or file_path.endswith('.yml'):
            return yaml.safe_load(file)
        else:
            raise ValueError("Unsupported file format. Please provide a JSON or YAML file.")

def perform_actions(data):
    # Example action: print the data
    print(data)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: python script.py <file_path>")
    
    file_path = sys.argv[1]
    try:
        data = parse_file(file_path)
        perform_actions(data)
    except Exception as e:
        sys.exit(f"Error: {e}")