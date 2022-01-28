<!--
{% comment %}
Copyright 2018-2022 Elyra Authors

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
## Pipeline runtime environment setup validation

Use the pipeline(s) in this directory to verify that your runtime environments and runtime configurations are set up properly.

### Validating the JupyterLab setup

To validate that you can run pipelines in your JupyterLab environment complete the steps below. If you are new to Elyra, please [review the introductory tutorial](https://github.com/elyra-ai/examples/tree/master/pipelines/hello_world) before proceeding.

1. In the File Explorer open `validate_python.pipeline` in the Visual Pipeline editor. The pipeline runs a trivial notebook and Python script.
1. In the Visual Pipeline editor click the "Run" button.
1. In the Run dialog choose `Local Runtime` as _Runtime Platform_.
1. Run the pipeline.

If the pipeline runs without any issues your basic setup is ok for Python scripts and notebooks that utilize a plain Python kernel.

### Validating a Kubeflow Pipelines setup

To validate that you can run pipelines in your JupyterLab environment complete the steps below. If you are new to Elyra, please [review the introductory tutorial](https://github.com/elyra-ai/examples/tree/master/pipelines/hello_world_kubeflow_pipelines) before proceeding.

Prerequisites:
- Kubeflow v1.2 or v1.3 is deployed
- [Runtime configuration is associated with this Kubeflow deployment](https://elyra.readthedocs.io/en/stable/user_guide/runtime-conf.html)

Steps:
1. In the File Explorer open `validate_python.pipeline` in the Visual Pipeline editor. The pipeline runs a trivial notebook and Python script.
1. In the Visual Pipeline editor click the "Run" button.
1. In the Run dialog choose `Kubeflow Pipelines` as _Runtime Platform_, and select the runtime configuration you've created.
1. Submit the pipeline. 
1. If the submission dialog indicates that an error occurred, check your runtime configuration and try again. 
1. If the submission succeeded open the Kubeflow Central dashboard link and [follow the monitoring steps outlined in the tutorial.](https://github.com/elyra-ai/examples/tree/master/pipelines/hello_world_kubeflow_pipelines#monitoring-a-pipeline-run)

### Validating an Apache Airflow setup

To validate that you can run pipelines in your Apache Airflow environment, follow the steps below. If you are new to Elyra, please [review the introductory tutorial](https://github.com/elyra-ai/examples/tree/master/pipelines/hello_world_apache_airflow) before proceeding.

1. [Create an Apache Airflow runtime configuration.](https://elyra.readthedocs.io/en/stable/user_guide/runtime-conf.html)
1. In the File Explorer open `validate_python.pipeline` in the Visual Pipeline editor. The pipeline runs a trivial notebook and Python script.
1. In the Visual Pipeline editor click the "Run" button.
1. In the Run dialog choose `Apache Airflow` as _Runtime Platform_, and select the runtime configuration you've created.
1. Submit the pipeline. 
1. If the submission dialog indicates that an error occurred, check your runtime configuration and try again. 
1. If the submission succeeded: 
   - Open the GitHub repository link and verify that a DAG with the pipeline name exists.
   - Open the Apache Airflow dashboard and [follow the monitoring steps outlined in the tutorial.](https://github.com/elyra-ai/examples/tree/master/pipelines/hello_world_apache_airflow#running-a-notebook-pipeline-on-apache-airflow)
