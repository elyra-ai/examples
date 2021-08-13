### Filter text component

Use the [_filter text_ example component](https://github.com/elyra-ai/elyra/blob/master/etc/config/components/kfp/filter_text_using_shell_and_grep.yaml) to find lines in a text file that contain the specified string pattern.

### Prerequisites
To use this component, please follow this setup:

Example:
We want to use a file called `data.csv` as our `text` parameter, and `data.csv` was located in a subdirectory of the 
root workspace, we would need to add a symlink to the data file in the Jupyterlab workspace root directory.

NOTE: If the data being used is already located in your Jupyterlab root workspace, you do not need to follow any further.
```
/Users/elyra/workspace/subdirectory/data.csv
----------------------              --------
           |                            |
     JL root workspace             actual file    
```
```
/Users/elyra/workspace/data.csv
---------------------  -------
           |              |
 JL root workspace     symlink    
```
This symlink would contain the relative path to the data file needed and be identically named. This link would provide
the relative path to the `data.csv` file. To create the symlink,  

First navigate to your Jupyterlab root workspace. Then run
```bash
ln -s <relative path to file> <filename>

Ex.

ln -s subdirectory/data.csv data.csv
```

### Parameters

- **Text** (required). The text file to be filtered.
- **Pattern** (optional, defaults to `.*`)

### Outputs

- **Filtered text**. File containing only lines that matched the specified pattern.
