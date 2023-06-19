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
## Component catalog connectors

Component catalog connectors provide Elyra's Visual Pipeline Editor access to [local and remote catalogs](https://elyra.readthedocs.io/en/stable/user_guide/pipeline-components.html#component-catalogs) that store [pipeline components](https://elyra.readthedocs.io/en/stable/user_guide/pipeline-components.html). 

![Component catalog connectors](doc/images/component-catalogs.png)

This directory contains component catalog connector implementations for
- [Kubeflow Pipelines example components](kfp-example-components-connector)
- [Apache Airflow example operators](airflow-example-components-connector)
- [Artifactory](artifactory-connector)
- [Machine Learning Exchange](mlx-connector)

The connectors listed above are maintained by the Elyra community. You can find a complete list of available connectors on [this page](connector-directory.md) or learn how to [build your own](build-a-custom-connector.md).
