## Elyra pipeline component examples catalog

This catalog connector provides access to example pipeline components for Apache Airflow.

### Install the component examples

You can install the component examples from PyPI or source code. Note that a **rebuild of JupyterLab is not required**.

**Prerequisites**

- [Install Elyra](https://elyra.readthedocs.io/en/stable/getting_started/installation.html) (version 3.3 and above).

**Install from PyPI**

  ```
  $ pip install elyra-examples-airflow-catalog
  ```

**Install from source code**

   ```
   $ git clone https://github.com/elyra-ai/examples.git
   $ cd examples/component-catalog-connectors/airflow-example-components-connector/
   $ make clean source-install
   ```

### Use the connector

1. Launch JupyterLab.
1. [Open the '`Manage Components`' panel](
https://elyra.readthedocs.io/en/stable/user_guide/pipeline-components.html#managing-custom-components-using-the-jupyterlab-ui).
1. Add a new component examples catalog ('`+`' > '`New Apache Airflow example components catalog`').
1. Specify a catalog name, e.g. '`Example components for Apache Airflow`'.
1. Save the catalog entry.
1. Open the Visual Pipeline Editor for Apache Airflow and expand the palette. The example components are displayed.

### Customize the catalog

This connector utilizes an embedded catalog as storage and is therefore a static catalog. To customize the catalog content according to your needs:

1. Clone or fork the `https://github.com/elyra-ai/examples` repository.
1. Navigate to the [`examples/component-catalog-connectors/airflow-example-components-connector/airflow_examples_connector/resources`](airflow_examples_connector/resources) directory. This directory contains the Apache Airflow operators that this connector makes available to Elyra. Note that the operator packages must be installed on the Apache Airflow cluster, or DAG execution will fail.
1. Change the content of this directory as desired.
1. Install the customized connector from source.

### Uninstall the connector

1. Remove all example catalog entries from the '`Manage Components`' panel.
1. Stop JupyterLab.
1. Uninstall the `elyra-examples-airflow-catalog` package.
   ```
   $ pip uninstall -y elyra-examples-airflow-catalog
   ```

### Troubleshooting

**Q: No example components are displayed in the Visual Pipeline Editor palette.**

A: Check the JupyterLab log file for error messages.