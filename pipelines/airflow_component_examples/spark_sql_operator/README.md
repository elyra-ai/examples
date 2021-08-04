##spark_sql_operator

See [Spark SQL Operator](https://airflow.apache.org/docs/apache-airflow/1.10.12/_api/airflow/contrib/operators/spark_sql_operator/index.html) documentation for more information

Required Parameters:
- sql
- conn_id
- total_executor_cores (Standalone & Mesos only)
- master
- name

This example requires a Non Kerberos spark standalone deployment and the `spark_sql_default` connection in Airflow to be configured correctly to the standalone deployment.