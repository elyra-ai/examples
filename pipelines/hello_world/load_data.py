#
# Copyright 2020 IBM Corporation
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
import os
from pathlib import Path
import requests
import tarfile
from urllib.parse import urlparse


if os.environ.get('DATASET_URL') is None:
    raise RuntimeError('Cannot run script. Required environment variable DATASET_URL is not defined.')
    
data_file = os.environ['DATASET_URL']

data_dir_name = 'data'

print('Downloading data file {} ...'.format(data_file))
r = requests.get(data_file)
if r.status_code != 200:
    raise RuntimeError('Could not fetch {}: HTTP status code {}'.format(data_file, r.status_code))
else:
    # extract data set file name from URL 
    data_file_name = Path((urlparse(data_file).path)).name
    # create the directory where the downloaded file will be stored
    data_dir = Path(data_dir_name)    
    data_dir.mkdir(parents=True, exist_ok=True)
    downloaded_data_file = data_dir / data_file_name

    print('Saving downloaded file "{}" as ...'.format(data_file_name))
    with open(downloaded_data_file, 'wb') as downloaded_file:
        downloaded_file.write(r.content)
    
    if r.headers['content-type'] == 'application/x-tar':
        print('Extracting downloaded file in directory "{}" ...'.format(data_dir))
        with tarfile.open(downloaded_data_file, 'r') as tar:
            tar.extractall(data_dir)
        print('Removing downloaded file ...')
        downloaded_data_file.unlink()