### Filter text component

Use the [_filter text_ example component](https://github.com/elyra-ai/elyra/blob/master/etc/config/components/kfp/filter_text_using_shell_and_grep.yaml) to find lines in a text file that contain the specified string pattern.

### Prerequisites
Ensure that you have the (Text) data downloaded and available via a download step prior to using this component.

To review and run the example pipeline for this component, [clone the examples repository](https://github.com/elyra-ai/examples) and launch JupyterLab as shown below:

```
$ jupyter lab --NotebookApp.notebook_dir=examples/pipelines/kubeflow_pipelines_component_examples/filter_file_component/
```

### Parameters

- **Text** (required). The text file to be filtered.
- **Pattern** (optional, defaults to `.*`)

### Outputs

- **Filtered text**. File containing only lines that matched the specified pattern.
