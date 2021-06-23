## bash_operator

### Overview

Use the [`BashOperator`](https://airflow.apache.org/docs/apache-airflow/1.10.12/howto/operator/bash.html) to execute commands in a Bash shell.

The example pipeline displays the content of the `/etc/hosts` file and the value of environment variable `TEST_ENV`. The value of `TEST_ENV` is also pushed to XCom to make it available to other DAG tasks.

### Prerequisites

None. The example pipeline should work as is.

### Parameters
- Runtime Image
- Available Operators
- Bash Command
- Xcom Push 
- Env or Environment Variables
- Output Encoding
