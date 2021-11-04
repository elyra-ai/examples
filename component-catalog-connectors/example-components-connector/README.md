## Elyra pipeline component examples catalog

This catalog connector enables Elyra to load example pipeline components.

### Install the connector

You can install the example component connector from PyPI or source code. Note that a **rebuild of JupyterLab is not required**.

**Prerequisites**

- [Install Elyra](https://elyra.readthedocs.io/en/stable/getting_started/installation.html) (version 3.3 and above).

**Install from PyPI**

  ```
  $ pip install elyra-example-components-catalog
  ```

**Install from source code**

   ```
   $ git clone https://github.com/elyra-ai/examples.git
   $ cd examples/component-catalog-connectors/elyra-examples-connector/
   $ make clean source-install
   ```

### Use the connector

1. Launch JupyterLab.
1. [Open the `Manage Components` panel](
https://elyra.readthedocs.io/en/stable/user_guide/pipeline-components.html#managing-custom-components-using-the-jupyterlab-ui).
1. Add a new component examples catalog ('`+`' > '`New Elyra examples component catalog`').
1. Specify a catalog name, e.g. '`Elyra example components`'.
1. Select a runtime from the list.
1. (Optional) Specify a category under which the example components will be organized in the palette.
1. Save the catalog entry.
1. Open the Visual Pipeline Editor for the chosen runtime and expand the palette. The example components are displayed.

### Uninstall the connector

1. Remove all example catalog entries from the '`Manage Components`' panel.
1. Stop JupyterLab.
1. Uninstall the `elyra-example-components-catalog` package.
   ```
   $ pip uninstall -y elyra-example-components-catalog
   ```

### Troubleshooting

**Q: No example components are displayed in the Visual Pipeline Editor palette.**
A: Verify that you imported the examples for the correct runtime environment and check the JupyterLab log file for error messages.