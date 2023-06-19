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
parser = argparse.ArgumentParser(description='Split row-based file into two')
# Paths must be passed in, not hardcoded
parser.add_argument('--input-file-path',
                    type=str,
                    required=True,
                    help='Path of the file to be truncated.')
parser.add_argument('--split-file-1-path',
                    type=str,
                    required=True,
                    help='Path of the first file where ~50% of the data is stored.')
parser.add_argument('--split-file-2-path',
                    type=str,
                    required=True,
                    help='Path of the second file where ~50% of the data is stored.')

args = parser.parse_args()

print('Input arguments:')
print(args)

# Create the directory where the output file is created (the directory
# may or may not exist).
try:
    output_dir = Path(args.input_file_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)
    output_dir = Path(args.split_file_1_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)
    output_dir = Path(args.split_file_2_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)
except Exception as ex:
    raise RuntimeError(f'Error creating output directory {output_dir}: {ex}')

try:
    with open(args.input_file_path, 'r') as input_file:
        with open(args.split_file_1_path, 'w') as output_file_1:
            with open(args.split_file_2_path, 'w') as output_file_2:
                odd = True
                row_count_file_1 = 0
                row_count_file_2 = 0
                for line in input_file:
                    if odd:
                        output_file_1.write(line)
                        row_count_file_1 += 1
                    else:
                        output_file_2.write(line)
                        row_count_file_2 += 1
                    odd = not odd

    print(f'Split file 1 {args.split_file_1_path} contains {row_count_file_1} rows.')
    print(f'Split file 2 {args.split_file_2_path} contains {row_count_file_2} rows.')

except Exception as ex:
    raise RuntimeError(f'Error splitting file {args.input_file_path}: {ex}')
