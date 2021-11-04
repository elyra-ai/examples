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

from glob import glob
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
            'root_dir': 'kfp_examples_components',
            'file_filter': '*.yaml'
        }
    }

    def get_catalog_entries(self, catalog_metadata: Dict[str, Any]) -> List[Dict[str, Any]]:

        """
        Returns Elyra example custom components for the selected runtime (Kubeflow Pipelines
        and Apache Airflow only)
        :param registry_metadata: the dictionary-form of the Metadata instance for a single registry
        """
        component_list = []

        if catalog_metadata.get('runtime') not in ExamplesCatalogConnector.config.keys():
            self.log.error('Example custom components are only available for Kubeflow Pipelines '
                           'and Apache Airflow.')
            # return empty component specification list
            return component_list

        try:
            root_dir = Path(__file__).parent / ExamplesCatalogConnector.config[catalog_metadata.get('runtime')]
            self.log.info(f"Retrieving component list for runtime '{catalog_metadata.get('runtime')}' from "
                          f'{root_dir}')
            file_spec = ExamplesCatalogConnector.config[catalog_metadata.get('runtime')].get('file_filter', '*')
            for file in glob.iglob(root_dir / '**' / file_spec):
                component_list.append({'component-id': file})

            self.log.info(f'Component list: {component_list}')

        except Exception as ex:
            self.log.warning(f"Error retrieving component list for runtime '{catalog_metadata.get('runtime')}'"
                             f" from {root_dir}: {ex}")

        return component_list

    def read_catalog_entry(self,
                           catalog_entry_data: Dict[str, Any],
                           catalog_metadata: Dict[str, Any]) -> Optional[str]:
        """
        Read a component definition for a single catalog entry using the its data (as returned from
        get_catalog_entries()) and the catalog metadata, if needed

        :param catalog_entry_data: a dictionary that contains the information needed to read the content
                                   of the component definition
        :param catalog_metadata: the metadata associated with the catalog in which this catalog entry is
                                 stored; in addition to catalog_entry_data, catalog_metadata may also be
                                 needed to read the component definition for certain types of catalogs

        :returns: the requested component specification, if it exists
        """

        component_id = catalog_entry_data['component-id']
        if component_id is None:
            self.log.error('Cannot retrieve example component specification: '
                           'A component id must be provided.')
            return None

        try:
            with open(component_id, 'r') as fp:
                return fp.read()
        except Exception as e:
            self.log.error(f'Failed to download component specification {component_id} '
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
