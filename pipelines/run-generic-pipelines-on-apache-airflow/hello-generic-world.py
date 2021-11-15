from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from airflow import DAG
from airflow.utils.dates import days_ago


args = {
    "project_id": "hello-generic-world-1011144224",
}

dag = DAG(
    "hello-generic-world-1011144224",
    default_args=args,
    schedule_interval="@once",
    start_date=days_ago(1),
    description="A generic pipeline tutorial",
    is_paused_upon_creation=False,
)


# Operator source: examples/pipelines/run-generic-pipelines-on-apache-airflow/load_data.ipynb
op_bb889c69_b23a_484e_8fb3_e69309f38a98 = KubernetesPodOperator(
    name="Load_weather_data",
    namespace="default",
    image="docker.io/amancevice/pandas:1.1.1",
    cmds=["sh", "-c"],
    arguments=[
        "mkdir -p ./jupyter-work-dir/ && cd ./jupyter-work-dir/ && curl -H 'Cache-Control: no-cache' -L https://raw.githubusercontent.com/elyra-ai/elyra/v3.2.0rc2/elyra/airflow/bootstrapper.py --output bootstrapper.py && curl -H 'Cache-Control: no-cache' -L https://raw.githubusercontent.com/elyra-ai/elyra/v3.2.0rc2/etc/generic/requirements-elyra.txt --output requirements-elyra.txt && python3 -m pip install packaging && python3 -m pip freeze > requirements-current.txt && python3 bootstrapper.py --cos-endpoint http://cloning1.fyre.ibm.com:30205 --cos-bucket kstokes --cos-directory 'hello-generic-world-1011144224' --cos-dependencies-archive 'load_data-bb889c69-b23a-484e-8fb3-e69309f38a98.tar.gz' --file 'examples/pipelines/run-generic-pipelines-on-apache-airflow/load_data.ipynb' --outputs 'data/noaa-weather-data-jfk-airport/jfk_weather.csv' "
    ],
    task_id="Load_weather_data",
    env_vars={
        "DATASET_URL": "https://dax-cdn.cdn.appdomain.cloud/dax-noaa-weather-data-jfk-airport/1.1.4/noaa-weather-data-jfk-airport.tar.gz",
        "ELYRA_RUNTIME_ENV": "airflow",
        "AWS_ACCESS_KEY_ID": "minio",
        "AWS_SECRET_ACCESS_KEY": "minio123",
        "ELYRA_ENABLE_PIPELINE_INFO": "True",
        "ELYRA_RUN_NAME": "hello-generic-world-1011144224-{{ ts_nodash }}",
    },
    in_cluster=True,
    config_file="None",
    dag=dag,
)


# Operator source: examples/pipelines/run-generic-pipelines-on-apache-airflow/Part 1 - Data Cleaning.ipynb
op_8c96e288_4461_4d7e_8e0d_353c1fdb0c8c = KubernetesPodOperator(
    name="Part_1___Data_Cleaning",
    namespace="default",
    image="docker.io/amancevice/pandas:1.1.1",
    cmds=["sh", "-c"],
    arguments=[
        "mkdir -p ./jupyter-work-dir/ && cd ./jupyter-work-dir/ && curl -H 'Cache-Control: no-cache' -L https://raw.githubusercontent.com/elyra-ai/elyra/v3.2.0rc2/elyra/airflow/bootstrapper.py --output bootstrapper.py && curl -H 'Cache-Control: no-cache' -L https://raw.githubusercontent.com/elyra-ai/elyra/v3.2.0rc2/etc/generic/requirements-elyra.txt --output requirements-elyra.txt && python3 -m pip install packaging && python3 -m pip freeze > requirements-current.txt && python3 bootstrapper.py --cos-endpoint http://cloning1.fyre.ibm.com:30205 --cos-bucket kstokes --cos-directory 'hello-generic-world-1011144224' --cos-dependencies-archive 'Part 1 - Data Cleaning-8c96e288-4461-4d7e-8e0d-353c1fdb0c8c.tar.gz' --file 'examples/pipelines/run-generic-pipelines-on-apache-airflow/Part 1 - Data Cleaning.ipynb' --inputs 'data/noaa-weather-data-jfk-airport/jfk_weather.csv' --outputs 'data/noaa-weather-data-jfk-airport/jfk_weather_cleaned.csv' "
    ],
    task_id="Part_1___Data_Cleaning",
    env_vars={
        "ELYRA_RUNTIME_ENV": "airflow",
        "AWS_ACCESS_KEY_ID": "minio",
        "AWS_SECRET_ACCESS_KEY": "minio123",
        "ELYRA_ENABLE_PIPELINE_INFO": "True",
        "ELYRA_RUN_NAME": "hello-generic-world-1011144224-{{ ts_nodash }}",
    },
    in_cluster=True,
    config_file="None",
    dag=dag,
)

op_8c96e288_4461_4d7e_8e0d_353c1fdb0c8c << op_bb889c69_b23a_484e_8fb3_e69309f38a98


# Operator source: examples/pipelines/run-generic-pipelines-on-apache-airflow/Part 2 - Data Analysis.ipynb
op_dcf486ef_2d73_4306_a3ca_af720a1f8eb3 = KubernetesPodOperator(
    name="Part_2___Data_Analysis",
    namespace="default",
    image="docker.io/amancevice/pandas:1.1.1",
    cmds=["sh", "-c"],
    arguments=[
        "mkdir -p ./jupyter-work-dir/ && cd ./jupyter-work-dir/ && curl -H 'Cache-Control: no-cache' -L https://raw.githubusercontent.com/elyra-ai/elyra/v3.2.0rc2/elyra/airflow/bootstrapper.py --output bootstrapper.py && curl -H 'Cache-Control: no-cache' -L https://raw.githubusercontent.com/elyra-ai/elyra/v3.2.0rc2/etc/generic/requirements-elyra.txt --output requirements-elyra.txt && python3 -m pip install packaging && python3 -m pip freeze > requirements-current.txt && python3 bootstrapper.py --cos-endpoint http://cloning1.fyre.ibm.com:30205 --cos-bucket kstokes --cos-directory 'hello-generic-world-1011144224' --cos-dependencies-archive 'Part 2 - Data Analysis-dcf486ef-2d73-4306-a3ca-af720a1f8eb3.tar.gz' --file 'examples/pipelines/run-generic-pipelines-on-apache-airflow/Part 2 - Data Analysis.ipynb' --inputs 'data/noaa-weather-data-jfk-airport/jfk_weather_cleaned.csv;data/noaa-weather-data-jfk-airport/jfk_weather.csv' "
    ],
    task_id="Part_2___Data_Analysis",
    env_vars={
        "ELYRA_RUNTIME_ENV": "airflow",
        "AWS_ACCESS_KEY_ID": "minio",
        "AWS_SECRET_ACCESS_KEY": "minio123",
        "ELYRA_ENABLE_PIPELINE_INFO": "True",
        "ELYRA_RUN_NAME": "hello-generic-world-1011144224-{{ ts_nodash }}",
    },
    in_cluster=True,
    config_file="None",
    dag=dag,
)

op_dcf486ef_2d73_4306_a3ca_af720a1f8eb3 << op_8c96e288_4461_4d7e_8e0d_353c1fdb0c8c


# Operator source: examples/pipelines/run-generic-pipelines-on-apache-airflow/Part 3 - Time Series Forecasting.ipynb
op_1e4b1763_337e_4f84_ae9c_a6cc79a1b7eb = KubernetesPodOperator(
    name="Part_3___Time_Series_Forecasting",
    namespace="default",
    image="docker.io/amancevice/pandas:1.1.1",
    cmds=["sh", "-c"],
    arguments=[
        "mkdir -p ./jupyter-work-dir/ && cd ./jupyter-work-dir/ && curl -H 'Cache-Control: no-cache' -L https://raw.githubusercontent.com/elyra-ai/elyra/v3.2.0rc2/elyra/airflow/bootstrapper.py --output bootstrapper.py && curl -H 'Cache-Control: no-cache' -L https://raw.githubusercontent.com/elyra-ai/elyra/v3.2.0rc2/etc/generic/requirements-elyra.txt --output requirements-elyra.txt && python3 -m pip install packaging && python3 -m pip freeze > requirements-current.txt && python3 bootstrapper.py --cos-endpoint http://cloning1.fyre.ibm.com:30205 --cos-bucket kstokes --cos-directory 'hello-generic-world-1011144224' --cos-dependencies-archive 'Part 3 - Time Series Forecasting-1e4b1763-337e-4f84-ae9c-a6cc79a1b7eb.tar.gz' --file 'examples/pipelines/run-generic-pipelines-on-apache-airflow/Part 3 - Time Series Forecasting.ipynb' --inputs 'data/noaa-weather-data-jfk-airport/jfk_weather_cleaned.csv;data/noaa-weather-data-jfk-airport/jfk_weather.csv' "
    ],
    task_id="Part_3___Time_Series_Forecasting",
    env_vars={
        "ELYRA_RUNTIME_ENV": "airflow",
        "AWS_ACCESS_KEY_ID": "minio",
        "AWS_SECRET_ACCESS_KEY": "minio123",
        "ELYRA_ENABLE_PIPELINE_INFO": "True",
        "ELYRA_RUN_NAME": "hello-generic-world-1011144224-{{ ts_nodash }}",
    },
    in_cluster=True,
    config_file="None",
    dag=dag,
)

op_1e4b1763_337e_4f84_ae9c_a6cc79a1b7eb << op_8c96e288_4461_4d7e_8e0d_353c1fdb0c8c
