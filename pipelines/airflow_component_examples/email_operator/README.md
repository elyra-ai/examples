## email_operator

### Overview

Use the [`email_operator`](https://airflow.apache.org/docs/apache-airflow/1.10.12/_api/airflow/operators/email_operator/index.html) to send an email alert.

The example pipeline sends an email.

### Prerequisites

The Airflow helm deployment must be preconfigured with Email support prior to using this operator. The `config` stanza
in the [`values.yaml`](https://github.com/helm/charts/blob/master/stable/airflow/values.yaml) file can be edited to fulfill this requirement.

```yaml
       AIRFLOW__EMAIL__EMAIL_BACKEND: "airflow.utils.email.send_email_smtp"
       AIRFLOW__SMTP__SMTP_HOST: "smtpmail.example.com"
       AIRFLOW__SMTP__SMTP_STARTTLS: "False"
       AIRFLOW__SMTP__SMTP_SSL: "False"
       AIRFLOW__SMTP__SMTP_PORT: "25"
       AIRFLOW__SMTP__SMTP_MAIL_FROM: "admin@example.com"
```

### Parameters
- Runtime image
- Available Operators
- to (recipient)
- subject
- html content
- files (attachments)
- cc
- bcc
