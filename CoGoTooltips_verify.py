import os
import sys
import argparse
import json
import re

# constant for converting json URLs to local files.
ASSET_PREFIX = "file:///android_asset/CoGoTooltips/"


def verify_json_file(json_path):
    """Process one JSON file, outputting a report file for each tool tip link."""
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            tooltips = json.load(f)
    except Exception as err:
        sys.stderr.write(f"Error loading JSON file {json_path}: {err}\n")
        return

    # Create separate output file for this JSON file.
    base_name = os.path.splitext(os.path.basename(json_path))[0]
    out_filename = base_name + "_verified_links.txt"

    # Open output file for writing.
    with open(out_filename, 'w', encoding='utf-8') as outf:
        for tip in tooltips:
            # Each tooltip should have a "tag", "category" and "buttons"
            tag = tip.get("tag", "UNKNOWN")
            category = tip.get("category", "UNKNOWN")
            buttons = tip.get("buttons", [])
            for button in buttons:
                # Expect each button to be an array with at least two elements:
                if not isinstance(button, list) or len(button) < 2:
                    continue
                url = button[1]
                # For URLs starting with "file:///android_asset/", remove the prefix.
                if url.startswith(ASSET_PREFIX):
                    local_path = url[len(ASSET_PREFIX):]
                else:
                    local_path = url  # leave as-is

                local_path = local_path.split("#")[0].encode('ascii', 'ignore').decode()

                # Check that this file exists relative to the current working directory.
                if os.path.exists(local_path):
                    status = "exists"
                else:
                    status = "missing"

                # Write the report line:
                # URL    status    tag, category
                outf.write(f"{url}\t{status}\t{tag} / {category}\n")
    print(f"Processed JSON file '{json_path}'; results written to '{out_filename}'.")


def verify_doc_dir(doc_dir):
    """Process one documentation directory:
       scan all HTML files for relative links; verify that each file exists.
       Writes a report file with one entry per link.
    """
    if not os.path.isdir(doc_dir):
        sys.stderr.write(f"Documentation directory not found: {doc_dir}\n")
        return

    # Determine an output file name based on the directory name.
    dir_name = os.path.basename(os.path.normpath(doc_dir))
    out_filename = dir_name + "_internal_links.txt"

    # Regex for finding href="...". (This is basic and may be adjusted for your HTML.)
    href_re = re.compile(r'href="([^"]+)"')

    with open(out_filename, 'w', encoding='utf-8') as outf:
        # Walk the directory recursively.
        for root, dirs, files in os.walk(doc_dir):
            for fname in files:
                if not fname.lower().endswith('.html'):
                    continue
                html_path = os.path.join(root, fname)
                try:
                    with open(html_path, 'r', encoding='utf-8') as html_file:
                        content = html_file.read()
                except Exception as e:
                    sys.stderr.write(f"Error reading {html_path}: {e}\n")
                    continue

                # Look for all href values.
                links = href_re.findall(content)
                for link in links:
                    # Skip if link is an external URL (http, https, mailto, etc.)
                    if re.match(r'^(https?:|mailto:|#)', link):
                        continue

                    link = link.split("#")[0].encode('ascii', 'ignore').decode()

                    # Determine the file to check by joining with the directory of the html file.
                    # Note: We use os.path.join on the directory of html file.
                    linked_path = os.path.normpath(os.path.join(os.path.dirname(html_path), link))

                    # Check for existence.
                    if os.path.exists(linked_path):
                        status = "exists"
                    else:
                        status = "missing"

                    # Write report line: URL, status, location of html file (absolute or relative to doc_dir)
                    # For clarity, we output the html path relative to the doc_dir.
                    rel_html_path = os.path.relpath(html_path, doc_dir)
                    outf.write(f"{link}\t{status}\t{rel_html_path}\n")

    print(f"Processed documentation dir '{doc_dir}'; results written to '{out_filename}'.")


def main():
    parser = argparse.ArgumentParser(
        description="Verify the integrity of internal links in tooltip JSON files and HTML documentation directories."
    )
    parser.add_argument(
        "--json-files",
        type=str,
        help="Comma-separated list of JSON file paths containing tooltip objects.",
        required=False,
        default=""
    )

    parser.add_argument(
        "--doc-dirs",
        type=str,
        help="Comma-separated list of documentation directories (HTML files) to check internal relative links.",
        required=False,
        default=""
    )

    args = parser.parse_args()

    # Process JSON files if provided.
    if args.json_files:
        json_files = [x.strip() for x in args.json_files.split(",") if x.strip()]
        for jf in json_files:
            verify_json_file(jf)

    # Process documentation directories if provided.
    if args.doc_dirs:
        doc_dirs = [x.strip() for x in args.doc_dirs.split(",") if x.strip()]
        for dd in doc_dirs:
            verify_doc_dir(dd)


if __name__ == "__main__":
    main()
