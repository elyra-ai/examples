## spark_sql_operator

See [Spark SQL Operator](https://airflow.apache.org/docs/apache-airflow/1.10.12/_api/airflow/contrib/operators/spark_sql_operator/index.html) documentation for more information.

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

- **sql** (required). The SQL to execute.
    - The SQL query to run on the spark hive metastore
- **conf**. See operator documentation.
- **conn_id** (required).The connection ID to use to connect to Spark. Default is set to "spark_sql_default".
- **total_executor_cores**. See operator documentation.
- **executor_cores**. See operator documentation.
- **executor_memory**. See operator documentation.
- **keytab**. See operator documentation.
- **principal**. See operator documentation.
- **master**. See operator documentation.
- **name** (required). The spark job name.
- **num_executors**. See operator documentation.
- **verbose**. See operator documentation.
- **yarn_queue**. See operator documentation.

### Outputs

None.