##bash_operator

See [Bash Operator](https://airflow.apache.org/docs/apache-airflow/1.10.12/howto/operator/bash.html) documentation for more information

Required Parameters:
- Runtime Image
- Available Operators
- Bash Command
- Xcom Push 
- Env or Environmental Variables
- Output Encoding

This example uses the Anaconda Image. It will set a test environmental variable and prints it out along with the hosts file of the container. 
This information is then pushed to xcoms to be relayed to other tasks in the DAG.