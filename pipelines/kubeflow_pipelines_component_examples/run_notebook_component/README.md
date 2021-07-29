### Run notebook component

Use the [_run notebook_ example component](https://github.com/elyra-ai/elyra/blob/master/etc/config/components/kfp/run_notebook_using_papermill.yaml) to run a Jupyter notebook using [Papermill](https://papermill.readthedocs.io/en/latest/).

### Prerequisites

None. The example pipeline should work as is.

### Parameters

- **Notebook** (required). The Jupyter notebook to run.
- **Parameters** (optional, defaults to `{}` - no parameters). Parameters to be passed to the notebook.
- **Packages to install** (optional, defaults to `[]` - no packages). Packages to be installed.
- **Input data** (optional). If set, variable `INPUT_DATA_PATH` points to a file that contains the provided input data.

### Outputs

- **Notebook**. The executed notebook.
- **Output data**. Variable `OUTPUT_DATA_PATH` points to a directory where the notebook can store output files.
