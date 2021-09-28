#!/usr/bin/env python3
import argparse
from pathlib import Path

import requests


# Defining and parsing the command-line arguments
parser = argparse.ArgumentParser(description='Download file from public HTTP/S URL')
# Paths must be passed in, not hardcoded
parser.add_argument('--file-url',
                    type=str,
                    required=True,
                    help='Public URL of file to download')
parser.add_argument('--downloaded-file-path',
                    type=str,
                    required=True,
                    help='Path of the local file where the Output 1 data should be written.')
args = parser.parse_args()

print(f'Program arguments: {args}')

# Creating the directory where the output file is created (the directory
# may or may not exist).
output_dir = Path(args.downloaded_file_path).parent
try:
    output_dir.mkdir(parents=True, exist_ok=True)
except Exception as ex:
    raise RuntimeError(f'Error creating output directory {output_dir}: {ex}')

response = requests.get(url=args.file_url)
if response.status_code == 200:
    try:
        with open(args.downloaded_file_path, 'wb') as output_file:
            output_file.write(response.content)
    except OSError as ose:
        raise RuntimeError(f'Error creating output file '
                           f'{args.downloaded_file_path}: {ose}')
else:
    raise RuntimeError(f'Download of {args.file_url} returned HTTP status code {response.status_code}')
