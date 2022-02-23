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

import io
import json
from pathlib import Path
import tarfile
import yaml

from mlx_catalog_connector.mlx_component_catalog_connector import MLXComponentCatalogConnector 

KFP_SUPPORTED_FILE_TYPES = [".yaml"]

def test_invalid_get_catalog_entries(requests_mock):
    """
    Test invalid connectivity scenarios
    """
    mlxc = MLXComponentCatalogConnector(KFP_SUPPORTED_FILE_TYPES)

    # The specified host is invalid
    requests_mock.get('http://no.such.host:8080/apis/v1alpha1/components', real_http=True)
    ces = mlxc.get_catalog_entries({'mlx_api_url':'http://no.such.host:8080'})
    assert len(ces) == 0

    # The specified URL returns something unexpected (e.g. is not an MLX server):
    # wrong content type (not JSON)
    requests_mock.get('http://not-an-mlx-server:8080/apis/v1alpha1/components',
                      text='some random text')
    ces = mlxc.get_catalog_entries({'mlx_api_url':'http://not-an-mlx-server:8080'})
    assert len(ces) == 0

    # The specified URL returns something unexpected (e.g. is not an MLX server):
    # correct content type (not matching the expected schema)
    requests_mock.get('http://not-an-mlx-server:8080/apis/v1alpha1/components',
                      json={'somekey': 1})
    ces = mlxc.get_catalog_entries({'mlx_api_url':'http://not-an-mlx-server:8080'})
    assert len(ces) == 0

    # The specified URL returns something unexpected (e.g. is not an MLX server):
    # correct content type (not matching the expected schema)
    requests_mock.get('http://not-an-mlx-server:8080/apis/v1alpha1/components',
                      json={'components': 42})
    ces = mlxc.get_catalog_entries({'mlx_api_url':'http://not-an-mlx-server:8080'})
    assert len(ces) == 0


def test_get_catalog_entries(requests_mock):
    """
    Test various valid get_catalog_entries scenarios
    """
    mlxc = MLXComponentCatalogConnector(KFP_SUPPORTED_FILE_TYPES)

    dummy_json = {'components': [{'id': 'a-test-component-id'}]}
    requests_mock.get('http://mlx-server:8080/apis/v1alpha1/components',
                      text=json.dumps(dummy_json),
                      headers={'Content-Type': 'application/json'})
    ces = mlxc.get_catalog_entries({'mlx_api_url':'http://mlx-server:8080'})
    assert len(ces) == 1
    assert ces[0]['mlx_component_id'] == 'a-test-component-id'


def test_invalid_get_component_definition(requests_mock):
    """
    Test various invalid get_component_definition scenarios
    """
    mlxc = MLXComponentCatalogConnector(KFP_SUPPORTED_FILE_TYPES)

    # The specified host is invalid (no such host)
    mlx_component_id = 'a-bogus-component-id'
    requests_mock.get(f'http://no.such.host:8080/apis/v1alpha1/components/{mlx_component_id}/download', real_http=True)
    cd = mlxc.get_component_definition({'mlx_component_id': mlx_component_id},
                                       {'mlx_api_url':'http://no.such.host:8080'})
    assert cd is None

    # the specified server URL is invalid (not an MLX server)
    # the endpoint wasn't found
    mlx_component_id = 'a-bogus-component-id'
    requests_mock.get(f'http://not-an-mlx-server:8080/apis/v1alpha1/components/{mlx_component_id}/download',
                      text='There is no such endpoint',
                      status_code=404,
                      headers={'Content-Type': 'text/html'})
    cd = mlxc.get_component_definition({'mlx_component_id': mlx_component_id},
                                       {'mlx_api_url':'http://not-an-mlx-server:8080'})
    assert cd is None

    # the specified server URL is invalid (not an MLX server)
    # the endpoint returns something unexpected
    mlx_component_id = 'a-bogus-component-id'
    requests_mock.get(f'http://not-an-mlx-server:8080/apis/v1alpha1/components/{mlx_component_id}/download',
                      text='The endpoint returns something unexpected',
                      headers={'Content-Type': 'text/html'})
    cd = mlxc.get_component_definition({'mlx_component_id': mlx_component_id},
                                       {'mlx_api_url':'http://not-an-mlx-server:8080'})
    assert cd is None

    # the specified server URL is valid but the specified component id is unknown
    mlx_component_id = 'a-bogus-component-id'
    requests_mock.get(f'http://mlx-server:8080/apis/v1alpha1/components/{mlx_component_id}/download',
                      text='Could not find component with id a-bogus-component-id',
                      status_code=404,
                      headers={'Content-Type': 'application/gzip'})
    cd = mlxc.get_component_definition({'mlx_component_id': mlx_component_id},
                                       {'mlx_api_url':'http://mlx-server:8080'})
    assert cd is None    


def test_get_component_definition(requests_mock):
    """
    Test various valid get_component_definition scenarios
    """
    mlxc = MLXComponentCatalogConnector(KFP_SUPPORTED_FILE_TYPES)

    mlx_component_id = 'echo-sample'

    # mock MLX response: read valid definition
    with open(Path(__file__).parents[0] / 'resources' / f'{mlx_component_id}.yaml', 'rb') as f:
        content = f.read()
        component_source = io.BytesIO(initial_bytes=content)

    # mock MLX response: create compressed tar archive
    mocked_tarfile = io.BytesIO()
    with tarfile.open(fileobj=mocked_tarfile, mode='w:gz') as tar_file:
        info = tarfile.TarInfo(f'{mlx_component_id}.yaml')
        info.size = len(content)
        tar_file.addfile(info, component_source)

    requests_mock.get(f'http://mlx-server:8080/apis/v1alpha1/components/{mlx_component_id}/download',
                      status_code=200,
                      content=mocked_tarfile.getvalue(),
                      headers={'Content-Type': 'application/gzip'})
    cd = mlxc.get_component_definition({'mlx_component_id': mlx_component_id},
                                       {'mlx_api_url':'http://mlx-server:8080'})
    assert cd is not None
    assert cd.definition is not None
    assert yaml.safe_load(cd.definition)['name'] == 'Echo Sample' 
    assert json.dumps(cd.identifier) == json.dumps({'mlx_component_id': mlx_component_id})


def test_get_hash_keys():
    """
    Verify that `get_hash_keys` returns the expected hash keys
    """
    mlxc = MLXComponentCatalogConnector(KFP_SUPPORTED_FILE_TYPES)
    hc = mlxc.get_hash_keys()
    assert len(hc) == 1
    assert hc[0] == 'mlx_component_id'
