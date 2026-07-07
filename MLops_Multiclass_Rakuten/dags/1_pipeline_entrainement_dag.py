import os
from datetime import timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.utils.dates import days_ago

# Imports de vos scripts personnalisés
from src.data_preprocessing import data_prepped
from src.model_training import train_model
from src.model_validation import push_model

# --- CONFIGURATION HARMONISÉE ---
# Ce nom doit être IDENTIQUE dans le DAG de déploiement
_model_name = "conv1D" 
_mlflow_experiment_name = "Rakuten"

# Chemins internes au conteneur (assurez-vous que le volume ./data:/data est dans le compose)
_raw_data_dir = '/data/raw_csv'
_data_dir = "/data/processed"

_data_files = {
    'raw_Y_train_file': os.path.join(_raw_data_dir, 'Y_train_CVw08PX.csv'),
    'raw_X_train_file': os.path.join(_raw_data_dir, 'X_train_update.csv'),
    'raw_X_test_file': os.path.join(_raw_data_dir, 'X_test_update.csv'),
    'X_train_split_file' : os.path.join(_data_dir, 'X_train_split.csv'),
    'X_val_split_file' : os.path.join(_data_dir, 'X_val_split.csv'),
    'X_test_file' : os.path.join(_data_dir, 'X_test.csv')
}

default_args = {
    'owner': 'IsmaelF',
    'depends_on_past': False,
    'start_date': days_ago(0),
    'retries': 1,
    'retry_delay': timedelta(seconds=10)
}

# --- DÉFINITION DU DAG ---
with DAG(
    '1_pipeline_entrainement_dag',
    default_args=default_args,
    description='Continuous Integration Pipeline - Training & Registry',
    schedule_interval=None, # Manuel ou déclenché par un changement de code
    catchup=False,
    tags=['rakuten', 'train']
) as dag:

    # 1. Préparation des données
    data_ingestion = PythonOperator(
        task_id='model_data_prepped',
        python_callable=data_prepped,
        op_kwargs={
            'input_folder': _raw_data_dir,
            'output_folder': _data_dir 
        }
    )

    # 2. Entraînement du modèle (Log dans MLflow)
    model_training = PythonOperator(
        task_id='model_training',
        python_callable=train_model,
        op_kwargs={
            'data_files': _data_files,
            'experiment_name': _mlflow_experiment_name
        }
    )

    # 3. Passage du modèle en stage "Production" dans le Registry MLflow
    push_to_production = PythonOperator(
        task_id='push_new_model',
        python_callable=push_model,
        op_kwargs={
            'model': _model_name # Transmet "conv1D"
        }
    )

    # 4. DÉCLENCHEMENT AUTOMATIQUE DU DÉPLOIEMENT
    """trigger_deployment = TriggerDagRunOperator(
        task_id='trigger_deployment_pipeline',
        trigger_dag_id='2_deployment_pipeline_dag', # ID exact du second DAG
        wait_for_completion=False
    )"""

    # --- FLUX DE TRAVAIL ---
    data_ingestion >> model_training >> push_to_production 
    #>> trigger_deployment