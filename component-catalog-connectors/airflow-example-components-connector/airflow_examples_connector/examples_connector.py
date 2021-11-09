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

from pathlib import Path
from typing import Any
from typing import Dict
from typing import List
from typing import Optional


from elyra.pipeline.catalog_connector import ComponentCatalogConnector
from elyra.pipeline.runtime_type import RuntimeProcessorType


class ExamplesCatalogConnector(ComponentCatalogConnector):
    """
    Makes a curated set of components for Apache Airflow available to Elyra.
    """

    def get_catalog_entries(self, catalog_metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Returns list of components that are stored in the '/resources' directory
        :param registry_metadata: the dictionary-form of the Metadata instance for a single registry
        """
        component_list = []

        runtime_type_name = catalog_metadata.get('runtime_type')
        runtime_type = RuntimeProcessorType.get_instance_by_name(runtime_type_name)
        # The runtime type's user-friendly display name
        runtime_type_display_name = runtime_type.value

        if runtime_type != RuntimeProcessorType.APACHE_AIRFLOW:
            self.log.error(f'Cannot retrieve component list for runtime type \'{runtime_type_display_name}\': '
                           f'Only \'{RuntimeProcessorType.APACHE_AIRFLOW.value}\' is supported.')
            # return empty component specification list
            return component_list

        try:
            root_dir = Path(__file__).parent / 'resources'
            self.log.debug(f'Retrieving component list for runtime type \'{runtime_type_display_name}\' from '
                           f'{root_dir}')
            pattern = '**/*.py'
            self.log.debug(f'Component file pattern: {pattern}')
            for file in root_dir.glob(pattern):
                component_list.append({'component-id': str(file)[len(str(root_dir)) + 1:]})
            self.log.debug(f'Component list: {component_list}')
        except Exception as ex:
            self.log.error(f"Error retrieving component list for runtime type '{runtime_type_display_name}'"
                           f" from {root_dir}: {ex}")

        return component_list

    def read_catalog_entry(self,
                           catalog_entry_data: Dict[str, Any],
                           catalog_metadata: Dict[str, Any]) -> Optional[str]:
        """
        Retrieves a component from the catalog that is identified using
        the information provided in catalog_entry_data.

        :param catalog_entry_data: an entry that was returned by get_catalog_entries
        :type catalog_entry_data: Dict[str, Any]
        :param catalog_metadata: the schema instance metadata, as defined in elyra-examples-catalog.json
        :type catalog_metadata: Dict[str, Any]
        :return: the component specification, if found
        :rtype: Optional[str]
        """
        component_id = catalog_entry_data.get('component-id')
        if component_id is None:
            self.log.error('Cannot retrieve component: '
                           'A component id must be provided.')
            return None

        runtime_type_name = catalog_metadata.get('runtime_type')
        runtime_type = RuntimeProcessorType.get_instance_by_name(runtime_type_name)
        # The runtime type's user-friendly display name
        runtime_type_display_name = runtime_type.value

        if runtime_type != RuntimeProcessorType.APACHE_AIRFLOW:
            self.log.error(f'Cannot retrieve component for runtime type \'{runtime_type_name}\': '
                           f'Only \'{RuntimeProcessorType.APACHE_AIRFLOW.value}\' is supported.')

        try:
            # load component from resources directory
            root_dir = Path(__file__).parent / 'resources'
            self.log.debug(f'Retrieving component of runtime type \'{runtime_type_display_name}\' from '
                           f'{root_dir}')
            with open(root_dir / component_id, 'r') as fp:
                return fp.read()
        except Exception as e:
            self.log.error(f'Failed to fetch component \'{component_id}\' '
                           f' from \'{root_dir}\': {str(e)}')
            return None

    def get_hash_keys(self) -> List[Any]:
        """
        Identifies the key(s) that read_catalog_entry method
        requires to be present in the catalog_entry_data parameter
        to allow for retrieval of a component.

        :returns: a list of keys
      """
        return ['component-id']
