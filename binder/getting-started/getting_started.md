<!--
{% comment %}
Copyright 2018-2020 IBM Corporation

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
# Elyra quickstart

This short interactive quickstart provides an introduction to Elyra - aset of AI centric extensions for JupyterLab. Note that this tour does not include features requiring software that is not bundled with Elyra or JupyterLab, such as Kubeflow Pipelines.

A complete list of features can be found in [the documentation](https://elyra.readthedocs.io/en/latest/getting_started/overview.html).

An easy way to determine whether Elyra is installed in your JupyterLab is to look for the logo.

  ![Elyra extensions](images/elyra.png)

## Git integration

Elyra includes the [Git extension](https://github.com/jupyterlab/jupyterlab-git) to allow for easy sharing and versioning of notebooks, Python scripts and other artifacts in your work directory.

1. From the JupyterLab main menu select `Git` > `Clone a Repository`.
1. Enter `https://github.com/elyra-ai/examples.git` as repository URL to clone the Elyra examples.
1. From the sidebar on the left hand side open the "File Browser" tab.
1. Navigate to the cloned `examples` directory.
1. From the sidebar select the "Git" tab. 

   ![Git interface](images/git-interface.png)

   When you add, modify, or remove files the status is reflected in this view. You can compare file versions, stage, unstage, or commit changes, access the commit history and much more.

## AI Pipelines

Elyra provides a Visual Pipeline Editor, which you can use to create AI workflows from Jupyter notebooks and Python scripts and run them in your local environment or on Kubeflow Pipelines, a platform for building and deploying portable and scalable machine learning workflows.

Local execution is primarily suitable during development or for workflows that process rather small data volumes or don't require special purpose hardware to complete processing in a reasonable amount of time.

![Pipeline editor](images/pipeline-in-editor.png)

The https://github.com/elyra-ai/examples.git repository contains two tutorials that guide you through the process of creating and running your first pipeline, which downloads a time series weather data set, cleanses it, performs analysis and explores approaches to predicting future temperatures.

1. Follow the instructions in section _[Git integration](#git-integration)_ to clone the repository.
1. In the File Browser navigate to `examples/pipelines/hello_world` to try out the local execution. The Elyra getting started deployment on mybinder does not include a Kubeflow Pipelines deployment. If you have access to a Kubeflow Pipelines deployment navigate to `examples/pipelines/hello_world_kubeflow_pipelines`. 

1. Open `README.md` and complete the steps.

## Enhanced Notebook Support

### Run notebooks interactively in remote environments

The Elyra extension supports interactive notebook execution in remote environments, enabling you to take advantage of environments with special purpose hardware, such as GPUs and TPUs. This feature requires the [Jupyter Enterprise Gateway](https://jupyter-enterprise-gateway.readthedocs.io/en/latest/).

1. Open the "File Browser" tab on the left hand side.
1. Open a notebook (`.ipynb`). The currently selected kernel is displayed next to the kernel state indicator, which depicts a circle if the kernel is idle.
1. Click on the kernel name to choose a different one. If the only available options are local kernels, such as `python3`, your JupyterLab is not connected to an Enterprise Gateway.

   ![Select kernel](images/notebook_switch_kernel.png)

Note that if your JupyterLab is connected to an Enterprise Gateway only remote kernels can be used.   

### Run notebooks as batch jobs in remote environments

You can run a notebook as a batch job in remote environments. This feature requires access to [Kubeflow Pipelines](https://www.kubeflow.org/docs/pipelines/overview/pipelines-overview/).

1. Open the "File Browser" tab on the left hand side.
1. Open a notebook (`.ipynb`).
1. Click "Submit notebook ..." and select a kubeflow pipeline configuration. If no [Kubeflow pipelines runtime is configured in your JupyterLab](https://elyra.readthedocs.io/en/latest/user_guide/runtime-conf.html) an error is raised.

   ![Run notebook as batch](images/notebook_batch.png)

## Table of Contents

In JupyterLab you can view a dynamically generated table of contents for notebooks and markdown files, making it easier to navigate through large files. Elyra will soon add similar functionality for Python scripts.

1. Open the "File Browser" tab on the left hand side.
1. Open a notebook (`.ipynb`) or markdown (`.md`) file.
1. Select the "Table of Contents" tab on the left hand side. Click on a heading to navigate to the corresponding location in the file.

   ![Table of contents](images/toc_notebook.png)

   The Table of Contents functionality depends on the open file type. For example, you can hide (or unhide) code cells in notebooks by clicking on the twistie. 

## Python Editor

Elyra adds a basic Python script editor, which supports running in a local kernel or a remote kernel for offloading of compute intensive tasks. Remote execution requires a [Jupyter Enterprise Gateway](https://jupyter-enterprise-gateway.readthedocs.io/en/latest/). 

1. Open the "File Browser" tab on the left hand side.
1. Open a Python script or create a new script ("File" > "New" > "Python File")
1. Select a kernel from the drop down and click "Run" to execute the script.

   ![Python Editor](images/python_editor.png)

## Code Snippets

Elyra introduces a re-usable code snippets feature, which enables you to define and insert custom pieces of code. 

### Creating code snippets

1. Select the "Code Snippets" tab on the left hand side. 
1. Click the + sign to create a new snippet. 

   ![Create code snippet](images/create_code_snippet.png)

1. Enter a snippet name, choose from the list of predefined languages (or enter a custom language value) and provide the desired source code. 

   ![Define code snippet](images/define_code_snippet.png)

For illustrative purposes this getting started tour includes two pre-defined code snippets - one for Python and one for markdown.   

### Copy and insert code snippets

You can copy code snippets to the clipboard or insert them in JupyterLab widgets, such as the notebook editor, that support the snippet's language.

![Copy and paste code snippet](images/consume_code_snippet.png)

To insert a Python or markdown snippet into a Python notebook cell:
1. Open the "File Browser" tab on the left hand side. 
1. Open the `getting_started.ipynb` notebook.
1. Scroll to the bottom.
1. Position the cursor in the _code_ cell that reads `# TODO: insert ...`.
1. Select the "Code Snippets" tab on the left hand side.
1. Try to insert the markdown snippet. A warning should be displayed indicating that the snippet is not compatible with the cell's type. Do not insert the snippet.
1. Insert the Python snippet into the code cell.

   ![Code Snippet](images/insert_code_snippet.png)

### Deleting code snippets

To delete a code snippet definition 

1. Select the "Code Snippets" tab on the left hand side.
1. Click the trash can icon. 

   ![Delete code snippet](images/delete_code_snippet.png)
