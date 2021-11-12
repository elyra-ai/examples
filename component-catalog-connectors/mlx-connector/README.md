[![PyPI version](https://badge.fury.io/py/mlx-component-catalog-connector.svg)](https://badge.fury.io/py/mlx-component-catalog-connector)

## Machine Learning Exchange catalog connector

This catalog connector enables Elyra to load Kubeflow Pipelines components from [Machine Learning Exchange](https://github.com/machine-learning-exchange) (MLX) deployments.

### Install the connector

You can install the MLX catalog connector from PyPI or source code. Note that a **rebuild of JupyterLab is not required**.

**Prerequisites**

- [Install Elyra](https://elyra.readthedocs.io/en/stable/getting_started/installation.html) (version 3.3 and above).
- [Machine Learning Exchange deployment](https://github.com/machine-learning-exchange/mlx) ([quickstart guide](https://github.com/machine-learning-exchange/mlx/tree/main/quickstart))

**Install from PyPI**

  ```
  $ pip install mlx-component-catalog-connector
  ```

**Install from source code**

   ```
   $ git clone https://github.com/elyra-ai/examples.git
   $ cd examples/component-catalog-connectors/mlx-connector/
   $ make source-install
   ```

### Use the connector

1. Launch JupyterLab.
1. [Open the '`Manage Components`' panel](
https://elyra.readthedocs.io/en/stable/user_guide/pipeline-components.html#managing-custom-components-using-the-jupyterlab-ui).
1. Add a new MLX component catalog ('`+`' > '`New Machine Learning Exchange Component Catalog`').
1. Specify a catalog name, e.g. '`MLX dev catalog`'.
1. (Optional) Specify a category under which the catalog's components will be organized in the palette.
1. Configure the `MLX API URL`, e.g. '`http://my-mlx-server.mydomain:8080/`'. 
   > Note: The Machine Learning Exchange API URL is different from the GUI URL!
1. Apply an optional filter expression to the component names. The `*` (zero or more characters) and `?` (zero or one character) wildcards are supported.
1. Save the catalog entry.
1. Open the Kubeflow Pipelines Visual Pipeline Editor and expand the palette. The catalog components are displayed.

### Uninstall the connector

1. Remove all MLX catalog entries from the '`Manage Components`' panel.
1. Stop JupyterLab.
1. Uninstall the `mlx-component-catalog-connector` package.
   ```
   $ pip uninstall -y mlx-component-catalog-connector
   ```

### Troubleshooting

**Problem: The palette does not display any components from the configured catalog.**

**Solution:** If the the Elyra GUI does not display any error message indicating that a problem was encountered, inspect the JupyterLab log file.

Example error message (The specified MLX URL is invalid):

```
Error fetching component list from MLX catalog http://localhost:8080: ... Failed to establish a new connection: [Errno 61] Connection refused'
```
