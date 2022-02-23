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


import re
import tarfile
from http import HTTPStatus
from io import BytesIO
from tempfile import TemporaryFile
from typing import Any
from typing import Dict
from typing import List
from urllib.parse import urlparse

from elyra.pipeline.catalog_connector import ComponentCatalogConnector
from elyra.pipeline.catalog_connector import ComponentDefinition

import requests


class MLXComponentCatalogConnector(ComponentCatalogConnector):
    """
    Read component definitions from a Machine Learning Exchange catalog
    https://github.com/machine-learning-exchange
    """

    def get_catalog_entries(self, catalog_metadata: Dict[str, Any]) -> List[Dict[str, Any]]:

        """
        Returns a list of component_metadata instances, one per component found in the given registry.
        The form that component_metadata takes is determined by requirements of the reader class.

        :param registry_metadata: the dictionary-form of the Metadata instance for a single registry
        """
        component_list = []

        # verify that the required inputs were provided
        mlx_api_url = catalog_metadata.get('mlx_api_url')

        if mlx_api_url is None:
            self.log.error('Cannot connect to MLX catalog: An API endpoint URL must be provided.')
            # return empty component list
            return component_list

        try:
            # invoke endpoint to retrieve component list from the catalog
            self.log.debug(f'Retrieving component list from MLX catalog \'{mlx_api_url}\'.')
            u = urlparse(mlx_api_url)
            # assemble MLX component list endpoint URL
            endpoint = u._replace(path='/apis/v1alpha1/components').geturl()

            # Query MLX catalog components endpoint
            res = requests.get(endpoint)
            if res.status_code != HTTPStatus.OK:
                self.log.warning(f'Error fetching component list from MLX catalog \'{mlx_api_url}\': '
                                 f'Request: {endpoint} HTTP code: {res.status_code}.')
                return component_list

            if res.headers.get('Content-Type') != 'application/json':
                self.log.warning(f'Error fetching component list from MLX catalog \'{mlx_api_url}\': '
                                 f'Unexpected response content type: {res.headers.get("Content-Type")}. '
                                 f'Content: {res.content}')
                return component_list

            # the response is JSON formatted:
            # "components": [
            #    {
            #      "id": "component-id-used-for-retrieval",
            #      "name": "user friendly component name"
            #      ...
            #    }
            # ]

            json_response = res.json()
            if json_response.get('components') is None or \
               not isinstance(json_response['components'], list):
                self.log.warning(f'Error fetching component list from MLX catalog \'{mlx_api_url}\': '
                                 f'Unexpected JSON response: '
                                 f'Content: {res.content}')
                return component_list

            # create component filter regex if a filter condition was
            # specified by the user
            filter_expression = catalog_metadata.get('filter', '').strip()
            regex = None
            if len(filter_expression) > 0:
                regex = filter_expression.replace('*', '.*').replace('?', '.?')

            # post-process the component list by applying the filter regex, if
            # one was specified
            for component in json_response.get('components', []):
                if regex:
                    if re.fullmatch(regex, component.get('name', ''), flags=re.IGNORECASE):
                        component_list.append({'mlx_component_id': component.get('id')})
                else:
                    component_list.append({'mlx_component_id': component.get('id')})

        except Exception as ex:
            self.log.warning(f'Error fetching component list from MLX catalog \'{mlx_api_url}\': {ex}')

        return component_list

    def get_component_definition(self,
                                 catalog_entry_data: Dict[str, Any],
                                 catalog_metadata: Dict[str, Any]) -> ComponentDefinition:
        """
        Fetch the component that is identified by catalog_entry_data from
        the MLX catalog.

        :param catalog_entry_data: a dictionary that contains the information needed to read the content
                                   of the component definition
        :param catalog_metadata: the metadata associated with the catalog in which this catalog entry is
                                 stored; in addition to catalog_entry_data, catalog_metadata may also be
                                 needed to read the component definition for certain types of catalogs

        :returns: A ComponentDefinition containing the definition, if found
        """

        # verify that the required inputs were provided
        mlx_api_url = catalog_metadata.get('mlx_api_url')
        if mlx_api_url is None:
            self.log.error('Cannot connect to MLX catalog: An API endpoint URL must be provided.')
            return None

        mlx_component_id = catalog_entry_data['mlx_component_id']
        if mlx_component_id is None:
            self.log.error(f'Cannot retrieve component specification from MLX catalog \'{mlx_api_url}\': '
                           'A component id must be provided.')
            return None

        try:
            u = urlparse(mlx_api_url)
            # assemble MLX component list endpoint URL
            endpoint = u._replace(path=f'apis/v1alpha1/components/{mlx_component_id}/download').geturl()
            res = requests.get(endpoint)
        except Exception as e:
            self.log.error(f'Failed to download component specification {mlx_component_id} '
                           f'from \'{mlx_api_url}\': {str(e)}')
            return None

        if res.status_code != HTTPStatus.OK:
            self.log.error(f'Error fetching component specification \'{mlx_component_id}\' '
                           f'from MLX catalog \'{mlx_api_url}\': '
                           f'Request: {endpoint} HTTP code: {res.status_code}.')
            return None

        if res.headers.get('Content-Type') != 'application/gzip':
            self.log.error(f'Error fetching component specification \'{mlx_component_id}\' '
                           f'from MLX catalog \'{mlx_api_url}\': '
                           f'Unexpected response content type: {res.headers.get("Content-Type")}.')
            return None

        # response type should be 'application/gzip'
        # Content-Disposition: attachment; filename=model-fairness-check.tgz
        with TemporaryFile() as fp:
            fp.write(res.content)
            fp.seek(0)
            try:
                tar = tarfile.open(fileobj=BytesIO(fp.read()),
                                   mode='r:gz')
                if len(tar.getnames()) > 1:
                    self.log.error(f'The response archive contains more than one member: {tar.getnames()}')

                return ComponentDefinition(definition=tar.extractfile(tar.getnames()[0]).read(),
                                           identifier=catalog_entry_data)
            except Exception as ex:
                # the response is not a tgz file
                self.log.error(f'The MLX catalog response could not be processed: {ex}')
                return None

    def get_hash_keys(self) -> List[Any]:
        """
        Identifies the unique MLX catalog key that read_catalog_entry can use
        to fetch an entry from the catalog. Method get_catalog_entries retrieves
        the list of available key values.

        :returns: a list of keys, which is for MLX the component id
      """
        return ['mlx_component_id']
