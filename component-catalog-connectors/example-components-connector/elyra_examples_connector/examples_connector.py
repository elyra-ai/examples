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


class ExamplesCatalogConnector(ComponentCatalogConnector):
    """
    Makes example components for Kubeflow Pipelines and Apache Airflow
    available to Elyra.
    """
    config = {
        'kfp': {
            'root_dir': 'kfp_example_components',
            'file_filter': '*.yaml'
        },
        'airflow': {
            'root_dir': 'airflow_example_components',
            'file_filter': '*.py'
        }
    }

    def get_catalog_entries(self, catalog_metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Returns Elyra example custom components for the selected runtime (Kubeflow Pipelines
        and Apache Airflow only)
        :param registry_metadata: the dictionary-form of the Metadata instance for a single registry
        """
        component_list = []

        runtime_id = catalog_metadata.get('runtime')

        if runtime_id not in ExamplesCatalogConnector.config.keys():
            self.log.error(f'Cannot retrieve component list for runtime \'{runtime_id}\': '
                           f'only {list(ExamplesCatalogConnector.config.keys())} are supported.')
            # return empty component specification list
            return component_list

        try:
            root_dir = Path(__file__).parent / ExamplesCatalogConnector.config[runtime_id]['root_dir']
            self.log.debug(f"Retrieving component list for runtime '{catalog_metadata.get('runtime')}' from "
                           f'{root_dir}')
            pattern = ExamplesCatalogConnector.config[runtime_id].get('file_filter', '*')
            self.log.debug(f'Pattern: {pattern}')
            for file in root_dir.glob(f'**/{pattern}'):
                component_list.append({'component-id': str(file)[len(str(root_dir)) + 1:]})
            self.log.debug(f'Component list: {component_list}')
        except Exception as ex:
            self.log.error(f"Error retrieving component list for runtime '{catalog_metadata.get('runtime')}'"
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
            self.log.error('Cannot retrieve component specification: '
                           'A component id must be provided.')
            return None

        runtime_id = catalog_metadata.get('runtime')
        if runtime_id not in ExamplesCatalogConnector.config.keys():
            self.log.error(f'Cannot fetch component \'{component_id}\': '
                           f'only {list(ExamplesCatalogConnector.config.keys())} are supported.')
            return None

        try:
            root_dir = Path(__file__).parent / ExamplesCatalogConnector.config[runtime_id]['root_dir']
            with open(root_dir / component_id, 'r') as fp:
                return fp.read()
        except Exception as e:
            self.log.error(f'Failed to fetch component \'{component_id}\' '
                           f': {str(e)}')
            return None

    def get_hash_keys(self) -> List[Any]:
        """
        Identifies the key(s) that read_catalog_entry method
        requires to be present in the catalog_entry_data parameter
        to allow for retrieval of a component.

        :returns: a list of keys
      """
        return ['component-id']
