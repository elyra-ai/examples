## Artifactory component catalog connector

This catalog connector enables Elyra to load Kubeflow Pipelines components from a generic-type Artifactory repo.

> 🟨 __Note__ 🟨
>
> Currently, this connector only works with `--runtime_type=KUBEFLOW_PIPELINES`, 
> we welcome contributions for other runtime types.

## Install the connector

You can install the Artifactory catalog connector from PyPI or source code.

### Prerequisites

- [Elyra](https://elyra.readthedocs.io/en/stable/getting_started/installation.html) (version 3.7 and above)
- A [generic-type](https://www.jfrog.com/confluence/display/JFROG/Repository+Management#RepositoryManagement-GenericRepositories) Artifactory repo

### Install from PyPI

```bash
$ pip install elyra-artifactory-catalog-connector
```

### Install from source code

```bash
$ git clone https://github.com/elyra-ai/examples.git
$ cd examples/component-catalog-connectors/artifactory-connector/
$ make source-install
```

## Create a Catalog

### From the UI

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

### From the CLI

```bash
$ elyra-metadata install component-catalogs \
    --schema_name="artifactory-catalog" \
    --name="my_artifactory" \
    --display_name="My Artifactory" \
    --description="components from my artifactory" \
    --runtime_type="KUBEFLOW_PIPELINES" \
    --categories='["My Artifactory"]' \
    --artifactory_url="https://example.com/artifactory/" \
    --repository_name="my-kubeflow-components" \
    --repository_path="/" \
    --max_recursion_depth="3" \
    --max_files_per_folder="-1" \
    --file_filter="*.yaml" \
    --file_ordering="VERSION_DESCENDING"
```

## Documentation

### Introduction

The basic idea, is to create a [generic-type](https://www.jfrog.com/confluence/display/JFROG/Repository+Management#RepositoryManagement-GenericRepositories)
Artifactory repo with a folder structure similar to the following:

```
my_component_1/
   __COMPONENT__
   1.0.0.yaml
   1.1.0.yaml
   2.0.0.yaml
my_component_2/
   __COMPONENT__
   1.0.0.yaml
   1.1.0.yaml
   2.0.0.yaml
special_components/
   special_component_1/
      __COMPONENT__
      1.0.0.yaml
      1.1.0.yaml
      2.0.0.yaml
   special_component_2/
      __COMPONENT__
      1.0.0.yaml
      1.1.0.yaml
      2.0.0.yaml
```

The most important thing to understand are the `__COMPONENT__` marker files, which tell the connector that a folder contains a component.

1. The content of the `__COMPONENT__` files is not considered, only the fact that they exist.
2. The presence of a `__COMPONENT__` file in a folder prevents further recursion into sub-folders of that folder.

### Catalog Configs

| Name                         | CLI Parameter          | Description                                                                                                                                                                                                                                                                            | Example                            | Required |
|------------------------------|------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------|----------|
| Artifactory URL              | `artifactory_url`      | URL of the Artifactory server                                                                                                                                                                                                                                                          | `https://example.com/artifactory/` | YES      |
| Artifactory Username         | `artifactory_username` | Username for the Artifactory server                                                                                                                                                                                                                                                    | `service_user`                     | NO       |
| Artifactory Password/API-Key | `artifactory_password` | Password or API Key for the Artifactory server                                                                                                                                                                                                                                         | `password123`                      | NO       |
| Repository Name              | `repository_name`      | Name of the Artifactory repository                                                                                                                                                                                                                                                     | `my-kubeflow-components`           | YES      |
| Repository Path              | `repository_path`      | Path of folder in repository to search under                                                                                                                                                                                                                                           | `/path/to/components/`             | YES      |
| Maximum Recursion Depth      | `max_recursion_depth`  | Maximum folder depth to recurse looking for `__COMPONENT__` marker files                                                                                                                                                                                                               | `3`                                | YES      |
| Maximum Files Per Folder     | `max_files_per_folder` | Maximum number of files returned from each folder. ('-1' is unlimited)                                                                                                                                                                                                                 | `-1`                               | YES      |
| File Filter                  | `file_filter`          | Fnmatch file name filter.<br> `*` match everything;<br> `?` any single character;<br> `[seq]` character in seq;<br> `[!seq]` character not in seq;<br> `[0-9]` any single number;                                                                                                      | `*.yaml`                           | YES      |
| File Ordering                | `file_ordering`        | Order in which files are processed per folder.<br> `NAME_ASCENDING` alphanumeric ascending;<br> `NAME_DESCENDING` alphanumeric descending;<br> `VERSION_ASCENDING` packaging.version.LegacyVersion() ascending;<br> `VERSION_DESCENDING` packaging.version.LegacyVersion() descending; | `VERSION_DESCENDING`               | YES      |

### Component Versioning 

Kubeflow has no native concept of "versioning" the same Component YAML over time ([proposal to add one](https://github.com/kubeflow/pipelines/issues/7832)).

If changes are made to a Component's YAML, existing pipelines may break or do unexpected things.
Given this, we recommend __treating each Component YAML as atomic__, and creating a new YAML file for every change (never updating the old ones).

When doing this, using [Semantic Versions](https://semver.org/) for file names is sensible.
For example, you may initially create a file called `0.1.0.yaml`, then make a change and create a new file called `X.X.X.yaml`
(the appropriate version number depends on if the change was backwards-compatible or not).

> 🟦 __Tip__ 🟦
>
> Make sure to include the version in each component's `name` so they can be distinguished in the Elyra UI.
> 
> For example, this component has `1.0.0` in its `name`:
> 
> ```yaml
> name: My Component - 1.0.0
> description: ""
> inputs: []
> outputs: []
> implementation: {}
> ```

> 🟥 __Warning__ 🟥
>
> For Elyra to run a pipeline with components from a catalog, 
> those components must be present in one of your catalogs.
>
> This means your catalogs must continue to include ALL old component versions, 
> otherwise pipelines using old components will be unable to run.
>
> To keep the UI clean, you may want to create TWO catalog instances:
> 
> 1. that ONLY has the LATEST version of each component:
>     - set `max_files_per_folder` to `1`
>     - set `file_ordering` to `VERSION_DESCENDING`
> 2. that has ALL versions of each component:
>     - set `max_files_per_folder` to `-1`

## Examples

Assume an artifactory server `https://example.com/artifactory/` has a repository called `elyra-components` 
with the following folder structure:

```
component_one/
   __COMPONENT__
   1.0.0.yaml
   2.0.0.yaml
missing_marker/
   1.0.0.yaml
   2.0.0.yaml
component_group/
   component_two/
      __COMPONENT__
      1.0.0.yaml
      2.0.0.yaml
      nested_component/
         __COMPONENT__
         1.0.0.yaml
         2.0.0.yaml
   component_three/
      __COMPONENT__
      1.0.0.yaml
      2.0.0.yaml
```

### Example 1

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
/component_one/1.0.0.yaml
/component_one/2.0.0.yaml
/component_group/component_two/1.0.0.yaml
/component_group/component_two/2.0.0.yaml
/component_group/component_three/1.0.0.yaml
/component_group/component_three/2.0.0.yaml

Notes:
=========
- the `/missing_marker` files are not matched as this folder does not contain a `__COMPONENT__` marker
- the `/component_group/component_two/nested_component` files are not matched as recursion stops at the first `__COMPONENT__` marker
```

### Example 2

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
/component_one/2.0.0.yaml
/component_group/component_two/2.0.0.yaml
/component_group/component_three/2.0.0.yaml

Notes:
=========
- as `max_files_per_folder` is `1`, only ONE file from each folder is matched 
- as `file_ordering` is `VERSION_DESCENDING`, the HIGHEST version file is returned
   - we use `packaging.version.LegacyVersion()` to preform the sort
   - the `file_ordering` is applied separately within each folder
   - the WHOLE file-name is treated as a version, so "aaaa-1.0.0.yaml" would be sorted before "bbbb-9.0.0.yaml"
     (to avoid this problem, don't include any prefix on file names, for example `1.0.0.yaml`, `1.1.0.yaml`)
```

### Example 3

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
NONE

Notes:
=========
- no files are matched, as `max_recursion_depth` is `0`, and there is no component at the root
```

## Uninstall the connector

1. Remove all Artifactory catalog entries from the `Manage Components` panel
2. Stop JupyterLab
3. Uninstall the `elyra-artifactory-catalog-connector` package:
   ```bash
   $ pip uninstall elyra-artifactory-catalog-connector
   ```

## Troubleshooting

- __Problem:__ The palette does not display any components from the configured catalog.
   - __Solution:__ If the Elyra GUI does not display any error message indicating that a problem was encountered, inspect the JupyterLab log file.
