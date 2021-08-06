## slack_api_post_operator

See [Slack API Post Operator](https://airflow.apache.org/docs/apache-airflow/1.10.12/_modules/airflow/operators/slack_operator.html) documentation for more information.

### Prerequisites

The operator utilizes a pre-configured `slack_conn_id`, which is set in the example pipeline to `slack_default`.

Configure a connection with that id:
 1. Open the Airflow GUI
 1. Navigate to `Admin` > `Connections`
 1. Create a new connection, specifying the following:
    - Connection id:   `slack_default`
    - Connection type: `HTTP`
    - Host: `https://hooks.slack.com/services/`

### Parameters

- **slack_conn_id** (required). The connection ID to use to connect to slack. Default is set to "slack_default"
- **token** (required). Slack API token.
- **api_parameters**. See operator documentation.
- **channel** (required). The channel you wish to post to. Must be a public channel or a channel that the token has "chat:write" access to. Default is set to "#general"
- **username**. Username under which the message is posted.
- **text** (required). The message to send.
- **icon_url**. See operator documentation.
- **attachments**. See operator documentation.
- **blocks**. See operator documentation. 

### Outputs

None.