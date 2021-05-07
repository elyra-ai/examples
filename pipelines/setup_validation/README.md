<!--
{% comment %}
Copyright 2018-2020 Elyra Authors

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
{% endcomment %}
-->
## Pipeline setup validation

Use the pipeline(s) in this directory to verify that your runtime environments and runtime configurations are set up properly.

### Validating the JupyterLab setup

1. In the File Explorer open `validate_python.pipeline` in the Visual Pipeline editor.
1. In the Visual Pipeline editor click the "Run" button.
1. In the Run dialog choose `Local Runtime` as _Runtime Platform_.
1. Run the pipeline.

If the pipeline runs without any issues your basic setup is ok for Python scripts and notebooks that utilize a plain Python kernel.

### Validating a Kubeflow Pipelines setup

To validate that you can run pipelines in your Kubeflow Pipelines environment, follow the steps below. If you are new to Elyra, please [review the introductory tutorial](https://github.com/elyra-ai/examples/tree/master/pipelines/hello_world_kubeflow_pipelines) before proceeding.

1. [Create a Kubeflow Pipelines runtime configuration.](https://elyra.readthedocs.io/en/stable/user_guide/runtime-conf.html)
1. In the File Explorer open `validate_python.pipeline` in the Visual Pipeline editor.
1. In the Visual Pipeline editor click the "Run" button.
1. In the Run dialog choose `Kubeflow Pipelines` as _Runtime Platform_, and select the runtime configuration you've created.
1. Run the pipeline.
1. [Follow the monitoring steps outlined in the tutorial.](https://github.com/elyra-ai/examples/tree/master/pipelines/hello_world_kubeflow_pipelines#monitoring-a-pipeline-run)

If the pipeline runs without any issues
- the Kubeflow Pipelines runtime configuration in Elyra is ok
- the Kubeflow Pipelines deployment is ok for Python scripts and notebooks that utilize a plain Python kernel.

### Validating an Apache Airflow setup

To validate that you can run pipelines in your Apache Airflow environment, follow the steps below. If you are new to Elyra, please [review the introductory tutorial](https://github.com/elyra-ai/examples/tree/master/pipelines/hello_world_apache_airflow) before proceeding.

1. [Create an Apache Airflow runtime configuration.](https://elyra.readthedocs.io/en/stable/user_guide/runtime-conf.html)
1. In the File Explorer open `validate_python.pipeline` in the Visual Pipeline editor.
1. In the Visual Pipeline editor click the "Run" button.
1. In the Run dialog choose `Apache Airflow` as _Runtime Platform_, and select the runtime configuration you've created.
1. Run the pipeline.
1. [Follow the monitoring steps outlined in the tutorial.](https://github.com/elyra-ai/examples/tree/master/pipelines/hello_world_apache_airflow#running-a-notebook-pipeline-on-apache-airflow)

If the pipeline runs without any issues
- the Kubeflow Pipelines runtime configuration in Elyra is ok
- the Kubeflow Pipelines deployment is ok for Python scripts and notebooks that utilize a plain Python kernel.