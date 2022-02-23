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

from kfp_examples_connector.examples_connector import ExamplesCatalogConnector

KFP_SUPPORTED_FILE_TYPES = [".yaml"]


def test_get_catalog_entries():
    """
    Test valid get_catalog_entries scenarios
    """
    xc = ExamplesCatalogConnector(KFP_SUPPORTED_FILE_TYPES)
    ces = xc.get_catalog_entries({'runtime_type': 'KUBEFLOW_PIPELINES'})

    # Verify that the expected example components are returned
    examples_resources_dir = Path(__file__).parent / '..' / 'kfp_examples_connector' / 'resources'
    examples = [f.name for f in examples_resources_dir.glob('**/*.yaml')]
    assert len(ces) == len(examples)
    for example in ces:
        assert example['component-id'] in examples


def test_get_hash_keys():
    """
    Verify that `get_hash_keys` returns the expected hash keys
    """
    xc = ExamplesCatalogConnector(KFP_SUPPORTED_FILE_TYPES)
    hc = xc.get_hash_keys()
    assert len(hc) == 1
    assert hc[0] == 'component-id'


def test_get_component_definition():
    """
    Test various valid get_component_definition scenarios
    """
    xc = ExamplesCatalogConnector(KFP_SUPPORTED_FILE_TYPES)

    examples_resources_dir = Path(__file__).parent / '..' / 'kfp_examples_connector' / 'resources'
    example_files = [f for f in examples_resources_dir.glob('**/*.yaml')]
    # validate every definition
    for example in example_files:
        cd = xc.get_component_definition({'component-id': example.name},
                                         {'runtime_type': 'KUBEFLOW_PIPELINES'})
        assert cd is not None
        assert cd.identifier['component-id'] == example.name
        with open(example, 'r') as component_source:
            assert component_source.read() == cd.definition


def test_invalid_get_component_definition():
    """
    Test various invalid get_component_definition scenarios
    """
    xc = ExamplesCatalogConnector(KFP_SUPPORTED_FILE_TYPES)

    # no component id specified
    cd = xc.get_component_definition({},
                                     {'runtime_type': 'KUBEFLOW_PIPELINES'})
    assert cd is None

    # invalid component id specified and no runtime name
    cd = xc.get_component_definition({'component-id': 'no-such-component.py'},
                                     {})
    assert cd is None

    # invalid component id specified and invalid runtime name
    cd = xc.get_component_definition({'component-id': 'no-such-component.py'},
                                     {'runtime_type': 'NO-SUCH-RUNTIME'})
    assert cd is None

    # component does not exist
    cd = xc.get_component_definition({'component-id': 'no-such-component.py'},
                                     {'runtime_type': 'KUBEFLOW_PIPELINES'})
    assert cd is None
