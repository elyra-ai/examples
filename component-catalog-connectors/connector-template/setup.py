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
import os

from setuptools import find_packages, setup

long_desc = """
            Elyra component catalog connector for <TODO>
            """

here = os.path.abspath(os.path.dirname(__file__))

version_ns = {}
with open(os.path.join(here, 'todo_catalog_connector', '_version.py')) as f:
    exec(f.read(), {}, version_ns)

setup_args = dict(
    name="todo-component-catalog-connector",
    version=version_ns['__version__'],
    url="TODO-CATALOG-CONNECTOR-REPOSITORY-URL",
    description="TODO-CATALOG-CONNECTOR-DESCRIPTION",
    long_description=long_desc,
    author="TODO-AUTHOR-INFO",
    author_email="TODO-AUTHOR-EMAIL",
    license="Apache License Version 2.0",
    packages=find_packages(),
    install_requires=[
    ],
    setup_requires=['flake8'],
    include_package_data=True,
    entry_points={
        'metadata.schemas_providers': [
            'todo-catalog-schema = todo_catalog_connector.todo_schema_provider:TODOSchemasProvider'
        ],
        'elyra.component.catalog_types': [
            'todo-catalog = todo_catalog_connector.todo_catalog_connector:TODOComponentCatalogConnector'
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ]
)


if __name__ == '__main__':
    setup(**setup_args)
