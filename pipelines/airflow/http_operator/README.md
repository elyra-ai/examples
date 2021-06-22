##http_operator

See [HTTP Operator](https://airflow.apache.org/docs/apache-airflow/1.10.12/_api/airflow/operators/http_operator/index.html) documentation for more information

Apache Airflow Connection Configuration Prerequisites:
- In the Airflow UI, under `Admin` -> `Connections`, scroll down to `http_default`. This connection defines the default
connection all http_operators will use unless otherwise configured. Modify the `Host` to `https://api.github.com`. Save and exit.

Required Parameters:
- Runtime Image
- Available Operators
- endpoint 
- method
- data
- headers
- response_check
- extra options
- xcom push
- http_conn_id - This id is the name of the connection we configured earlier (http_default), but can be configured to any http connection we wish.
- log response

This example uses the Anaconda Image. It sends a email to the recipient with the subject line "test". 