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
import os

from setuptools import find_packages, setup

long_desc = """
            Elyra component catalog for example Kubeflow Pipelines
            and Apache Airflow components.
            """

here = os.path.abspath(os.path.dirname(__file__))

version_ns = {}
with open(os.path.join(here, 'elyra_examples_connector', '_version.py')) as f:
    exec(f.read(), {}, version_ns)

setup_args = dict(
    name="elyra-example-components-catalog",
    version=version_ns['__version__'],
    url="https://github.com/elyra-ai/examples",
    description="Kubeflow Pipelines and Airflow example components for Elyra",
    long_description=long_desc,
    author="Elyra Maintainers",
    license="Apache License Version 2.0",
    packages=find_packages(),
    install_requires=[
        'elyra==3.3.0.dev0'
    ],
    setup_requires=['flake8'],
    include_package_data=True,
    entry_points={
        'metadata.schemas_providers': [
            'examples-catalog-schema = elyra_examples_connector.examples_schema_provider:ExamplesSchemasProvider'
        ],
        'elyra.component.catalog_types': [
            'examples-catalog = elyra_examples_connector.examples_connector:ExamplesCatalogConnector'
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