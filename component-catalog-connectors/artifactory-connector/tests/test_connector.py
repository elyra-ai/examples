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

import logging
from typing import Dict, Union

import pytest
from artifactory_catalog_connector.artifactory_catalog_connector import (
    ArtifactoryComponentCatalogConnector,
)
from elyra.pipeline.catalog_connector import KfpEntryData
from requests.exceptions import ConnectTimeout
from requests_mock import Mocker


################################
# TEST HELPERS
################################
def _component_yaml(component_name: str, component_version: str) -> str:
    with open("tests/resources/component-template.yaml", "r") as f:
        return (
            f.read()
            .replace("{{COMPONENT_NAME}}", component_name)
            .replace("{{COMPONENT_VERSION}}", component_version)
        )


def _register_artifactory_mocks(
    requests_mock: Mocker,
    api_base_url: str,
    repository_name: str,
    folder_path: str,
    folder_content: Dict[str, Union[Dict, str]],
):
    for name, content in folder_content.items():
        # CASE: content represents a file
        if isinstance(content, str):
            file_path = f"{folder_path}/{name}"

            # register a mock that returns the file content
            url = f"{api_base_url.rstrip('/')}/{repository_name}/{file_path.strip('/')}"
            requests_mock.get(
                url=url,
                headers={"Content-Type": "text/plain"},
                text=content,
            )
            logging.getLogger().warning(f"Registered Mock URL - {url}")

        # CASE: content represents a folder
        elif isinstance(content, dict):
            subfolder_path = f"{folder_path}/{name}"

            # register a mock that returns the FolderInfo
            # https://www.jfrog.com/confluence/display/JFROG/Artifactory+REST+API#ArtifactoryRESTAPI-FolderInfo
            url = f"{api_base_url.rstrip('/')}/api/storage/{repository_name}/{subfolder_path.strip('/')}"
            requests_mock.get(
                url=url,
                headers={
                    "Content-Type": "application/vnd.org.jfrog.artifactory.storage.FolderInfo+json"
                },
                json={
                    "uri": url,
                    "repo": repository_name,
                    "path": f"/{subfolder_path.strip('/')}",
                    "created": "2000-01-01T00:00:00.000Z",
                    "createdBy": "userY",
                    "lastModified": "2000-01-01T00:00:00.000Z",
                    "modifiedBy": "userY",
                    "lastUpdated": "2000-01-01T00:00:00.000Z",
                    "children": [
                        {
                            "uri": f"/{child_name}",
                            "folder": isinstance(child_content, dict),
                        }
                        for child_name, child_content in content.items()
                    ],
                },
            )
            logging.getLogger().warning(f"Registered Mock URL - {url}")

            # recursively call this function to populate subdirectories
            _register_artifactory_mocks(
                requests_mock=requests_mock,
                api_base_url=api_base_url,
                repository_name=repository_name,
                folder_path=f"{folder_path}/{name}",
                folder_content=content,
            )


################################
# TESTS
################################
class TestArtifactoryComponentCatalogConnector:

    log = logging.getLogger(__name__)

    @pytest.fixture(scope="function")
    def connector(self):
        _kfp_supported_file_types = [".yaml"]
        yield ArtifactoryComponentCatalogConnector(_kfp_supported_file_types)

    @pytest.fixture(scope="function")
    def mock_artifactory(self, requests_mock):
        _artifactory_url = "https://artifactory.example.com/"
        _repository_name = "my-repository"
        _repo_content = {
            "components": {
                "component_1": {
                    "__COMPONENT__": "",
                    "component-1.0.9.yaml": _component_yaml("component_1", "1.0.9"),
                    "component-1.0.10.yaml": _component_yaml("component_1", "1.0.10"),
                },
                "component_2": {
                    "__COMPONENT__": "",
                    "component-1.0.0.yaml": _component_yaml("component_2", "1.0.0"),
                    "component-1.1.0.yaml": _component_yaml("component_2", "1.1.0"),
                },
                "component_3": {
                    "__COMPONENT__": "",
                    "component-1.0.0.yaml": _component_yaml("component_3", "1.0.0"),
                    "component-1.1.0.yaml": _component_yaml("component_3", "1.1.0"),
                    "hidden_component": {
                        "__COMPONENT__": "",
                        "component-1.0.0.yaml": _component_yaml(
                            "hidden_component", "1.0.0"
                        ),
                        "component-1.1.0.yaml": _component_yaml(
                            "hidden_component", "1.1.0"
                        ),
                    },
                },
            }
        }
        _register_artifactory_mocks(
            requests_mock=requests_mock,
            api_base_url=_artifactory_url,
            repository_name=_repository_name,
            folder_path="",
            folder_content=_repo_content,
        )
        yield _artifactory_url, _repository_name

    def test__get_hash_keys(self, connector):
        """
        Verify that `get_hash_keys()` returns the expected hash keys
        """
        hash_keys = connector.get_hash_keys()
        assert len(hash_keys) == 1
        assert hash_keys[0] == "url"

    def test__get_catalog_entries__invalid(self, connector, requests_mock):
        """
        Test various invalid `get_catalog_entries()` scenarios
        """
        _artifactory_url = "https://invalid.example.com/"
        _repository_name = "my-repository"
        _repository_path = "/components"
        _catalog_metadata = {
            "artifactory_url": _artifactory_url,
            "repository_name": _repository_name,
            "repository_path": _repository_path,
            "max_recursion_depth": "3",
            "max_files_per_folder": "-1",
            "file_filter": "*.yaml",
            "file_ordering": "VERSION_ASCENDING",
        }

        # the URL of the expected first API call given the above parameters
        _storage_api_url = (
            f"{_artifactory_url.rstrip('/')}"
            "/api/storage"
            f"/{_repository_name}"
            f"/{_repository_path.strip('/')}"
        )

        # TEST - the specified URL times out
        mock = requests_mock.get(url=_storage_api_url, exc=ConnectTimeout)
        catalog_entries = connector.get_catalog_entries(_catalog_metadata)
        assert mock.called
        assert len(catalog_entries) == 0

        # TEST - the specified URL returns non-200 status code
        mock = requests_mock.get(url=_storage_api_url, status_code=400)
        catalog_entries = connector.get_catalog_entries(_catalog_metadata)
        assert mock.called
        assert len(catalog_entries) == 0

        # TEST - the specified URL returns wrong content type 'plain/text'
        mock = requests_mock.get(
            url=_storage_api_url,
            text="some random text",
            headers={"Content-Type": "plain/text"},
        )
        catalog_entries = connector.get_catalog_entries(_catalog_metadata)
        assert mock.called
        assert len(catalog_entries) == 0

        # TEST - the specified URL returns correct content type, but malformed
        mock = requests_mock.get(
            url=_storage_api_url,
            json={"children": [{"invalid_key": "some value"}]},
            headers={
                "Content-Type": "application/vnd.org.jfrog.artifactory.storage.FolderInfo+json"
            },
        )
        catalog_entries = connector.get_catalog_entries(_catalog_metadata)
        assert mock.called
        assert len(catalog_entries) == 0

    def test__get_catalog_entries__valid(self, connector, mock_artifactory):
        """
        Test various valid `get_catalog_entries()` scenarios
        """
        _artifactory_url, _repository_name = mock_artifactory

        # TEST - single component folder
        catalog_entries = connector.get_catalog_entries(
            {
                "artifactory_url": _artifactory_url,
                "repository_name": _repository_name,
                "repository_path": "/components/component_1",
                "max_recursion_depth": "3",
                "max_files_per_folder": "-1",
                "file_filter": "*.yaml",
                "file_ordering": "VERSION_ASCENDING",
            }
        )
        expected_catalog_entries = [
            {"url": f"{_artifactory_url.rstrip('/')}/{_repository_name}/{path}"}
            for path in [
                "components/component_1/component-1.0.9.yaml",
                "components/component_1/component-1.0.10.yaml",
            ]
        ]
        assert catalog_entries == expected_catalog_entries

        # TEST - multiple component folders
        catalog_entries = connector.get_catalog_entries(
            {
                "artifactory_url": _artifactory_url,
                "repository_name": _repository_name,
                "repository_path": "/components",
                "max_recursion_depth": "3",
                "max_files_per_folder": "-1",
                "file_filter": "*.yaml",
                "file_ordering": "VERSION_ASCENDING",
            }
        )
        expected_catalog_entries = [
            {"url": f"{_artifactory_url.rstrip('/')}/{_repository_name}/{path}"}
            for path in [
                "components/component_1/component-1.0.9.yaml",
                "components/component_1/component-1.0.10.yaml",
                "components/component_2/component-1.0.0.yaml",
                "components/component_2/component-1.1.0.yaml",
                "components/component_3/component-1.0.0.yaml",
                "components/component_3/component-1.1.0.yaml",
            ]
        ]
        assert catalog_entries == expected_catalog_entries

    def test__get_entry_data__invalid(self, connector, requests_mock):
        """
        Test various invalid `get_entry_data()` scenarios
        """
        _entry_url = "https://invalid.example.com/my-repository/component.yaml"
        _catalog_entry_data = {"url": _entry_url}
        _catalog_metadata = {}

        # TEST - the specified URL times out
        mock = requests_mock.get(url=_entry_url, exc=ConnectTimeout)
        entry_data = connector.get_entry_data(_catalog_entry_data, _catalog_metadata)
        assert mock.called
        assert entry_data is None

        # TEST - the specified URL returns non-200 status code
        mock = requests_mock.get(url=_entry_url, status_code=400)
        entry_data = connector.get_entry_data(_catalog_entry_data, _catalog_metadata)
        assert mock.called
        assert entry_data is None

        # TEST - the specified URL returns wrong content type (not 'plain/text')
        mock = requests_mock.get(
            url=_entry_url,
            json={"some key": "some value"},
            headers={"Content-Type": "application/json"},
        )
        entry_data = connector.get_entry_data(_catalog_entry_data, _catalog_metadata)
        assert mock.called
        assert entry_data is None

    def test__get_entry_data__valid(self, connector, mock_artifactory):
        """
        Test various valid `get_entry_data()` scenarios
        """
        _artifactory_url, _repository_name = mock_artifactory

        # TEST - single component definition
        entry_data = connector.get_entry_data(
            catalog_entry_data={
                "url": (
                    f"{_artifactory_url.rstrip('/')}"
                    f"/{_repository_name}"
                    "/components/component_1/component-1.0.10.yaml"
                )
            },
            # we don't use catalog_metadata when retrieving entries, so can be blank
            catalog_metadata={},
        )
        assert isinstance(entry_data, KfpEntryData)
        assert entry_data.definition == _component_yaml("component_1", "1.0.10")
