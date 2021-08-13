### Run notebook component

Use the [_run notebook_ example component](https://github.com/elyra-ai/elyra/blob/master/etc/config/components/kfp/run_notebook_using_papermill.yaml) to run a Jupyter notebook using [Papermill](https://papermill.readthedocs.io/en/latest/).

### Prerequisites

To use this component, please follow this setup:

Example:
We want to use a file called `notebook.ipynb` as our `notebook` parameter, and `notebook.ipynb` was located in a subdirectory of the 
root workspace, we would need to add a symlink to the notebook file in the Jupyterlab workspace root directory.

NOTE: If the data being used is already located in your Jupyterlab root workspace, you do not need to follow any further.
```
/Users/elyra/workspace/subdirectory/notebook.ipynb
----------------------                 --------
           |                               |
     JL root workspace                actual file    
```
```
/Users/elyra/workspace/notebook.ipynb
---------------------      -------
           |                  |
 JL root workspace         symlink    
```
This symlink would contain the relative path to the data file needed and be identically named. This link would provide
the relative path to the `notebook.ipynb` file. To create the symlink,  

First navigate to your Jupyterlab root workspace. Then run
```bash
ln -s <relative path to file> <filename>

Ex.

ln -s subdirectory/notebook.ipynb notebook.ipynb
```

### Parameters

- **Notebook** (required). The Jupyter notebook to run.
- **Parameters** (optional, defaults to `{}` - no parameters). Parameters to be passed to the notebook.
- **Packages to install** (optional, defaults to `[]` - no packages). Packages to be installed.
- **Input data** (optional). If set, variable `INPUT_DATA_PATH` points to a file that contains the provided input data.

### Outputs

- **Notebook**. The executed notebook.
- **Output data**. Variable `OUTPUT_DATA_PATH` points to a directory where the notebook can store output files.
