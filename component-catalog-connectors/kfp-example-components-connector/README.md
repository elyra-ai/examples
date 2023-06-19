<!--
{% comment %}
Copyright 2018-2023 Elyra Authors

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
{% endcomment %}
-->
[![PyPI version](https://badge.fury.io/py/elyra-examples-kfp-catalog.svg)](https://badge.fury.io/py/elyra-examples-kfp-catalog)

## Kubeflow Pipelines component examples catalog

This catalog connector provides access to example pipeline components for Kubeflow Pipelines.

### Install the component examples

You can install the component examples from PyPI or source code. Note that a **rebuild of JupyterLab is not required**.

**Prerequisites**

- [Install Elyra](https://elyra.readthedocs.io/en/stable/getting_started/installation.html) (version 3.7 and above). This connector version does not support Elyra versions below 3.7. 

**Install from PyPI**

To install the connector from PyPI:

  ```
  $ pip install elyra-examples-kfp-catalog
  ```

**Install from source code**

To install the connector from source:

   ```
   $ git clone https://github.com/elyra-ai/examples.git
   $ cd examples/component-catalog-connectors/kfp-example-components-connector/
   $ make clean source-install
   ```

**Run connector unit tests**

To run the unit tests:

   ```
   $ git clone https://github.com/elyra-ai/examples.git
   $ cd examples/component-catalog-connectors/kfp-example-components-connector/
   $ make test
   ```

### Use the connector

1. Launch JupyterLab.
1. [Open the '`Manage Components`' panel](
https://elyra.readthedocs.io/en/stable/user_guide/pipeline-components.html#managing-custom-components-using-the-jupyterlab-ui).
1. Add a new component examples catalog ('`+`' > '`New Kubeflow Pipelines example components catalog`').
1. Specify a catalog name, e.g. '`Example components for Kubeflow Pipelines`'.
1. Save the catalog entry.
1. Open the Visual Pipeline Editor for Kubeflow Pipelines and expand the palette. The example components are displayed.

### Customize the catalog

This connector utilizes an embedded catalog as storage and is therefore a static catalog. To customize the catalog content according to your needs:

1. Clone or fork the `https://github.com/elyra-ai/examples` repository.
1. Navigate to the [`examples/component-catalog-connectors/kfp-example-components-connector/kfp_examples_connector/resources`](kfp_examples_connector/resources) directory. This directory contains the Kubeflow Pipelines components that this connector makes available to Elyra.
1. Change the content of this directory as desired.
1. Install the connector from source.

### Uninstall the connector

1. Remove all example catalog entries from the '`Manage Components`' panel.
1. Stop JupyterLab.
1. Uninstall the `elyra-examples-kfp-catalog` package.
   ```
   $ pip uninstall -y elyra-examples-kfp-catalog
   ```

### Troubleshooting

**Q: No example components are displayed in the Visual Pipeline Editor palette.**

A: Check the JupyterLab log file for error messages.