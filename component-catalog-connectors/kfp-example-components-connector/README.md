## Elyra pipeline component examples catalog

This catalog connector provides access to example pipeline components for Kubeflow Pipelines.

### Install the component examples

You can install the component examples from PyPI or source code. Note that a **rebuild of JupyterLab is not required**.

**Prerequisites**

- [Install Elyra](https://elyra.readthedocs.io/en/stable/getting_started/installation.html) (version 3.3 and above).

**Install from PyPI**

  ```
  $ pip install elyra-examples-kfp-catalog
  ```

**Install from source code**

   ```
   $ git clone https://github.com/elyra-ai/examples.git
   $ cd examples/component-catalog-connectors/kfp-example-components-connector/
   $ make clean source-install
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