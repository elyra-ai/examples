### Filter text component

Use the [_filter text_ example component](https://github.com/elyra-ai/elyra/blob/master/etc/config/components/kfp/filter_text_using_shell_and_grep.yaml) to find lines in a text file that contain the specified string pattern.

### Prerequisites

None. The example pipeline should work as is.

### Parameters

- **Text** (required). The text file to be filtered.
- **Pattern** (optional, defaults to `.*`)

### Outputs

- **Filtered text**. File containing only lines that matched the specified pattern.
