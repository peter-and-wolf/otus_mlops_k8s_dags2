import os
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd

import s3fs
import mlflow

from evidently import ColumnMapping
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago


def hello_world():  
  aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID']
  aws_access_secret_key = os.environ['AWS_SECRET_ACCESS_KEY']
  s3_endpoint_url = os.environ['MLFLOW_S3_ENDPOINT_URL']
  drifter_url = os.environ['DRIFTER_URL'] 
  reference_df_path = os.environ['REFERENCE_DF_PATH']

  print(aws_access_key_id) 
  print(aws_access_secret_key) 
  print(s3_endpoint_url)
  print(drifter_url)
  print(reference_df_path)

  s3 = s3fs.S3FileSystem(
    key=aws_access_key_id,
    secret=aws_access_secret_key,
    endpoint_url=s3_endpoint_url
  )

  reference_df = pd.read_csv(
    s3.open(reference_df_path)
  )
  print('REFERENCE')
  print(reference_df.head())

  current_df = pd.read_csv(drifter_url)
  print('CURRENT')
  print(current_df.head())

  column_mapping = ColumnMapping()
  column_mapping.numerical_features = list(reference_df.columns)

  data_drift = Report(metrics = [DataDriftPreset()])
  data_drift.run(
    current_data = current_df,
    reference_data = reference_df,
    column_mapping=column_mapping
  )

  report = data_drift.as_dict()

  with tempfile.TemporaryDirectory() as tmp_dir:
    path = Path(tmp_dir, 'test-evidently.csv')
    reference_df.to_csv(path, index=False)
    
    with mlflow.start_run() as run:
      mlflow.log_artifact(path)
      mlflow.log_param('dataset_drift', report['metrics'][1]['result']['dataset_drift'])
      mlflow.log_metrics({
        'number_of_drifted_columns': report['metrics'][1]['result']['number_of_drifted_columns'],
        'share_of_drifted_columns': report['metrics'][1]['result']['share_of_drifted_columns'],
      })
      for feature in column_mapping.numerical_features:
        mlflow.log_metric(feature, report["metrics"][1]["result"]["drift_by_columns"][feature]["drift_score"])


with DAG(dag_id="hello_world_dag",
         start_date=days_ago(2),
         schedule="*/5 * * * *",
         catchup=False) as dag:
      
  task = PythonOperator(
    task_id="hello_world",
    python_callable=hello_world,
  )
  task