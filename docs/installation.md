# Installation, exploitation, structure

## Prérequis

| Élément | Minimum |
|---|---|
| Mémoire | 16 Go de RAM |
| Disque | 32 Go |
| Logiciels | Docker, Docker Compose, `make`, Git, Git LFS |

## Récupération du dépôt

```bash
git lfs install
git clone https://github.com/Ismael-IF/rakuten-mlops-project.git
cd rakuten-mlops-project
git checkout rakuten-final
cd MLops_Multiclass_Rakuten
```

`git lfs install` est nécessaire avant le clone : les modèles `.h5` et `.pkl` sont suivis
par Git LFS (voir `.gitattributes`). Déposez ensuite les CSV du challenge dans
`data/raw_csv/`, voir [donnees.md](donnees.md).

## Premier lancement

```bash
make init-airflow
make start
```

`make init-airflow` crée les dossiers `dags`, `logs` et `plugins`, écrit `AIRFLOW_UID`
dans `.env` et initialise la base de métadonnées Airflow ainsi que le compte
administrateur. `make start` construit les images et démarre l'ensemble des services.

Le premier build télécharge TensorFlow et les images de base : prévoir un temps d'attente
important. Les lancements suivants se font avec `make start` seul.

## Services

| Service | URL | Identifiants |
|---|---|---|
| MLflow | `http://localhost:5000` | aucun |
| JupyterLab | `http://localhost:8888` | token `cd4ml` |
| MinIO, console | `http://localhost:9001` | `mlflow_access` / `mlflow_secret` |
| MinIO, API S3 | `http://localhost:9000` | `mlflow_access` / `mlflow_secret` |
| Flower (Celery) | `http://localhost:5555` | aucun |
| Airflow | port non publié par défaut, voir ci-dessous | `airflow` / `airflow` |
| API FastAPI | `http://localhost:8000`, après le DAG de déploiement | JWT via `/token` |

PostgreSQL (Airflow et MLflow) et Redis ne sont pas publiés sur l'hôte : ils ne sont
joignables que depuis le réseau Docker.

### Publier le port de l'interface Airflow

Dans `docker-compose.yml`, le service `airflow-webserver` publie `9002:9002` et la ligne
`- "8082:8080"` est commentée. Pour atteindre l'interface depuis l'hôte, rétablir une
publication vers le port 8080 du conteneur :

```yaml
  airflow-webserver:
    ports:
      - "8082:8080"
```

L'interface est alors disponible sur `http://localhost:8082`.

## Premier cycle complet

1. Dans Airflow, activer puis déclencher `1_pipeline_entrainement_dag`.
2. Suivre le run dans MLflow et vérifier que le modèle `conv1D` est passé en stage
   `Production` dans le Model Registry.
3. Déclencher `2_deployment_pipeline_dag`.
4. Ouvrir `http://localhost:8000/docs`, créer un compte, demander un jeton, puis appeler
   une route de prédiction.

L'environnement se pilote depuis les conteneurs : les notebooks s'exécutent dans
JupyterLab et non dans un interpréteur local, afin de bénéficier du `PYTHONPATH` qui
expose `plugins/src` et des variables MLflow et S3 déjà configurées.

## Tests

```bash
export PYTHONPATH=$PYTHONPATH:$(pwd)/rakuten_api
pytest rakuten_api/tests/
```

`rakuten_api/tests/test_api.py` est pour l'instant un test de fumée destiné à valider la
chaîne d'intégration continue. Les trois images de test décrites dans [api.md](api.md)
couvrent l'authentification, les autorisations et les prédictions en conteneurs isolés.

## Arrêt et nettoyage

```bash
make stop                        # arrête la stack (docker compose down)
make restart                     # down puis up --build
make airflow-logs                # logs du webserver Airflow
make del-containers-and-images   # supprime conteneurs, images et volumes
```

`make del-containers-and-images` est destructif : il supprime tous les conteneurs, images
et volumes Docker de la machine, pas seulement ceux du projet.

## Intégration continue

| Workflow | Déclencheur | Contrôle |
|---|---|---|
| `ci_testing.yml` | push et pull request sur `main` | installe les dépendances de l'API et exécute `pytest rakuten_api/tests/` |
| `airflow_check.yml` | push touchant `dags/**` | charge le `DagBag` et échoue si un DAG contient une erreur d'import, ce qui empêche la mise en ligne d'un DAG cassé |
| `model_validation.yml` | push touchant `rakuten_api/app/models/trained_models/**` | vérifie que `final_model.pkl` est chargeable avec `joblib.load` |
| `docker_publish.yml` | push sur `main` touchant `app/**` | build de l'image et publication sur `ghcr.io/<owner>/<repo>/mon_api_rakuten:latest` |

Les limites actuelles de ces workflows sont listées dans [perimetre.md](perimetre.md).

## Versions

| Composant | Version |
|---|---|
| Airflow | image `apache/airflow:2.9.1`, CeleryExecutor |
| Redis | `redis:7.2-bookworm` |
| PostgreSQL | `postgres:13`, une instance pour Airflow, une pour MLflow |
| MinIO | `minio/minio`, bucket `data` |
| MLflow | image construite sur `python:3.9-slim` |
| JupyterLab | `jupyter/scipy-notebook:lab-3.3.2` |
| API | `python:3.9-slim`, `fastapi==0.79.0`, `uvicorn==0.18.2`, `tensorflow==2.9.1`, `mlflow==1.28.0` |
| MongoDB | `mongo:4.0.4` |

## Structure du dépôt

```
MLops_Multiclass_Rakuten/
├── Makefile                        init-airflow, start, stop, restart, nettoyage
├── docker-compose.yml              14 services
├── mlflow-init-script.sh           création du bucket S3 des artefacts
│
├── dags/
│   ├── 1_pipeline_entrainement_dag.py   préparation, entraînement, enregistrement
│   └── 2_deployment_pipeline_dag.py     build, récupération du modèle, déploiement
│
├── plugins/src/                    code ML importé par les DAGs
│   ├── config.py                   chemins centralisés (usage local et notebooks)
│   ├── data_preprocessing/         nettoyage de texte, mapping des classes, split
│   ├── model_training/             architecture Conv1D, boucle d'entraînement, run MLflow
│   ├── model_validation/           comparaison challenger / production, transition de stage
│   ├── model_inference/            chargement de modèle et prédictions
│   └── deploy_model/               contexte de build d'un endpoint de scoring
│
├── rakuten_api/                    application servie en production
│   ├── setup.sh                    build des 4 images Docker
│   ├── docker-compose.yml          API, MongoDB et conteneurs de test
│   ├── app/                        FastAPI : routers, prédictions, config, modèles
│   ├── authentication_image/       conteneur de test : authentification
│   ├── authorization_image/        conteneur de test : autorisations
│   ├── prediction_image/           conteneur de test : prédictions, avec images d'exemple
│   └── tests/
│
├── dockerfiles/                    images Airflow, MLflow et Jupyter
├── notebooks/                      exploration, à exécuter depuis JupyterLab
├── data/                           monté sur /data dans les conteneurs, hors dépôt
└── .github/workflows/              4 workflows d'intégration continue
```
