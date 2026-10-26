# Périmètre actuel et pistes d'amélioration

État réel du dépôt, pour lever toute ambiguïté sur ce qui tourne de bout en bout et ce
qui reste à faire.

## Ce qui fonctionne de bout en bout

* La préparation des données : chargement des CSV, nettoyage du texte, encodage des 27
  classes, split stratifié, écriture des fichiers dans `/data/processed`.
* L'entraînement du Conv1D texte, avec poids de classes équilibrés et early stopping.
* Le suivi du run dans MLflow : hyperparamètres, métriques de chaque epoch, historique en
  artefact, modèle sérialisé.
* La promotion dans le Model Registry : archivage de l'ancienne version, enregistrement
  et passage en stage `Production`.
* La récupération du modèle en production, le build des images et le déploiement de l'API
  avec vérification de disponibilité bloquante.
* L'authentification JWT, la gestion des utilisateurs et la prédiction à partir du texte
  avec le Conv1D, dont le modèle `conv1d_text_model.h5` est versionné dans le dépôt.

## Limites connues

### Modèles absents du dépôt

`rakuten_api/app/config/inputs.py` attend `Model_Texte_SimpleDNN.hdf5`,
`Model_Images_Xception.hdf5` et `Model_Images_InceptionV3.hdf5` dans
`app/models/trained_models/`. Seuls `conv1d_text_model.h5` et `final_model.pkl` y sont
présents : les routes Simple DNN, image et bimodales échouent au chargement du modèle
tant que ces fichiers ne sont pas fournis.

Les modèles image pèsent plusieurs centaines de méga-octets, d'où leur absence du dépôt.
La suite logique est un stockage externe : artefacts MinIO, release GitHub ou DVC, avec
téléchargement au démarrage du conteneur.

### Entraînement limité au texte

Le DAG n'entraîne que le Conv1D. Les modèles image et bimodaux proviennent de la phase de
modélisation et ne sont pas réentraînés par la chaîne. Étendre le pipeline aux images
suppose d'ajouter la préparation des images (redimensionnement, augmentation) et des
tâches d'entraînement dédiées.

### Validation non branchée

`validate_model.py` existe mais n'est pas utilisé comme tâche de branchement entre
l'entraînement et la promotion : le modèle est promu sans comparaison avec la production.
Le brancher suppose un `BranchPythonOperator` entre `model_training` et `push_new_model`.

### Pas d'évaluation sur jeu de test

Le split produit un ensemble de validation utilisé par l'early stopping. Le `X_test` du
challenge n'étant pas labellisé, aucune métrique de généralisation n'est journalisée
automatiquement. Un jeu de test tenu à l'écart du split serait nécessaire pour alimenter
le garde-fou F1 de `validate_model.py`.

### Enchaînement des deux DAGs

Le `TriggerDagRunOperator` reliant l'entraînement au déploiement est écrit mais commenté
dans `1_pipeline_entrainement_dag.py`.

### Branche par défaut et workflows

Le travail d'industrialisation est sur `rakuten-final`, alors que `ci_testing.yml` et
`docker_publish.yml` ciblent `main` : ces deux workflows ne se déclenchent pas en l'état.

`docker_publish.yml` surveille par ailleurs `app/**` et construit depuis la racine du
dépôt, alors que le Dockerfile de l'API se trouve dans `rakuten_api/app/`.

### Interface Airflow non publiée

La publication du port de l'interface Airflow est commentée dans `docker-compose.yml`,
voir [installation.md](installation.md).

### Sérialisation du modèle

`push_model.py` enregistre un modèle Keras via `mlflow.sklearn.log_model`, ce qui
fonctionne par sérialisation pickle mais n'utilise pas la saveur `mlflow.tensorflow`,
plus adaptée : signature du modèle, exemple d'entrée, rechargement natif.

### Couverture de tests

Les tests unitaires de l'API restent à écrire : route `/token`, contrôle des rôles,
format des réponses de prédiction, validation des entrées. Le test actuel valide la
chaîne d'intégration continue, pas le comportement de l'application.

### Pas de supervision en production

Aucun suivi de dérive des données ou des performances, ni métriques applicatives
exposées. Un export Prometheus sur l'API et un DAG de contrôle périodique des
distributions d'entrée seraient les premières briques.

### Secrets en clair

Les identifiants de développement figurent dans `docker-compose.yml`. Un déploiement réel
suppose des secrets Docker ou GitHub Actions et un `.env` non versionné.
