## TODO component catalog connector

This catalog connector enables Elyra to load pipelines components from TODO.

### Install the connector

You can install the TODO catalog connector from PyPI or source code. Note that a **rebuild of JupyterLab is not required**.

**Prerequisites**

- [Elyra](https://elyra.readthedocs.io/en/stable/getting_started/installation.html) (version 3.3 and above).
- TODO

**Install from PyPI**

  ```
  $ pip install todo-component-catalog-connector
  ```

**Install from source code**

   ```
   $ git clone https://github.com/elyra-ai/examples.git
   $ cd examples/component-catalog-connectors/connector-template/
   $ make source-install
   ```

### Use the connector

1. Launch JupyterLab.
1. [Open the '`Manage Components`' panel](
https://elyra.readthedocs.io/en/stable/user_guide/pipeline-components.html#managing-custom-components-using-the-jupyterlab-ui).
1. Add a new TODO component catalog ('`+`' > '`New TODO  Component Catalog`').
1. Specify a catalog name, e.g. '`Test TODO catalog`'.
1. (Optional) Specify a category under which the catalog's components will be organized in the palette.
1. Configure the required `todo_required_parm`.
1. COnfigure the optional `todo_optional_parm`.
1. Save the catalog entry.
1. Open the Visual Pipeline Editor and expand the palette. The catalog components are displayed.

### Uninstall the connector

1. Remove all TODO catalog entries from the '`Manage Components`' panel.
1. Stop JupyterLab.
1. Uninstall the `todo-component-catalog-connector` package.
   ```
   $ pip uninstall -y todo-component-catalog-connector
   ```

### Troubleshooting

**Problem: The palette does not display any components from the configured catalog.**

**Solution:** If the the Elyra GUI does not display any error message indicating that a problem was encountered, inspect the JupyterLab log file.
