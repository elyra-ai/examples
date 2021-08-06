## spark_submit_operator

See [Spark Submit Operator](https://airflow.apache.org/docs/apache-airflow/1.10.12/_api/airflow/contrib/operators/spark_submit_operator/index.html) documentation for more information.

The example pipeline is configured to run the  "Calculate Pi" example distributed with Apache Spark.

### Prerequisites

This example requires a Non Kerberos spark standalone deployment and the `spark_sql_default` connection in Airflow to be configured correctly to the standalone deployment.
Directions on how to set up an Apache Spark standalone deploy can be found [here](https://spark.apache.org/docs/latest/spark-standalone.html).

The operator utilizes a pre-configured `spark_sql_default` connection.

Configure a connection with that id:
 1. Open the Airflow GUI
 1. Navigate to `Admin` > `Connections`
 1. Create a new connection, specifying the following:
    - Connection id:   `spark_sql_default`
    - Connection type: `Spark`
    - ...

### Parameters

- **application** (required). The application (`.py` or `.jar`) to submit to Spark to run. The application must reside on the Airflow host deployment and accessible by Airflow in the file system.
- **conf**. See operator documentation.
- **conn_id** (required). The connection ID to use to connect to Spark. Default is set to "spark_sql_default".
- **files**. See operator documentation.
- **py_files**. See operator documentation.
- **archives**. See operator documentation.
- **driver_class_path**. See operator documentation.
- **jars**. See operator documentation.
- **java_class**. See operator documentation.
- **packages**. See operator documentation.
- **exclude_packages**. See operator documentation.
- **repositories**. See operator documentation.
- **total_executor_cores**. See operator documentation.
- **executor_cores**. See operator documentation.
- **executor_memory**. See operator documentation.
- **driver_memory**. See operator documentation.
- **keytab**. See operator documentation.
- **principal**. See operator documentation.
- **proxy_user**. See operator documentation.
- **name** (required). The spark job name.
- **num_executors**. See operator documentation.
- **status_poll_interval**. See operator documentation.
- **application_args**. See operator documentation.
- **env_vars**. See operator documentation.
- **verbose**. See operator documentation.
- **spark_binary**. See operator documentation.

### Outputs

None.