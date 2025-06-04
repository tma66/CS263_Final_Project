import argparse
import json
import yaml
from pprint import pprint

def parse_json(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data
    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {e}")
        exit(1)

def parse_yaml(file_path):
    try:
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
            return data
    except yaml.YAMLError as e:
        print(f"Invalid YAML: {e}")
        exit(1)

def main():
    parser = argparse.ArgumentParser(description='Parse JSON or YAML input files and perform actions based on contents')
    parser.add_argument('file_path', type=str, help='Path to the JSON or YAML file')
    args = parser.parse_args()

    if args.file_path.endswith('.json'):
        data = parse_json(args.file_path)
    elif args.file_path.endswith('.yaml') or args.file_path.endswith('.yml'):
        data = parse_yaml(args.file_path)
    else:
        print(f"Unsupported file type: {args.file_path}")
        exit(1)

    pprint(data)

if __name__ == '__main__':
    main()