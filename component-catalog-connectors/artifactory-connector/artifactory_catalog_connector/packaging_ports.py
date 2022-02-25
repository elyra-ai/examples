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
from typing import Iterator, Tuple, List

"""
Provides a port of `packaging.version.LegacyVersion()` which will be removed in a future `packaging` release.
Used in our implementation of "VERSION_ASCENDING" and "VERSION_DESCENDING" for `file_ordering`.
"""

# source: https://github.com/pypa/packaging/blob/21.3/packaging/version.py#L32
LegacyCmpKey = Tuple[int, Tuple[str, ...]]

# source: https://github.com/pypa/packaging/blob/21.3/packaging/version.py#L168
_legacy_version_component_re = re.compile(r"(\d+ | [a-z]+ | \.| -)", re.VERBOSE)

# source: https://github.com/pypa/packaging/blob/21.3/packaging/version.py#L170-L176
_legacy_version_replacement_map = {
    "pre": "c",
    "preview": "c",
    "-": "final-",
    "rc": "c",
    "dev": "@",
}


# source: https://github.com/pypa/packaging/blob/21.3/packaging/version.py#L179-L193
def _parse_version_parts(s: str) -> Iterator[str]:
    for part in _legacy_version_component_re.split(s):
        part = _legacy_version_replacement_map.get(part, part)

        if not part or part == ".":
            continue

        if part[:1] in "0123456789":
            # pad for numeric comparison
            yield part.zfill(8)
        else:
            yield "*" + part

    # ensure that alpha/beta/candidate are before final
    yield "*final"


# source: https://github.com/pypa/packaging/blob/21.3/packaging/version.py#L196-L220
def _legacy_cmpkey(version: str) -> LegacyCmpKey:
    # We hardcode an epoch of -1 here. A PEP 440 version can only have a epoch
    # greater than or equal to 0. This will effectively put the LegacyVersion,
    # which uses the defacto standard originally implemented by setuptools,
    # as before all PEP 440 versions.
    epoch = -1

    # This scheme is taken from pkg_resources.parse_version setuptools prior to
    # it's adoption of the packaging library.
    parts: List[str] = []
    for part in _parse_version_parts(version.lower()):
        if part.startswith("*"):
            # remove "-" before a prerelease tag
            if part < "*final":
                while parts and parts[-1] == "*final-":
                    parts.pop()

            # remove trailing zeros from each series of numeric parts
            while parts and parts[-1] == "00000000":
                parts.pop()

        parts.append(part)

    return epoch, tuple(parts)


def legacy_version(version: str) -> LegacyCmpKey:
    """
    Provides the same behaviour as `packaging.version.LegacyVersion()` when used as a sort-key function.

    :param version: the version string to extract a sort key from
    :return: a sort key
    """
    return _legacy_cmpkey(version)
