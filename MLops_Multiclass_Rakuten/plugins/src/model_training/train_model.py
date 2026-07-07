# Description: Use this script to train a new ML model from scratch. The algorithm
#              is defined in 'get_model'. The trained model will be tracked in
#              MLflow and is available for further steps in the pipeline via model 
#              uri
# ================================================================================

import os
import mlflow
import mlflow.sklearn
import mlflow.tensorflow
import numpy as np
from sklearn.utils.class_weight import compute_class_weight
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from src.model_training.text_model_builder import create_model
from src.model_training.text_models_training import train_model_and_save
import time
import pandas as pd
import pickle
import tempfile
import logging
import json

logger = logging.getLogger(__name__)


def _check_keys(dict_, required_keys):
    """checks if a dict contains all expected keys"""
    for key in required_keys:
        if key not in dict_:
            raise ValueError(f'input argument "data_files" is missing required key "{key}"')


def get_model():

    # Create a Conv1D model via text_model_builder
    model = create_model()
    
    return model
    

def train_model(data_files, experiment_name="Rakuten", **kwargs):
    """
    Loads x_train.csv and y_train.csv from data_dir, trains a model and tracks
    it with MLflow

    Args:
        data_files (dict): contains the following keys:
          'transformed_x_train_file': location of the training input data
          'transformed_y_train_file': location of the training data labels
        experiment_name (str): name of the MLflow experiment
    """
    required_keys = [
        'X_train_split_file' ,
        'X_val_split_file' ,
        'X_test_file',
    ]
     
    #_check_keys(data_files, required_keys)
    
    start = time.time()
        
    mlflow.set_experiment(experiment_name)
    
    X_train = pd.read_csv(data_files['X_train_split_file'])
    X_val = pd.read_csv(data_files['X_val_split_file'])
    X_test = pd.read_csv(data_files['X_test_file'])
    
    y_train = X_train['prdtypecode_encoded'].values
    y_val = X_val['prdtypecode_encoded'].values
    
    class_labels = np.unique(X_train["prdtypecode_encoded"])
    class_counts = {label: np.sum(X_train["prdtypecode_encoded"] == label) for label in class_labels}

    # Compute class weights based on distribution
    class_weights = compute_class_weight('balanced', classes=class_labels, y=X_train["prdtypecode_encoded"])
    class_weight_dict = {class_labels[i]: class_weights[i] for i in range(len(class_labels))}
    class_weight_dict = {int(key): value for key, value in class_weight_dict.items()}
    

    # Extract text data
    train_text = X_train["text"].astype(str)
    val_text = X_val["text"].astype(str)
    test_text = X_test["text"].astype(str)

    # Define hyperparameters
    MAX_VOCAB_SIZE = 20000  # Maximum number of words in the vocabulary
    maxlen = 500  # Maximum sequence length

    # Initialize and fit the tokenizer on training text
    tokenizer = Tokenizer(num_words=MAX_VOCAB_SIZE, oov_token="<OOV>")
    tokenizer.fit_on_texts(train_text)

    # Convert text to sequences
    X_train_seq = tokenizer.texts_to_sequences(train_text)
    X_val_seq = tokenizer.texts_to_sequences(val_text)
    X_test_seq = tokenizer.texts_to_sequences(test_text)

    # Apply padding to ensure uniform sequence length
    X_train_pad = pad_sequences(X_train_seq, maxlen=maxlen, padding="post", truncating="post")
    X_val_pad = pad_sequences(X_val_seq, maxlen=maxlen, padding="post", truncating="post")
    X_test_pad = pad_sequences(X_test_seq, maxlen=maxlen, padding="post", truncating="post")

    
    with mlflow.start_run() as active_run:
        run_id = active_run.info.run_id
        # add the git commit hash as tag to the experiment run
        git_hash = os.popen("git rev-parse --verify HEAD").read()[:-2]
        mlflow.set_tag("git_hash", git_hash)
        
        conv1d = get_model()
       
        
        # Train the model
        conv1d, history = train_model_and_save(conv1d,X_train_pad, y_train,X_val_pad,y_val, 
                class_weight_dict=class_weight_dict)
        
        # On récupère le dictionnaire des scores (loss, accuracy, val_loss, etc.)
        history_dict = history.history 

        # On boucle sur chaque époque pour créer les graphiques dans MLflow
        for epoch in range(len(history_dict['loss'])):
            metrics = {key: float(values[epoch]) for key, values in history_dict.items()}
            mlflow.log_metrics(metrics, step=epoch)

        # Sauvegarder l'historique complet en JSON comme artefact pour archive
        with tempfile.TemporaryDirectory() as temp_dir:
            history_path = os.path.join(temp_dir, "history.json")
            with open(history_path, "w") as f:
                json.dump(history_dict, f)
            mlflow.log_artifact(history_path, "training_metadata")
            
        # Save model as pickle file and log as artifact
        # This avoids the MLflow model registry complications with --serve-artifacts
        with tempfile.TemporaryDirectory() as temp_dir:
            model_path = os.path.join(temp_dir, 'conv1d.pkl')
            with open(model_path, 'wb') as f:
                pickle.dump(conv1d, f)
            
            # Log the model file as an artifact
            mlflow.log_artifact(model_path, 'conv1d')
            
            # Also log model metadata
            mlflow.log_param("model_type", type(conv1d).__name__)
        
        # Get the model URI - this will now point to the actual artifact location
        model_uri = mlflow.get_artifact_uri("conv1d")
       
    logger.info(f"completed script in {round(time.time() - start, 3)} seconds)") 
    
    return run_id, model_uri
    
    
