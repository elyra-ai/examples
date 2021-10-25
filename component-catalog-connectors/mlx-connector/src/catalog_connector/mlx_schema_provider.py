#
# Copyright 2018-2021 Elyra Authors
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

import json
from pathlib import Path
from typing import Dict
from typing import List

from elyra.metadata.schema import SchemasProvider


class MLXSchemasProvider(SchemasProvider):
    """
    Enables BYO catalog connector for the Machine Learning Exchange
    """

    def get_schemas(self) -> List[Dict]:
        """
        Return the MLX catalog connector schema
        """
        mlx_catalog_schema_defs = []
        try:
            mlx_catalog_connector_schema_file = Path(__file__) / 'schema' / 'mlx-catalog.json'
            print(f'Reading MLX catalog connector schema from {mlx_catalog_connector_schema_file}')
            with open(mlx_catalog_connector_schema_file, 'r') as fp:
                mlx_catalog_connector_schema = json.load(fp)
                mlx_catalog_schema_defs.append(mlx_catalog_connector_schema)
        except Exception as ex:
            print(f'Error reading MLX catalog connector schema {mlx_catalog_connector_schema_file}: {ex}')

        return mlx_catalog_schema_defs
