## bash_operator

Use the [`BashOperator`](https://airflow.apache.org/docs/apache-airflow/1.10.12/howto/operator/bash.html) to execute commands in a Bash shell.

The example pipeline displays the content of the `/etc/hosts` file and the value of environment variable `TEST_ENV`. The value of `TEST_ENV` is also pushed to XCom to make it available to other DAG tasks.

### Prerequisites

None. The example pipeline should work as is.

### Parameters

- **Bash Command** (required). The command(s) or script to execute.
- **xcom_push**. If enabled, the last line written to stdout is pushed to XCom. 
- **Env**. Environment variables to be defined for the process where the bash command is executed. Use the following format:
  ```
  {
      "env_var_name": "env var value",
      "another_env_var": "another value" 
  }
  ```
  If not specified, the current process environment variables are used.
- **Output Encoding**. Output encoding of the bash command.

### Outputs

If `xcom_push` is enabled, the last line written to stdout is pushed to XCom. 