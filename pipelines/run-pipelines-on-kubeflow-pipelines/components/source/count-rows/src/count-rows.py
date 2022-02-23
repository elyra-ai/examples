#!/usr/bin/env python3
#
# Copyright 2018-2022 Elyra Authors
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
                    help='Path of the file to be processed.')
parser.add_argument('--row-count-path',
                    type=str,
                    required=True,
                    help='Path of the file where the file\'s row count is stored.')
args = parser.parse_args()

print('Input arguments:')
print(args)

# Creating the directory where the output file is created (the directory
# may or may not exist).
output_dir = Path(args.row_count_path).parent
try:
    output_dir.mkdir(parents=True, exist_ok=True)
except Exception as ex:
    raise RuntimeError(f'Error creating output directory {output_dir}: {ex}')

count = 0
with open(args.input_file_path, 'r') as input_file:
    for line in input_file:
        count += 1
print(f'Input file contains {count} lines')
with open(args.row_count_path, 'w') as output_file:
    output_file.write(str(count))
