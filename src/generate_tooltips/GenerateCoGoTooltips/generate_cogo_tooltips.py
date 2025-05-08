import argparse
import csv
import json
import os
import sys

def main():
    parser = argparse.ArgumentParser(
        prog='generate_manual_tooltips.py',
        description='Generates tooltips for Code On The Go from the Java API documentation.')
    parser.add_argument('--out-file', help='Path to root directory of the Java API documentation.',
                        required=True)
    parser.add_argument('--input-json', help='Comma-separated list of tooltip JSON files to include in JSON output alongside Java tooltips.',
                        required=True)
    args = parser.parse_args()

    java_classes_tooltips_path = os.path.join('java_docs_tooltips', 'out', 'classes.json')
    java_modules_tooltips_path = os.path.join('java_docs_tooltips', 'out', 'modules.json')
    java_packages_tooltips_path = os.path.join('java_docs_tooltips', 'out', 'packages.json')

    with open(java_classes_tooltips_path, 'r') as file:
        classes_data = json.load(file)
    with open(java_modules_tooltips_path, 'r') as file:
        modules_data = json.load(file)
    with open(java_packages_tooltips_path, 'r') as file:
        packages_data = json.load(file)
    with open(args.input_json, 'r') as file:
        internal_data = json.load(file)

    tooltips_file_path = "CoGoTooltips.json"

    json_dump = json.dumps([e for e in modules_data + packages_data + classes_data + internal_data], indent=4)
    open(tooltips_file_path, "w", encoding='utf-8').write(json_dump)

    print("Combined class tooltips with internally-written tooltips in " + tooltips_file_path)

if __name__ == "__main__":
    main()