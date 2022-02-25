## Artifactory component catalog connector

This catalog connector enables Elyra to load pipelines components from a generic-type Artifactory repo.

## Install the connector

You can install the Artifactory catalog connector from PyPI or source code. Note that a **rebuild of JupyterLab is not required**.

### Prerequisites

- [Elyra](https://elyra.readthedocs.io/en/stable/getting_started/installation.html) (version 3.3 and above)
- A [generic-type Artifactory repo](https://www.jfrog.com/confluence/display/JFROG/Repository+Management#RepositoryManagement-GenericRepositories)

### Install from PyPI

  ```
  $ pip install elyra-artifactory-catalog-connector
  ```

### Install from source code

   ```
   $ git clone https://github.com/elyra-ai/examples.git
   $ cd examples/component-catalog-connectors/artifactory-connector/
   $ make source-install
   ```

## Use the connector

### Add a new Artifactory catalog

1. Launch JupyterLab
2. Open the  [`Manage Components` panel](https://elyra.readthedocs.io/en/stable/user_guide/pipeline-components.html#managing-custom-components-using-the-jupyterlab-ui)
3. Click `+` then `New Artifactory Component Catalog`
4. Specify a "name" for the catalog
5. (Optional) Specify a "category name" under which the catalog's components will be organized in the palette
6. Specify the required "Source" parameters:
    - `artifactory_url`
    - `repository_name`
    - `repository_path`
    - `max_recursion_depth`
    - `max_files_per_folder`
    - `file_filter`
    - `file_ordering`
7. (Optional) Specify the optional "Source" parameters:
    - `artifactory_username`
    - `artifactory_password`
8. Save the catalog entry
9. Open the Visual Pipeline Editor and expand the palette. The catalog components are displayed.

### Recommended Usage

We recommend that you version your component YAML rather than having users always point to the latest version of each component.
Otherwise, when changes are made to `inputs`/`outputs`/`implementation`, existing pipelines may break or do unexpected things.

> 🟦 __Tip__ 🟦
>
> Include the version in each component's `name` so they can be distinguished in the Elyra UI.
>
> For example:
> ```yaml
> name: My Component - 1.0.0
> description: ""
> inputs: []
> outputs: []
> implementation: {}
> ```

Elyra only stores pointers to the source-catalog of each component in its `.pipeline` files.
This means your catalogs must continue to include ALL old component versions, otherwise old pipelines will be unable to run.

You can solve this problem with the `Artifactory Catalog Connector` by adding TWO catalog instances for your single Artifactory repo:

1. that has only the latest version of each component:
    - `max_files_per_folder = 1`
    - `file_ordering = VERSION_DESCENDING`
2. that has all versions of each component:
    - `max_files_per_folder = -1`

> 🟦 __Tip__ 🟦
>
> Name your component YAML files with consistent prefixes before the version.
> 
> This is because `VERSION_DESCENDING` treats the whole file-name as a version.
> For example, `aaaa-1.0.0.yaml` would be sorted before `bbbb-9.0.0.yaml`.
>
> Alternatively, don't include any prefix on file names, for example `1.0.0.yaml`, `1.1.0.yaml`.


### Example Configs

Assume an artifactory server `https://example.com/artifactory/` has a repository called `elyra-components` 
with the following folder structure:

```
component_1/
   __COMPONENT__
   component-1.0.9.yaml
   component-1.0.10.yaml
component_2/
   hidden_component/
      __COMPONENT__
      component-1.0.0.yaml
      component-1.1.0.yaml
   __COMPONENT__
   component-1.0.0.yaml
   component-1.1.0.yaml
component_3/
   component-1.0.0.yaml
   component-1.1.0.yaml
```

__Example 1:__

```
Configs:
=========
artifactory_url      = https://example.com/artifactory/
repository_name      = elyra-components
repository_path      = /
max_recursion_depth  = 3
max_files_per_folder = -1
file_filter          = *.yaml
file_ordering        = VERSION_DESCENDING

Matched:
=========
https://example.com/artifactory/elyra-components/component_1/component-1.0.9.yaml
https://example.com/artifactory/elyra-components/component_1/component-1.0.10.yaml
https://example.com/artifactory/elyra-components/component_2/component-1.0.0.yaml
https://example.com/artifactory/elyra-components/component_2/component-1.1.0.yaml

Notes:
=========
- the `component_3/` files are not matched as this folder does not contain a `__COMPONENT__` marker
- the `component_2/hidden_component/` files are not matched as recursion stops at the first `__COMPONENT__` marker
```

__Example 2:__

```
Configs:
=========
artifactory_url      = https://example.com/artifactory/
repository_name      = elyra-components
repository_path      = /
max_recursion_depth  = 0
max_files_per_folder = -1
file_filter          = *.yaml
file_ordering        = VERSION_DESCENDING

Matched:
=========
N/A

Notes:
=========
- no files are matched, as `max_recursion_depth` is `0`
```

__Example 3:__

```
Configs:
=========
artifactory_url      = https://example.com/artifactory/
repository_name      = elyra-components
repository_path      = /
max_recursion_depth  = 3
max_files_per_folder = 1
file_filter          = *.yaml
file_ordering        = VERSION_DESCENDING

Matched:
=========
https://example.com/artifactory/elyra-components/component_1/component-1.0.10.yaml
https://example.com/artifactory/elyra-components/component_2/component-1.1.0.yaml

Notes:
=========
- the `file_ordering` is applied separately within each folder
- as `max_files_per_folder` is `1`, only ONE file from each folder is matched 
- as `file_ordering` is `VERSION_DESCENDING`, the file names are ordered as if they are version numbers
  (we use `packaging.version.LegacyVersion()` to preform the sort)
- the whole file-name is treated as a version, so "aaaa-1.0.0.yaml" is sorted before "bbbb-9.0.0.yaml"
  (take care not to change your file-name prefixes, or alternatively don't include a prefix and use "1.0.0.ymal")
```

## Uninstall the connector

1. Remove all Artifactory catalog entries from the `Manage Components` panel
2. Stop JupyterLab
3. Uninstall the `elyra-artifactory-catalog-connector` package:
   ```
   $ pip uninstall elyra-artifactory-catalog-connector
   ```

## Troubleshooting

- __Problem:__ The palette does not display any components from the configured catalog.
   - __Solution:__ If the Elyra GUI does not display any error message indicating that a problem was encountered, inspect the JupyterLab log file.
- __Problem:__ The pallet does not reflect the current state of the Artifactory repo.
   - __Solution:__ Trigger the catalog to refresh by editing the catalog, and clicking "SAVE & CLOSE" (without making any changes).
