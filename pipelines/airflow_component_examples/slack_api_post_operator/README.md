##slack_api_post_operator

See [Slack API Post Operator](https://airflow.apache.org/docs/apache-airflow/1.10.12/_modules/airflow/operators/slack_operator.html) documentation for more information

Required Parameters:
- slack_conn_id
- channel 
- text

This example uses the alpine Image. This requires a connection be created in the `Admin` menu of Airflow under `connections` to be
referenced as the `slack_conn_id` here. 
