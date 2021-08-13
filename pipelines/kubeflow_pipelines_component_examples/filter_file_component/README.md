### Filter text component

Use the [_filter text_ example component](https://github.com/elyra-ai/elyra/blob/master/etc/config/components/kfp/filter_text_using_shell_and_grep.yaml) to find lines in a text file that contain the specified string pattern.

### Prerequisites
To use this component, ensure that you create your pipeline with the accompanying `textfile` in your Jupyterlab workspace root directory.

### Parameters

- **Text** (required). The text file to be filtered.
- **Pattern** (optional, defaults to `.*`)

### Outputs

- **Filtered text**. File containing only lines that matched the specified pattern.
