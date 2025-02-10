import os
import uuid
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



def hello_world(filekey: str):
  
  aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID']
  aws_access_secret_key = os.environ['AWS_SECRET_ACCESS_KEY']
  print(aws_access_key_id, aws_access_secret_key)

  current_ds = pd.read_csv('http://localhost:9999/api/v1/data')
  print(current_ds.head())


 

with DAG(dag_id="hello_world_dag",
         start_date=days_ago(2),
         schedule="*/5 * * * *",
         catchup=False) as dag:
      
  filekey = str(uuid.uuid4())

  #joke_endpoint = os.environ.get('JOKE_API_ENDPOINT')
  #if joke_endpoint is None:
  #  raise ValueError('env JOKE_API_ENDPOINT must be set!')
  
  #s3_endpoint = os.environ.get('S3_ENDPOINT')
  #if s3_endpoint is None:
  #  raise ValueError('env S3_ENDPOINT must be set!')
  
  #s3_bucket = os.environ.get('S3_BUCKET')
  #if s3_bucket is None:
  #  raise ValueError('env S3_BUCKET must be set!')
  
  #joke_to_s3_image = os.environ.get('JOKE_TO_S3_IMAGE')
  #if joke_to_s3_image is None:
  #  raise ValueError('env JOKE_TO_S3_IMAGE must be set!')
  

  #task1 = KubernetesPodOperator (
  #  task_id='joke-to-s3',
  #  name='joke-to-s3',
  #  namespace='default',
  #  image=joke_to_s3_image,
  #  cmds = [
  #    'python', 'main.py', 
  #    '--joke-endpoint', joke_endpoint,
  #    '--s3-endpoint', s3_endpoint,
  #    '--bucket', s3_bucket,
  #    '--filekey', f'jokes/{filekey}'
  #  ],
  #  secrets=[aws_access_key_id, aws_secret_access_key],
  #  in_cluster=True
  #)

  task = PythonOperator(
    task_id="hello_world",
    python_callable=hello_world,
    op_kwargs=dict(
      filekey=f'jokes/{filekey}'
    )
  )
  task