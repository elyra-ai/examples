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

import ast
from os.path import sep
from pathlib import Path
import re
import shutil
from tempfile import mkdtemp
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from urllib.parse import urlparse
import zipfile

from elyra.pipeline.catalog_connector import ComponentCatalogConnector
import requests


class AirflowProviderPackageCatalogConnector(ComponentCatalogConnector):
    """
    Read component definitions from an Apache Airflow provider package archive
    """

    def get_catalog_entries(self, catalog_metadata: Dict[str, Any]) -> List[Dict[str, Any]]:

        """
        Returns a list of component_metadata instances, one per component found in the given registry.
        The form that component_metadata takes is determined by requirements of the reader class.

        :param registry_metadata: the dictionary-form of the Metadata instance for a single registry
        """

        # Return data structure: each list entry contains a 'file' and a 'class' key
        # entry, as defined in the 'get_hash_keys' method
        operator_key_list = []

        # Load user-provided catalog connector parameters. Required parameter
        # values (e.g. a catalog server URL) must be provided by the user
        # during connector creation. Optional parameters (e.g. a filter condition)
        # can be provided by the user during connector creation.
        # Parameters are defined in the 'airflow-provider-package-catalog-catalog.json' schema file.

        provider_package_download_url = catalog_metadata['provider_package_download_url']
        provider_package_name = Path(urlparse(provider_package_download_url).path).name

        # tmp_archive_dir is used to store the downloaded provider package archive
        # and the extracted archive
        if hasattr(self, 'tmp_archive_dir'):
            shutil.rmtree(self.tmp_archive_dir.name, ignore_errors=True)
        self.tmp_archive_dir = Path(mkdtemp())

        try:
            self.log.warning(f'Downloading provider package from \'{provider_package_download_url}\' ...')

            # download archive
            response = requests.get(provider_package_download_url,
                                    allow_redirects=True)
            if response.status_code == 200:
                # save archive
                archive = str(self.tmp_archive_dir / Path(urlparse(provider_package_download_url).path).name)
                self.log.warning(f'Saving provider package in \'{archive}\' ...')
                with open(archive, 'wb') as archive_fh:
                    archive_fh.write(response.content)

                # extract archive
                self.log.warning(f'Extracting provider archive \'{archive}\' ...')
                with zipfile.ZipFile(archive, 'r') as zip_ref:
                    zip_ref.extractall(self.tmp_archive_dir)

                # Locate 'get_provider_info.py' in the extracted archive.
                # It identifies Python modules that contain operator class definitions.
                pl = list(self.tmp_archive_dir.glob('**/get_provider_info.py'))
                if len(pl) != 1:
                    # No such file or more than one file was found. Cannot proceed.
                    self.log.error(f'Error. Provider archive \'{archive}\' '
                                   'contains {len(pl)} '
                                   'file(s) named get_provider_info.py.')
                    # return empty list
                    return operator_key_list
                get_provider_info_file_location = pl[0]

                # extract module names from get_provider_info.py
                with open(get_provider_info_file_location, 'r') as gpi_file:
                    f = gpi_file.read()
                namespace = {}
                exec(f, namespace)
                try:
                    # try to run the 'get_provider_info' method
                    return_dict = namespace['get_provider_info']()
                except KeyError:
                    # no method with this name is defined in get_provider_info.py
                    self.log.error('Error. Cannot invoke get_provider_info method '
                                   f'in \'{get_provider_info_file_location}\'.')
                    return operator_key_list

                module_list = []
                for operator_entry in return_dict.get('operators', []):
                    for m in operator_entry['python-modules']:
                        module_list.append(f'{m.replace(".", sep)}.py')
                if len(module_list) == 0:
                    self.log.info(f'Provider package \'{provider_package_name}\' '
                                  'does not include any operator definitions.')
                    return operator_key_list

                # Locate Python files in module_list that extend the
                # Airflow BaseOperator class
                extends_baseoperator = []  # list of str, containing classes that extend BaseOperator
                classes_to_analyze = {}
                imported_operator_classes = []  # list of str, identifying imported operator classes
                for module in module_list:
                    with open(self.tmp_archive_dir / module, 'r') as mf:
                        # parse module
                        tree = ast.parse(mf.read())
                        for node in ast.walk(tree):
                            # analyze imports
                            if isinstance(node, ast.Import):
                                for name in node.names:
                                    self.log.warning(f'Detected an IMPORT: {name.name}')
                            elif isinstance(node, ast.ImportFrom):
                                node_module = node.module
                                for name in node.names:
                                    self.log.warning(f'Detected an IMPORT FROM: {node_module} -> {name.name}')
                                    if 'airflow.models' == node_module and name.name == 'BaseOperator':
                                        imported_operator_classes.append(name.name)
                                    else:
                                        # Look for package imports that match one of the following patters:
                                        # airflow.providers.*.operators.
                                        # airflow.operators.*
                                        patterns = [r'airflow\.providers\.[a-z_]+\.operators',
                                                    r'airflow\.operators\.']
                                        for pattern in patterns:
                                            match = re.match(pattern, node_module)
                                            if match:
                                                imported_operator_classes.append(name.name)
                                                break

                            # analyze classes
                            elif isinstance(node, ast.ClassDef):
                                # self.log.warning(f'{module} {node.name}')
                                # determine whether class extends one of the imported operator classes
                                if len(node.bases) == 0:
                                    # class does not extend other classes; nothing to do
                                    continue
                                for base in node.bases:
                                    extends = False
                                    if base.id in imported_operator_classes:
                                        extends = True
                                        extends_baseoperator.append(node.name)
                                        operator_key_list.append(
                                            {'provider_package': provider_package_name,
                                             'file': module,
                                             'class': node.name})
                                        continue
                                if extends is False:
                                    classes_to_analyze[node.name] = {
                                        'node': node,
                                        'file': module
                                    }

                # identify classes that indirectly extend BaseOperator
                analysis_complete = len(classes_to_analyze.keys()) == 0
                while analysis_complete is False:
                    analysis_complete = True
                    for class_name in list(classes_to_analyze.keys()):
                        self.log.warning(f'Analyzing {class_name} from '
                                         f"'{classes_to_analyze[class_name]['file']}\'... ")
                        for base in classes_to_analyze[class_name]['node'].bases:
                            if base.id in extends_baseoperator:
                                extends_baseoperator.append(class_name)
                                operator_key_list.append({
                                    'provider_package': provider_package_name,
                                    'file': classes_to_analyze[class_name]['file'],
                                    'class': class_name})
                                del classes_to_analyze[class_name]
                                analysis_complete = False
                                continue
        except Exception as ex:
            self.log.error('Error retrieving operator list from provider package '
                           f'{provider_package_download_url}: {ex}')

        self.log.info(f'Identified {len(operator_key_list)} operators in '
                      f'provider package \'{provider_package_download_url}\'.')
        self.log.warning(f'Operator key list: {operator_key_list}')
        return operator_key_list

    def read_catalog_entry(self,
                           catalog_entry_data: Dict[str, Any],
                           catalog_metadata: Dict[str, Any]) -> Optional[str]:
        """
        Fetch the component that is identified by catalog_entry_data from
        the <TODO> catalog.

        :param catalog_entry_data: a dictionary that contains the information needed to read the content
                                   of the component definition
        :param catalog_metadata: the metadata associated with the catalog in which this catalog entry is
                                 stored; in addition to catalog_entry_data, catalog_metadata may also be
                                 needed to read the component definition for certain types of catalogs

        :returns: the content of the given catalog entry's definition in string form
        """

        self.log.warning(f'catalog_entry_data: {catalog_entry_data}')

        # Get operator key information from the catalog_entry_data dictionary.
        # provider_package_name = catalog_entry_data.get('provider_package')
        operator_file_name = catalog_entry_data.get('file')
        # operator_class_name = catalog_entry_data.get('class')

        if hasattr(self, 'tmp_archive_dir') is False:
            # Log error and return None
            self.log.error('Error. Cannot fetch operator definition. The '
                           ' downloaded provider package archive was not found.')
            return None

        # load component source using the provided key
        component_source = self.tmp_archive_dir / operator_file_name
        self.log.warning(f'Reading component source {component_source} ...')
        with open(component_source, 'r') as source:
            return source.read()

        return None

    def get_hash_keys(self) -> List[Any]:
        """
        Identifies the unique keys that method read_catalog_entry
        can use to fetch a component from the Airflow provider package.
        Method get_catalog_entries retrieves the list of available key
        values from the package.

        :returns: a list of keys
      """
        return ['provider_package', 'file', 'class']
