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

import json
import logging
from pathlib import Path
from typing import Dict
from typing import List

from elyra.metadata.schema import SchemasProvider


class ExamplesSchemasProvider(SchemasProvider):
    """
    Provides access to example custom components
    for Kubeflow Pipelines and Apache Airflow.
    """

    def get_schemas(self) -> List[Dict]:
        """
        Return the example schema
        """
        # use Elyra logger
        log = logging.getLogger('ElyraApp')
        examples_catalog_schema_defs = []
        try:
            # load examples schema definition
            examples_catalog_connector_schema_file = Path(__file__).parent / 'elyra-kfp-catalog.json'
            log.debug(f'Reading examples catalog connector schema from {examples_catalog_connector_schema_file}')
            with open(examples_catalog_connector_schema_file, 'r') as fp:
                examples_catalog_connector_schema = json.load(fp)
                examples_catalog_schema_defs.append(examples_catalog_connector_schema)
        except Exception as ex:
            log.error(f'Error reading examples catalog connector schema {examples_catalog_connector_schema_file}: {ex}')

        return examples_catalog_schema_defs
