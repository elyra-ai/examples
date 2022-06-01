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
import fnmatch
from http import HTTPStatus
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from urllib.parse import urlparse

import requests
from artifactory_catalog_connector import packaging_ports
from elyra.pipeline.catalog_connector import ComponentCatalogConnector, EntryData, KfpEntryData
from requests.auth import HTTPBasicAuth, AuthBase


class ArtifactoryApiKeyAuth(AuthBase):
    """
    A `requests.auth.AuthBase` implementation that sets the "X-JFrog-Art-Api" header.
    """

    def __init__(self, api_key):
        self.api_key = api_key

    def __call__(self, r):
        r.headers["X-JFrog-Art-Api"] = self.api_key
        return r


def get_folder_info(
    api_base_url: str,
    api_auth: Optional[AuthBase],
    repository_name: str,
    folder_path: str,
    file_filter: str,
) -> (List[str], List[str], bool):
    """
    Run a "folder info" query against an Artifactory repo to get lists of child files/folders.

    https://www.jfrog.com/confluence/display/JFROG/Artifactory+REST+API#ArtifactoryRESTAPI-FolderInfo

    :param api_base_url: the base url of the artifactory server
    :param api_auth: an instance of requests.auth.AuthBase
    :param repository_name: the name of the artifactory repository
    :param folder_path: the path of the folder which the query will be run against
    :param file_filter: an `fnmatch.fnmatch()` pattern to filter the returned child files
    :return: (child_folders, child_files, is_component_folder)
    """
    req_url = f"{api_base_url}/api/storage/{repository_name}/{folder_path.strip('/')}"
    resp = requests.get(req_url, auth=api_auth)

    if resp.status_code != HTTPStatus.OK:
        raise RuntimeError(
            f"Failed to get FolderInfo from '{req_url}'... "
            f"Got unhandled HTTP Status {resp.status_code}, expected 200... "
            f"{resp.text}"
        )
    expected_content_type = (
        "application/vnd.org.jfrog.artifactory.storage.FolderInfo+json"
    )
    if resp.headers["Content-Type"] != expected_content_type:
        raise RuntimeError(
            f"Failed to get FolderInfo from '{req_url}'... "
            f"Got unexpected Content-Type '{resp.headers['Content-Type']}', "
            f"expected '{expected_content_type}'"
        )

    child_folders = []
    child_files = []
    is_component_folder = False

    for child in resp.json().get("children", []):
        if child["folder"]:
            folder_path = child["uri"]
            child_folders.append(folder_path)
        else:
            file_path = child["uri"].lstrip("/")
            if file_path == "__COMPONENT__":
                is_component_folder = True
            elif fnmatch.fnmatch(file_path, file_filter):
                child_files.append(file_path)

    return child_folders, child_files, is_component_folder


def recursively_get_components(
    api_base_url: str,
    api_auth: Optional[AuthBase],
    repository_name: str,
    file_filter: str,
    file_ordering: str,
    max_recursion_depth: int,
    max_files_per_folder: int,
    current_folder_path: str,
    current_recursion_depth: int,
) -> List[Dict[str, Any]]:
    """
    A function which recursively traverses an Artifactory repo to return elyra `component_metadata` instances.

    NOTE: only returns `component_metadata` instances from folders which contain a "__COMPONENT__" marker file.

    :param api_base_url: the base url of the artifactory server
    :param api_auth: an instance of requests.auth.AuthBase
    :param repository_name: the name of the artifactory repository
    :param file_filter: an `fnmatch.fnmatch()` pattern to filter the returned files
    :param file_ordering: how the files in each folder are ordered (used in conjunction with `max_files_per_folder`)
    :param max_recursion_depth: max folder depth to recurse looking for "__COMPONENT__" files
    :param max_files_per_folder: max number of files returned from each folder (-1 is unlimited)
    :param current_folder_path: the path of the current folder that is being traversed
    :param current_recursion_depth: the current folder depth
    :return: a list of elyra `component_metadata` instances
    """
    component_list = []

    if current_recursion_depth > max_recursion_depth:
        return component_list

    child_folders, child_files, is_component_folder = get_folder_info(
        api_base_url=api_base_url,
        api_auth=api_auth,
        repository_name=repository_name,
        folder_path=current_folder_path,
        file_filter=file_filter,
    )

    if is_component_folder:
        if max_files_per_folder >= 0:
            if file_ordering == "NAME_ASCENDING":
                child_files.sort()
            elif file_ordering == "NAME_DESCENDING":
                child_files.sort(reverse=True)
            elif file_ordering == "VERSION_ASCENDING":
                child_files.sort(key=packaging_ports.legacy_version)
            elif file_ordering == "VERSION_DESCENDING":
                child_files.sort(key=packaging_ports.legacy_version, reverse=True)

            child_files = child_files[0:min(max_files_per_folder, len(child_files))]

        for relative_path in child_files:
            absolute_file_path = (
                f"{current_folder_path.strip('/')}/{relative_path.strip('/')}"
            )
            component_list.append(
                {"url": f"{api_base_url}/{repository_name}/{absolute_file_path}"}
            )
    else:
        for relative_path in child_folders:
            absolute_folder_path = (
                f"{current_folder_path.strip('/')}/{relative_path.strip('/')}"
            )
            component_list += recursively_get_components(
                api_base_url=api_base_url,
                api_auth=api_auth,
                repository_name=repository_name,
                file_filter=file_filter,
                file_ordering=file_ordering,
                max_recursion_depth=max_recursion_depth,
                max_files_per_folder=max_files_per_folder,
                current_folder_path=absolute_folder_path,
                current_recursion_depth=current_recursion_depth + 1,
            )

    return component_list


class ArtifactoryComponentCatalogConnector(ComponentCatalogConnector):
    """
    Read component definitions from an Artifactory catalog
    """

    def get_catalog_entries(
        self, catalog_metadata: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Returns a list of component_metadata instances, one per component found in the given registry.
        The form that component_metadata takes is determined by requirements of the reader class.

        :param catalog_metadata: the dictionary-form of the Metadata instance for a single registry
        """
        component_list = []

        artifactory_url = catalog_metadata["artifactory_url"]
        artifactory_username = catalog_metadata.get("artifactory_username")
        artifactory_password = catalog_metadata.get("artifactory_password")
        repository_name = catalog_metadata["repository_name"]
        repository_path = catalog_metadata["repository_path"]
        max_recursion_depth = int(catalog_metadata["max_recursion_depth"])
        max_files_per_folder = int(catalog_metadata["max_files_per_folder"])
        file_filter = catalog_metadata["file_filter"]
        file_ordering = catalog_metadata["file_ordering"]

        url_obj = urlparse(artifactory_url)
        api_base_url = f"{url_obj.scheme}://{url_obj.netloc}/{url_obj.path.strip('/')}"

        api_auth = None
        if artifactory_username and artifactory_password:
            api_auth = HTTPBasicAuth(
                username=artifactory_username, password=artifactory_password
            )
        elif artifactory_password:
            api_auth = ArtifactoryApiKeyAuth(api_key=artifactory_password)

        try:
            self.log.debug("Retrieving component list from Artifactory catalog.")

            component_list += recursively_get_components(
                api_base_url=api_base_url,
                api_auth=api_auth,
                repository_name=repository_name,
                file_filter=file_filter,
                file_ordering=file_ordering,
                max_recursion_depth=max_recursion_depth,
                max_files_per_folder=max_files_per_folder,
                current_folder_path=repository_path,
                current_recursion_depth=0,
            )

        except Exception as ex:
            self.log.error(
                f"Error retrieving component list from Artifactory catalog: {ex}"
            )

        return component_list

    def get_entry_data(
        self, catalog_entry_data: Dict[str, Any], catalog_metadata: Dict[str, Any]
    ) -> Optional[EntryData]:
        """
        Fetch the component that is identified by catalog_entry_data from the Artifactory catalog.

        :param catalog_entry_data: a dictionary that contains the information needed to read the content
                                   of the component definition
        :param catalog_metadata: the metadata associated with the catalog in which this catalog entry is
                                 stored; in addition to catalog_entry_data, catalog_metadata may also be
                                 needed to read the component definition for certain types of catalogs
        :returns: an EntryData object representing the definition (and other identifying info) for a single
                  catalog entry; if None is returned, this catalog entry is skipped and a warning message logged
        """
        artifactory_username = catalog_metadata.get("artifactory_username")
        artifactory_password = catalog_metadata.get("artifactory_password")

        url = catalog_entry_data.get("url")
        if url is None:
            self.log.error("Artifactory component source must contain `url`.")
            return None

        api_auth = None
        if artifactory_username and artifactory_password:
            api_auth = HTTPBasicAuth(
                username=artifactory_username, password=artifactory_password
            )
        elif artifactory_password:
            api_auth = ArtifactoryApiKeyAuth(api_key=artifactory_password)

        resp = requests.get(url, auth=api_auth)
        if resp.status_code != HTTPStatus.OK:
            self.log.error(
                f"Failed to read component from '{url}'... "
                f"Got unhandled HTTP Status {resp.status_code}, expected 200"
            )
            return None
        if resp.headers["Content-Type"] != "text/plain":
            self.log.error(
                f"Failed to read component from '{url}'... "
                f"Got unexpected Content-Type '{resp.headers['Content-Type']}', expected 'text/plain'"
            )
            return None

        return KfpEntryData(definition=resp.text)

    @classmethod
    def get_hash_keys(cls) -> List[Any]:
        """
        Identifies the unique Artifactory catalog key that get_entry_data
        can use to fetch a component from the catalog. Method get_catalog_entries
        retrieves the list of available key values from the catalog.

        :returns: a list of keys
        """
        return ["url"]
