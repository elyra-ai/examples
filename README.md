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

# Elyra examples

This repository provides a set of examples that explore some of the unique
features provided by Elyra. All examples require Elyra version 2.3.x.

Examples for earlier releases:
 - [`v2.2.x`](https://github.com/elyra-ai/examples/tree/v2.2.x)

## Pipelines

Use the Elyra Visual Pipeline Editor to [assemble pipelines from Python notebooks or scripts](https://elyra.readthedocs.io/en/latest/user_guide/pipelines.html) without the need for any coding.

### Pipeline tutorials

Tutorials to get started with generic pipelines in Elyra:
- [Introduction to generic pipelines](pipelines/introduction-to-generic-pipelines)
- [Run generic pipelines on Kubeflow Pipelines](pipelines/run-generic-pipelines-on-kubeflow-pipelines)
- [Run generic pipelines on Apache Airflow](pipelines/run-generic-pipelines-on-apache-airflow)

### Example pipelines
This repository includes the following example pipelines:
- [Analyzing NOAA weather data](pipelines/dax_noaa_weather_data)
- [Visualize outputs in the Kubeflow Pipelines UI](pipelines/visualize_output_in_kubeflow_pipelines_ui)

### Example pipelines in third-party repositories
Pipelines that were created by the community:
- [Analyzing COVID-19 time series data](https://github.com/CODAIT/covid-notebooks)
- [Analyzing flight delays](https://github.com/CODAIT/flight-delay-notebooks)
