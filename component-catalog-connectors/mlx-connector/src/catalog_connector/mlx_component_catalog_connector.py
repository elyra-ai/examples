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

import re
import tarfile
from http import HTTPStatus
from io import BytesIO
from tempfile import TemporaryFile
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from urllib.parse import urlparse

from elyra.pipeline.catalog_connector import ComponentCatalogConnector

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
            # return empty component specification list
            return component_list

        if catalog_metadata.get('runtime') != 'kfp':
            self.log.error(f'MLX catalog {mlx_api_url} only supports Kubeflow Pipelines.')
            # return empty component specification list
            return component_list

        try:
            # invoke endpoint to retrieve list of component specifications from
            # the catalog
            self.log.debug(f'Retrieving component list from MLX catalog \'{mlx_api_url}\'.')
            u = urlparse(mlx_api_url)
            # assemble MLX component list endpoint URL
            endpoint = u._replace(path='/apis/v1alpha1/components').geturl()

            # Query MLX catalog components endpoint
            res = requests.get(endpoint)
            if res.status_code != HTTPStatus.OK:
                self.log.warning(f'Error fetching component list from MLX catalog {mlx_api_url}: '
                                 f'Request: {endpoint} HTTP code: {res.status_code}.')
                return component_list

            if res.headers['Content-Type'] != 'application/json':
                self.log.warning(f'Error fetching component list from MLX catalog {mlx_api_url}: '
                                 f'Unexpected content type: {res.headers["Content-Type"]}.'
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

            # create component filter regex if a filter condition was
            # specified by the user
            filter_expression = catalog_metadata.get('filter', '').strip()
            regex = None
            if len(filter_expression) > 0:
                regex = filter_expression.replace('*', '.*').replace('?', '.?')

            # post-process the component list by applying the filter regex, if
            # one was specified
            for component in res.json().get('components', []):
                if regex:
                    if re.fullmatch(regex, component.get('name', ''), flags=re.IGNORECASE):
                        component_list.append({'mlx_component_id': component.get('id')})
                else:
                    component_list.append({'mlx_component_id': component.get('id')})

        except Exception as ex:
            self.log.warning(f'Error fetching component list from MLX catalog {mlx_api_url}: {ex}')

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

        :returns: the content of the given catalog entry's definition in string form
        """

        # verify that the required inputs were provided
        mlx_api_url = catalog_metadata.get('mlx_api_url')
        if mlx_api_url is None:
            self.log.error('Cannot connect to MLX catalog: An API endpoint URL must be provided.')
            return None

        mlx_component_id = catalog_entry_data['mlx_component_id']
        if mlx_component_id is None:
            self.log.error(f'Cannot retrieve component specification from MLX catalog {mlx_api_url}: '
                           'A component id must be provided.')
            return None

        try:
            u = urlparse(mlx_api_url)
            # assemble MLX component list endpoint URL
            endpoint = u._replace(path=f'apis/v1alpha1/components/{mlx_component_id}/download').geturl()
            res = requests.get(endpoint)
        except Exception as e:
            self.log.error(f'Failed to download component specification {mlx_component_id} '
                           f'from {mlx_api_url}: {str(e)}')
            return None

        if res.status_code != HTTPStatus.OK:
            self.log.error(f'Error fetching component specification {mlx_component_id} '
                           f'from MLX catalog {mlx_api_url}: '
                           f'Request: {endpoint} HTTP code: {res.status_code}.')
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

                return tar.extractfile(tar.getnames()[0]).read()
            except Exception as ex:
                # the response is not a tgz file
                self.log.error(f'The MLX catalog response could not be processed: {ex}')

        return None

    def get_hash_keys(self) -> List[Any]:
        """
        Provides a list of keys available in the 'catalog_entry_data' dictionary whose values
        will be used to construct a unique hash id for each entry with the given catalog type

        :returns: a list of keys
      """
        return ['mlx_component_id']
