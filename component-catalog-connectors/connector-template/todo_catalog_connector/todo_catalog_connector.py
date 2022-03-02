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

from pathlib import Path
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from elyra.pipeline.catalog_connector import ComponentCatalogConnector
from elyra.pipeline.catalog_connector import EntryData

"""
 Customize this template file as necessary. At a minimum all occurrences
 of '<TODO-...>', 'TODO', and 'todo' must be replaced.
"""


class TODOComponentCatalogConnector(ComponentCatalogConnector):
    """
    Read component definitions from a <TODO> catalog
    """

    def get_catalog_entries(self, catalog_metadata: Dict[str, Any]) -> List[Dict[str, Any]]:

        """
        Returns a list of component_metadata instances, one per component found in the given registry.
        The form that component_metadata takes is determined by requirements of the reader class.

        :param registry_metadata: the dictionary-form of the Metadata instance for a single registry
        """
        component_list = []

        # Load user-provided catalog connector parameters. Required parameter
        # values (e.g. a catalog server URL) must be provided by the user
        # during connector creation. Optional parameters (e.g. a filter condition)
        # can be provided by the user during connector creation.
        # Parameters are defined in the 'TODO-catalog.json' schema file.

        todo_required_parm = catalog_metadata['todo_required_parm']
        todo_optional_parm = catalog_metadata.get('todo_optional_parm')

        self.log.debug(f'Value of required parameter \'todo_required_parm\': {todo_required_parm}')
        self.log.debug(f'Value of optional parameter \'todo_optional_parm\': {todo_optional_parm}')

        try:
            # connect to catalog and retrieve component list
            self.log.debug('Retrieving component list from <TODO> catalog.')

            # Fetch components and add their keys to the component list.
            # Each 'todo_component_key_info' uniquely identifies a component in the catalog.
            # Method get_entry_data has access to todo_component_key_info via the
            # 'catalog_entry_data' parameter and uses it to retrieve the component from the catalog.
            todo_component_key_info = {
                'TODO-COMPONENT-KEY': 'dummy-component.yaml'
                # ... compound keys are okay!
            }
            component_list.append(todo_component_key_info)

        except Exception as ex:
            # error handling
            self.log.error(f'Error retrieving component list from <TODO> catalog: {ex}')

        return component_list

    def get_entry_data(self,
                       catalog_entry_data: Dict[str, Any],
                       catalog_metadata: Dict[str, Any]) -> Optional[EntryData]:
        """
        Fetch the definition that is identified by catalog_entry_data for the <TODO> catalog and
        create an EntryData object to represent it. If runtime-type-specific properties are required
        (e.g. `package_name` for certain Airflow operators), a runtime-type-specific EntryData
        object can be created, e.g. AirflowEntryData(definition=<...>, package_name=<...>)

        :param catalog_entry_data: a dictionary that contains the information needed to read the content
            of the component definition
        :param catalog_metadata: the metadata associated with the catalog in which this catalog entry is
            stored; in addition to catalog_entry_data, catalog_metadata may also be needed to read the
            component definition for certain types of catalogs

        :returns: the content of the given catalog entry's definition in string form
        """

        # Load user-provided catalog connector parameters.
        todo_required_parm = catalog_metadata['todo_required_parm']
        todo_optional_parm = catalog_metadata.get('todo_optional_parm')

        # Get catalog component key information from the catalog_entry_data
        # dictionary.
        todo_component_key = catalog_entry_data.get('TODO-COMPONENT-KEY')

        self.log.debug(f'Value of required parameter \'todo_required_parm\': {todo_required_parm}')
        self.log.debug(f'Value of optional parameter \'todo_optional_parm\': {todo_optional_parm}')

        # verify that a component key was provided
        if todo_component_key is None:
            # Log error and return None
            self.log.error('Cannot connect to <TODO> catalog: todo_component_key must be provided.')
            return None

        # load component from catalog using the provided key
        component_source = Path(__file__).parent / todo_component_key
        self.log.debug(f'Fetching component from {component_source}')
        with open(component_source, 'r') as dummy_component_fp:
            # read and return component
            return EntryData(definition=dummy_component_fp.read())

        return None

    @classmethod
    def get_hash_keys(cls) -> List[Any]:
        """
        Identifies the unique TODO catalog key that method get_entry_data
        can use to fetch a component from the catalog. Method get_catalog_entries
        retrieves the list of available key values from the catalog.

        :returns: a list of keys
      """
        return ['TODO-COMPONENT-KEY']
