## http_operator

Use the [`http_operator`](https://airflow.apache.org/docs/apache-airflow/1.10.12/_api/airflow/operators/http_operator/index.html) to call an endpoint on an HTTP system.

In the example pipeline the operator is configured to query the [location of the International Space Station](https://wheretheiss.at/) by sending a `GET` request to `https://api.wheretheiss.at/v1/satellites/25544`.

### Prerequisites

The operator utilizes a pre-configured `http_conn_id`, which is set in the example pipeline to `http_iss`.

Configure a connection with that id:
 1. Open the Airflow GUI
 1. Navigate to `Admin` > `Connections`
 1. Create a new connection, specifying the following:
    - Connection id:   `http_iss`
    - Connection type: `HTTP`
    - Host: `api.wheretheiss.at`
    - Schema: `https` 

### Parameters

- **endpoint**. The relative part of the URL.  
- **method**. The HTTP method, e.g. `GET`
- **data**. The data to pass.
- **headers**. HTTP headers to be added to `GET` requests.
- **response_check**. See operator description.
- **extra options**. See operator description.
- **xcom_push**. If enabled, the last line written to stdout is pushed to XCom. 
- **http_conn_id**. Id of the preconfigured HTTP  connection.
- **log response**.

### Outputs

If `xcom_push` is enabled, the last line written to stdout is pushed to XCom. 