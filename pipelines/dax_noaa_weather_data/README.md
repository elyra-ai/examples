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
## Overview

This notebook pipeline downloads [a free NOAA weather time series data set archive from the Data Asset Exchange](https://developer.ibm.com/exchanges/data/all/jfk-weather-data/), extracts, cleanses and analyzes the data file. The data file is subsequently used to predict the weather. 

This pipeline illustrates the following concepts:
 - **Execute notebooks sequentially**. Notebook `Part 1 - Data Cleaning` runs after notebook `load_data` completed successfully.
 - **Execute notebooks in parallel**. Notebooks `Part 2 - Data Analysis` and `Part 3 - Time Series Forecasting` run in parallel after notebook `Part 1 - Data Cleaning` completed successfully.
 - **Pass input parameters to a notebook**. The generic `load_data` notebook requires an environment variable to be defined that identifies the public dataset download URL.
 - **Share data between notebooks**. Notebook `Part 1 - Data Cleaning` generates a data file `jfk_weather_cleaned.csv`, which is consumed in notebook `Part 2 - Data Analysis` and `Part 3 - Time Series Forecasting`.

![pipeline snapshot](doc/images/pipeline_snapshot.png)

You can run this pipeline as is locally in JupyterLab or on Kubeflow Pipelines.

 ## Prerequisites
 
 This pipeline requires Elyra v1.2 or later.

 ## Exploring the pipeline

 1. Launch JupyterLab, which has the [Elyra extension installed](https://elyra.readthedocs.io/en/latest/getting_started/installation.html).
 1. Clone the sample repository `https://github.com/elyra-ai/examples.git` using the Git extension ("Git" > "Clone repository").
 1. If you have access to a Kubeflow Pipelines deployment, [create a runtime environment configuration].(https://elyra.readthedocs.io/en/latest/user_guide/runtime-conf.html) 
 1. From the File Browser open `analyze_NOAA_weather_data.pipeline`, which is located in the `pipelines/dax_noaa_weather_data/` directory.
 1. Review the notebook properties (right click > "Properties").
 1. Review the notebooks (right click > "Open file").
 1. Run the pipeline. Two links are displayed.
 1. Open the Kubeflow Pipelines console link in a new browser window. You can monitor the pipeline execution progress by clicking on a node and opening the "Logs" tab. 
    ![pipeline graph](doc/images/pipeline_graph_and_output.png)
 1. Open the object storage link in another browser window to download the completed notebooks.
    ![object storage](doc/images/object_storage.png) 
 
