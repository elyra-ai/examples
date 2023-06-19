#!/usr/bin/env python3
#
# Copyright 2018-2023 Elyra Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import argparse
from pathlib import Path


# Defining and parsing the command-line arguments
parser = argparse.ArgumentParser(description='Count rows in input file')
# Paths must be passed in, not hardcoded
parser.add_argument('--input-file-path',
                    type=str,
                    required=True,
                    help='Path of the file to be truncated.')
parser.add_argument('--truncated-file-path',
                    type=str,
                    required=True,
                    help='Path of the file where the truncated file is stored.')
parser.add_argument('--max-rows-value',
                    type=int,
                    default=100,
                    help='The number of rows to read from the input and write to the output.')

args = parser.parse_args()

print('Input arguments:')
print(args)

# Create the directory where the output file is created (the directory
# may or may not exist).
output_dir = Path(args.truncated_file_path).parent
try:
    output_dir.mkdir(parents=True, exist_ok=True)
except Exception as ex:
    raise RuntimeError(f'Error creating output directory {output_dir}: {ex}')

count = 0
try:
    with open(args.input_file_path, 'r') as input_file:
        with open(args.truncated_file_path, 'w') as output_file:
            for line in input_file:
                count += 1
                if count > args.max_rows_value:
                    break
                output_file.write(line)
            if count > 0:
                count -= 1
    print(f'Truncated {args.input_file_path} after {count} rows.')
except Exception as ex:
    raise RuntimeError(f'Error truncating file {args.input_file_path}: {ex}')
