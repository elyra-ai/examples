##spark_submit_operator

See [Spark Submit Operator](https://airflow.apache.org/docs/apache-airflow/1.10.12/_api/airflow/contrib/operators/spark_submit_operator/index.html) documentation for more information

Required Parameters:
- application
- conn_id
- total_executor_cores (Standalone & Mesos only) 
- name 
- num_executors 
- application_args 

This example requires a Non Kerberos spark standalone deployment and the `spark_default` connection in Airflow to be configured correctly to the standalone deployment.