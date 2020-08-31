## Getting started with notebook pipelines

A notebook pipeline comprises of notebook nodes that are connected with each other. While pipelines can be used to run any kinds of notebooks, they are commonly used to implement machine learning workflows.

![The completed tutorial pipeline](doc/images/completed_tutorial_pipeline.png)

Notebook pipelines can run locally in JupyterLab or remotely on Kubeflow Pipelines, a platform for building and deploying machine learning workflows based on Docker containers.

![Run a notebook pipeline locally or on Kubeflow Pipelines](doc/images/notebook_pipeline_local_and_remote.png)

In this tutorial you will learn how to create a notebook pipeline and run it on Kubeflow Pipelines. Take a look at the [Hello World tutorial](https://github.com/elyra-ai/examples/tree/master/pipelines/hello_world) to learn how to run notebook pipelines locally in JupyterLab. 

### Prerequisites

To complete this tutorial you need
- [JupyterLab 2.x with the Elyra extension v1.1 (or newer) installed](https://elyra.readthedocs.io/en/latest/getting_started/installation.html)
- Access to a [Kubeflow Pipelines](https://www.kubeflow.org/docs/pipelines/overview/pipelines-overview/) deployment

#### Information to collect collect before starting

Collect the following information for your Kubeflow Pipelines installation:
- API endpoint, e.g. `http://kubernetes-service.ibm.com/pipeline`
- Username for a multi-user, auth-enabled Kubeflow installation, e.g. `jdoe`
- Password for a multi-user, auth-enabled Kubeflow installation, e.g. `passw0rd`

Notebook pipelines use S3-compatible cloud storage at runtime to make data available to notebooks. Any kind of cloud storage should work (e.g. IBM Cloud Object Storage or Minio) as long as it can be accessed from your local machine and the Kubeflow Pipelines installation:
- S3 compatible object storage endpoint, e.g. `http://minio-service.kubeflow:9000`
- S3 object storage username, e.g. `minio`
- S3 object storage password, e.g. `minio123`

### Setup

This tutorial uses the `hello_world_kubeflow_pipelines` sample from the https://github.com/elyra-ai/examples GitHub repository.
1. Launch JupyterLab.
1. Open the _Git clone_ wizard (Git > Clone).

   ![Open Git clone wizard](doc/images/navigate_to_git_clone.png)

1. Enter `https://github.com/elyra-ai/examples.git` as _Clone URI_.
1. In the _File Browser_ navigate to `examples/pipelines/hello_world_kubeflow_pipelines`.

   ![Tutorial assets in File Browser](doc/images/cloned_examples.png)
   
   The cloned repository includes a set of notebooks that download an open [weather data set from the Data Asset Exchange](https://developer.ibm.com/exchanges/data/all/jfk-weather-data/), cleanse the data, analyze the data, and perform time-series predictions. In this tutorial you create a pipeline that runs these notebooks in the appropriate order. 

You are ready to start the tutorial.

### Creating a notebook pipeline

1. Open the _Launcher_ (File > New Launcher) if it is not already open.

   ![Open pipeline editor](doc/images/open_pipeline_editor.png)

1. Open the _Pipeline Editor_ (Elyra > Pipeline Editor) to create a new untitled pipeline.

   ![New pipeline](doc/images/new_pipeline.png)

1. In the _File Browser_ pane, right click on the untitled pipeline and select &#x270E; _Rename_.

   ![Rename pipeline](doc/images/rename_pipeline.png)

1. Change the pipeline name to `hello_world_kubeflow_pipelines`.

Next, you'll add a notebook to the pipeline that downloads an open data set archive from public cloud storage.

### Adding a notebook to the pipeline

1. From the _File Browser_ pane drag the `load_data.ipynb` notebook onto the canvas.

   ![Add first notebook to pipeline](doc/images/add_first_node.png)

1. Right click on the `load_data` notebook node to customize its execution properties.

   ![Open notebook node properties](doc/images/open_node_properties.png)

   The execution properties define the runtime environment, input artifacts (file dependencies and environment variables), and output files.

   ![Notebook node configuration](doc/images/node_configuration.png)

1. Notebooks are executed in Docker containers. 
   ![Notebooks are executed in Docker containers](doc/images/execution_environment.png)

   When you configure a notebook node you identify the _runtime image_, which will be used to instantiate the container. You can choose from a set of pre-configured public images or [provide your own](https://elyra.readthedocs.io/en/latest/user_guide/runtime-image-conf.html). If you provide your own image Python 3 and `curl` must be pre-installed. In this tutorial you'll use the stock `Pandas` image to run this notebook and all other notebooks.

   ![Configure runtime image](doc/images/configure_runtime_image.png)

1. By default only the notebook is made available in the Docker container. If a notebook requires access to other files (like Python scripts) that are stored on your local machine you have to specify them as _file dependencies_. Files that have been declared as a dependency are uploaded to a cloud storage bucket together with the notebook and downloaded into the Docker image prior to notebook execution.

   ![Input dependencies are uploaded to a Cloud storage bucket](doc/images/input_dependencies.png)

   The `load_data` notebook does not have any file dependencies. Leave the input field empty.

   ![Configure input file dependencies](doc/images/configure_input_file_dependencies.png)

1. If a notebook references `environment variables` you can declare them, if required. The `load_data` notebook you have added to the pipeline uses environment variable `DATASET_URL` to determine the name and location of a compressed data set archive, which needs to be downloaded and extracted. Assign environment variable `DATASET_URL` the value `https://dax-cdn.cdn.appdomain.cloud/dax-noaa-weather-data-jfk-airport/1.1.4/noaa-weather-data-jfk-airport.tar.gz`, which is a time-series data set containing weather information.

   ![Configure environment variables](doc/images/configure_environment_variables.png)

1. Each notebook in a pipeline is executed in an isolated Docker container. These Docker containers do not have access to a shared local file system and persisted output artifacts (such as data files or trained model files) that a notebook might produce. To make output artifacts accessible to other notebooks you have to declare them as _output files_ in the node configuration of the notebook that produces them. Declared output artifacts are automatically uploaded to the pre-configured cloud object storage bucket after notebook processing has completed and can subsequently be accessed by other notebooks in the pipeline by referencing the declared name.

   ![Data exchange between notebooks in a pipeline via cloud storage](doc/images/data_flow.png)
    
   The `load_data` notebook produces a data file named `data/noaa-weather-data-jfk-airport/jfk_weather.csv`, which we'll declare to make it accessible to the other notebooks in this pipeline.

    ![Configure output files](doc/images/configure_output_files.png)

    > It is considered good pratice to specify paths that are relative to the notebook location.

1. Save the node configuration.

1. Select the `load_data` node and attach a comment to it.

   ![Add node comment](doc/images/add_comment.png)

   The comment is automatically associated with the node.

   ![Associated node comment](doc/images/associated_node_comment.png)

1. In the comment node enter a descriptive text, such as `Download the JFK Weather dataset archive and extract it`.

   ![Add node comment](doc/images/add_comment_text.png)

Next, you'll add a second notebook to the pipeline and connect it with the first notebook in such a way that it is executed _after_ the first notebook. This notebook cleans the data in  `data/noaa-weather-data-jfk-airport/jfk_weather.csv`, which the `load_data` notebook produced, and stores the data in another CSV file.

### Adding a second notebook to the pipeline

1. Drag the `Part 1 - Data Cleaning.ipynb` notebook from the File Browser onto the canvas.
1. Customize the node's execution properties as follows:
   - Runtime image: `Pandas`
   - Output files: `data/noaa-weather-data-jfk-airport/jfk_weather_cleaned.csv`
1. Attach a comment node to the `Part 1 - Data Cleaning` node and provide a description, such as `Clean the dataset`. 
1. Connect the _output port_ of the `load_data` node to the _input port_ of the `Part 1 - Data Cleaning` node to establish a depency between the two notebooks.

   ![Connect two notebook nodes](doc/images/connect_two_nodes.png)

1. Save the pipeline.

   ![Save pipeline](doc/images/save_wip_pipeline.png)

Before you can run a pipeline on Kubeflows Pipelines, you have to define a runtime environment configuration.

> You can run a pipeline locally right away using the default `run in-place locally` configuration, as illustrated in the [_Hello World_ tutorial](https://github.com/elyra-ai/examples/tree/master/pipelines/hello_world).

### Defining a runtime environment configuration

A runtime environment configuration in Elyra contains connectivity information for a Kubeflow Pipelines instance and S3-compatible cloud storage. In this tutorial you will use the UI to define the runtime environment configuration, but you can also use the CLI [as described in the documentation](https://elyra.readthedocs.io/en/latest/user_guide/runtime-conf.html).

1. From the sidebar on the left side (or the Pipeline editor tool bar) choose _Runtimes_ to open the runtime configuration pane.

   ![Open runtime configuration panel](doc/images/open_runtime_configuration_panel.png)

1. Click + to create a new configuration.

   ![Create runtime configuration](doc/images/create_runtime_configuration.png)

1. Enter a _Name_ and an optional _Description_ for the configuration.

1. Enter the connectivity information for your Kubeflows Pipelines instance and S3-compatible cloud storage. If access to your Kubeflows Pipelines instance is [secured using DEX](https://www.kubeflow.org/docs/started/k8s/kfctl-istio-dex/), provide the appropriate credentials.

   ![Configure Kubeflows Pipelines runtime](doc/images/configure_runtime_environment.png)

1. Save the runtime configuration.

   ![Saved Kubeflows Pipelines runtime configuration](doc/images/saved_runtime_configuration.png)

1. Expand the twistie in front of the configuration entry. The displayed links provide access to the configured Kubeflow Pipelines UI and the cloud strage UI.

   ![Review runtime configuration](doc/images/review_runtime_configuration.png)

### Running a notebook pipeline on Kubeflow Pipelines

1. Run the pipeline.

   ![Run pipeline](doc/images/run_pipeline.png)

1. Enter `hello_kubeflows_world_pipeline` as _Pipeline name_.

1. From the _Runtime configuration_ drop down select the runtime configuration you've just created.

   ![Configure pipeline run](doc/images/run_pipeline_remotely.png)

1. Start the pipeline run. The pipeline artifacts (notebooks and file input dependencies) are gathered, packaged, and uploaded to cloud storage. The pipeline is compiled and subsequently submitted to Kubeflow Pipelines for execution.

   ![Pipeline run submitted confirmation message](doc/images/run_submission_confirmation.png)

   The confirmation message contains two links:
    - _Run details_: provides access to the Kubeflow Pipelines UI where you monitor the pipeline execution progress.
    - _Object storage_: provides access to the object storage where you access the input artifacts and output artifacts.

### Monitoring a notebook pipeline run

1. Open the _Run Details_ link. The _Experiments_ panel is displayed, depicting the in-progress execution graph for the pipeline. Only nodes that are currently executing or have already executed are displayed.

   ![](doc/images/pipeline_graph_run_in_progress.png)

1. Select one of the displayed nodes. A side panel opens, displaying information about the pipeline.

1. Open the _Logs_ tab to access the notebook node execution log file.

   ![Monitor pipeline run progress](doc/images/review_node_execution_log.png)

1. Wait for the pipeline run to finish.

   ![Wait for pipeline run to finish](doc/images/pipeline_run_complete.png)

### Accessing the pipeline run outputs

Notebook pipelines that execute on Kubeflow Pipelines store the pipeline run outputs (completed notebooks and declared output files) in the cloud storage bucket you've configured in the runtime configuration.

1. Open the object storage link and, if required, log in. 

   ![open cloud storage page](doc/images/access_pipeline_run_results.png)

1. Navigate to the bucket you've specified in the runtime configuration to review the content.

   ![review run output artifacts](doc/images/inspect_object_storage_bucket_content.png)

   If pipeline execution completed successfully the bucket contains for each notebook node the following artifacts:
      - a `tar.gz` archive containing the input notebook and, if applicable, its declared file-dependencies
      - the completed notebook with it's populated output cells
      - HTML version of the completed notebook
      - if applicable, the declared output files 

   For example, for the `load_data` notebook the following artifacts should be present:

   - `load_data-<UUID>.tar.gz` (input artifacts)
   - `load_data.ipynb` (output artifact) 
   - `load_data.html` (output artifact) 
   - `data/noaa-weather-data-jfk-airport/jfk_weather.csv` (output artifact)


### Next steps

This concludes the _Hello World Kubeflow Pipelines_ tutorial. You've learned how to 
- create a notebook pipeline
- add a notebook and configure its execution properties
- connect notebooks to define the execution dependencies
- create a Kubeflow Pipelines runtime configuration
- run a notebook pipeline on Kubeflow Pipelines
- monitor the pipeline run progress in the Kubeflow Pipelines UI
- access the pipeline run output on cloud storage

If you'd like you can extend the pipeline by adding two more notebooks, which can be executed in parallel after notebook `Part 1 - Data Cleaning.ipynb` was processed:
 - `Part 2 - Data Analysis.ipynb`
 - `Part 3 - Time Series Forecasting.ipynb`

Each of the notebooks can run in the `Pandas` Docker image and doesn't have any input dependencies, doesn't require any environment variables and doesn't produce an additional output files.

 ![The completed tutorial pipeline](doc/images/completed_tutorial_pipeline.png)
