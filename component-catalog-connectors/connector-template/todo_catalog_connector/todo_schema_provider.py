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
import logging
from pathlib import Path
from typing import Dict
from typing import List

from elyra.metadata.schema import SchemasProvider

"""
 Customize this template file as necessary. At a minimum all occurrences
 of '<TODO-...>', 'TODO', and 'todo' must be replaced.
"""


class TODOSchemasProvider(SchemasProvider):
    """
    Enables catalog connector for <TODO-CATALOG-TYPE>
    """

    def get_schemas(self) -> List[Dict]:
        """
        Return the <TODO-CATALOG-TYPE> catalog connector schema
        """
        # use Elyra logger
        log = logging.getLogger('ElyraApp')
        catalog_schema_defs = []
        try:
            # load <TODO-CATALOG-TYPE> catalog schema definition
            catalog_connector_schema_file = Path(__file__).parent / 'TODO-catalog.json'
            log.debug(f'Reading <TODO-CATALOG-TYPE> catalog connector schema from {catalog_connector_schema_file}')
            with open(catalog_connector_schema_file, 'r') as fp:
                catalog_connector_schema = json.load(fp)
                catalog_schema_defs.append(catalog_connector_schema)
        except Exception as ex:
            log.error('Error reading <TODO-CATALOG-TYPE> catalog connector '
                      f'schema {catalog_connector_schema_file}: {ex}')

        return catalog_schema_defs
