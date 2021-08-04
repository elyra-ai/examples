##spark_sql_operator

See [Spark SQL Operator](https://airflow.apache.org/docs/apache-airflow/1.10.12/_api/airflow/contrib/operators/spark_sql_operator/index.html) documentation for more information

Required Parameters:
- sql
    - The SQL query to run on the spark hive metastore
- conn_id
    - Airflow connection ID to use
    - defined as "spark_sql_default" in the sample pipeline
- name
    - name the spark job 

This example requires a Non Kerberos spark standalone deployment and the `spark_sql_default` connection in Airflow to be configured correctly to the standalone deployment.
Directions on how to setup an Apache Spark standalone deploy can be found [here](https://spark.apache.org/docs/latest/spark-standalone.html)