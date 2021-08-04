##spark_submit_operator

See [Spark Submit Operator](https://airflow.apache.org/docs/apache-airflow/1.10.12/_api/airflow/contrib/operators/spark_submit_operator/index.html) documentation for more information

Required Parameters:
- application
    - The application (py or jar) to submit to Spark to run. The application must reside on the airflow host deployment and accessible by airflow in the file system.
    - Currently configured to run the sample "Calculate Pi" example distributed with Apache Spark
- conn_id
    - conn_id
    - Airflow connection ID to use
    - defined as "spark_default" in the sample pipeline
- name 
    - give the job a name 
    - default is "airflow-spark"

This example requires a Non Kerberos spark standalone deployment and the `spark_default` connection in Airflow to be configured correctly to the standalone deployment.
Directions on how to setup an Apache Spark standalone deploy can be found [here](https://spark.apache.org/docs/latest/spark-standalone.html)