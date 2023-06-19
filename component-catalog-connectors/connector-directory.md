<!--
{% comment %}
Copyright 2018-2023 Elyra Authors

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
## Component catalog connector directory

The following catalog connectors should work with Elyra version 3.3 and above. Connectors are provided as-is and, unless specified otherwise, are not maintained by the Elyra core committers. 

- To add your connector to the list [create a pull request](https://github.com/elyra-ai/examples/pulls). 
- Learn [how to build your own catalog connector](build-a-custom-connector.md).

| Connector | Description |
| --- | --- |
| [Apache Airflow example catalog](airflow-example-components-connector) | Provides access to a small set of curated Apache Airflow operators that you can use to get started with the Visual Pipeline Editor. |
| [Kubeflow Pipelines example catalog](kfp-example-components-connector) | Provides access to a small set of curated Kubeflow Pipelines components that you can use to get started with the Visual Pipeline Editor. |
| [Artifactory](artifactory-connector) | Enables Elyra to load Kubeflow Pipelines components from a generic-type Artifactory repo. |
| [Machine Learning Exchange](mlx-connector/) | This LFAI project provides an open source Data and AI assets catalog and execution engine for Kubeflow Pipelines.  |

