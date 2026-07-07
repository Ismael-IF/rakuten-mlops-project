from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.exceptions import AirflowException
from datetime import datetime, timedelta
import os
import mlflow
from mlflow.tracking import MlflowClient
import shutil

# --- CONFIGURATION MISE À JOUR ---
PROJECT_DIR = "/opt/airflow/rakuten_api" # Chemin interne défini dans le volume
SHARED_DATA_DIR = "/data"                # Dossier monté pour le transfert
MODEL_NAME = "conv1D"                    # Nom identique au CI Pipeline
DEST_PATH = "/opt/airflow/rakuten_api/app/models/trained_models/final_model.pkl"

default_args = {
    "owner": "IsmaelF",
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
}

def transfer_model_from_mlflow():
    """Récupère le modèle Production de MLflow vers /data"""
    client = MlflowClient()
    try:
        # 1. Identifier la version en Production
        versions = client.get_latest_versions(MODEL_NAME, stages=["Production"])
        if not versions:
            raise AirflowException(f"Aucune version 'Production' pour {MODEL_NAME}")
        
        run_id = versions[0].run_id
        print(f"Version {versions[0].version} détectée (Run: {run_id}).")

        # 2. On utilise "production_model" comme défini dans push_model.py
        # On télécharge dans un dossier temporaire pour ne pas polluer /data directement
        local_path = client.download_artifacts(run_id, "production_model", SHARED_DATA_DIR)
        print(f"Artefacts téléchargés dans : {local_path}")

        # 3. MODIFICATION ICI : On cherche le fichier .pkl de manière flexible
        found = False
        for root, dirs, files in os.walk(local_path):
            for file in files:
                if file.endswith(".pkl"):
                    source_file = os.path.join(root, file)
                    shutil.copy2(source_file, DEST_PATH) # Copie vers /data/final_model.pkl
                    print(f"Modèle déplacé avec succès : {source_file} -> {DEST_PATH}")
                    found = True
                    break
        
        if not found:
            raise AirflowException(f"Aucun fichier .pkl trouvé dans {local_path}")

    except Exception as e:
        print(f"Erreur lors du transfert : {str(e)}")
        raise AirflowException(e)

with DAG(
    dag_id="2_deployment_pipeline_dag",
    default_args=default_args,
    schedule_interval=None,
    start_date=datetime(2023, 1, 1),
    catchup=False,
    tags=["rakuten", "cd"],
) as dag:

    # 1. Build des images
    build_images = BashOperator(
        task_id="build_rakuten_images",
        bash_command="cd /opt/airflow/rakuten_api && chmod +x setup.sh && ./setup.sh ",
    )

    # 2. Récupération du modèle
    fetch_model = PythonOperator(
        task_id="fetch_production_model",
        python_callable=transfer_model_from_mlflow,
    )

    # 3. Lancement de l'API (Docker Run)
    deploy_api = BashOperator(
        task_id="deploy_rakuten_api",
        bash_command="""
            # On récupère l'ID du réseau qui contient 'default' (pas d'accolades, pas de conflit)
            NETWORK_ID=$(docker network ls --filter name=default -q | head -n 1)
            
            # Si NETWORK_ID est vide, on utilise 'bridge' par défaut
            NETWORK=${NETWORK_ID:-bridge}
            echo "Utilisation du réseau ID : $NETWORK"

            docker rm -f rakuten-mongo rakuten-api fastApi_rakuten >/dev/null 2>&1 || true
            
            # Lancement de MongoDB
            docker run -d --name rakuten-mongo --network $NETWORK -p 27018:27017 mongo:4.0.4
            
           docker run -d --name fastApi_rakuten \
                --network $NETWORK \
                -p 8000:8000 \
                -v /data:/home/data \
                -e MLFLOW_TRACKING_URI='http://mlflow-webserver:5000' \
                -e AWS_ACCESS_KEY_ID='mlflow_access' \
                -e AWS_SECRET_ACCESS_KEY='mlflow_secret' \
                -e MLFLOW_S3_ENDPOINT_URL='http://s3-artifact-storage:9000' \
                -e DB_URL='mongodb://rakuten-mongo:27017/rakuten_users_db' \
                mon_api_rakuten:latest

            echo "Attente du chargement du modèle TensorFlow (30s)..."
            sleep 30

            # Vérification sur le nom du conteneur (pas localhost)
            if curl -s --retry 3 --retry-delay 5 http://fastApi_rakuten:8000/docs > /dev/null; then
                echo "✅ API déployée et accessible sur le réseau Docker !"
            else
                echo "❌ L'API ne répond pas. Voici les logs d'erreur :"
                docker logs fastApi_rakuten | tail -n 20
                exit 1  # Forcer l'échec de la tâche Airflow
            fi
                    """,
    )

    build_images >> fetch_model >> deploy_api