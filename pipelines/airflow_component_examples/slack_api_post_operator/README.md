##slack_api_post_operator

See [Slack API Post Operator](https://airflow.apache.org/docs/apache-airflow/1.10.12/_modules/airflow/operators/slack_operator.html) documentation for more information

Required Parameters:
- slack_conn_id
    - The connection ID to use to connect to slack
    - Default is set to "slack_default"
- channel
    - The channel you wish to post to. Must be a public channel or a channel that the token has "chat:write" access to
    - Default is set to "#general"
- text
    - The message you want to 

This requires a connection be created in the `Admin` menu of Airflow under `connections` to be referenced as the `slack_conn_id` here. 
