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
import os
import requests

data_file_url = os.getenv(
    "DATASET_URL",
    "https://raw.githubusercontent.com/elyra-ai/examples/"
    "main/pipelines/introduction-to-generic-pipelines/data/iris.data",
)

# Download the dataset
print(f"Downloading data file {data_file_url} ...")
r = requests.get(data_file_url)
if r.status_code != 200:
    raise RuntimeError(
        f"Error downloading {data_file_url}: HTTP status code {r.status_code}"
    )

# Save the dataset
datafile_name = "iris.data"
with open(datafile_name, "w") as downloaded_file:
    downloaded_file.write(r.text)
print(f"Saved data file as {datafile_name}.")
