import tensorflow as tf
import os
import pandas as pd
import pickle
from pathlib import Path
from sklearn.metrics import f1_score
import numpy as np
import config

# is_Debug = True
is_Debug = False

def train_model_and_save(model, x_train, y_train,x_val,y_val, epochs=40, batch_size=64, 
                class_weight_dict=None, learning_rate=0.001, early_stopping_patience=5, model_name="model_name", 
                save_model_dir=None, step_name=None, lr_scheduler=None):
    """
    Trains the model (Conv1D, DNN, RNN with GRU, RNN with LSTM) and saves the model and its checkpoints.

    Args:
    - model: The model to train (already created model passed as argument).
    - train_data: The training data generator.
    - x_val: The validation data generator.
    - epochs: Number of epochs for training.
    - batch_size: Batch size for training.
    - class_weight_dict: Dictionary of class weights (optional).
    - learning_rate: Learning rate for the optimizer.
    - model_name: The model's name for generating save file names.
    - save_model_dir: Directory where the model and checkpoints should be saved.
    - early_stopping_patience: Number of epochs with no improvement after which training will stop.
    - lr_scheduler: Learning rate scheduler (optional).
        
    Returns:
    - model: The trained model.
    - history: The training history.
    """

    # Optimizer
    optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)
    model.compile(optimizer=optimizer, loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    # Callback for early stopping
    early_stopping_callback = tf.keras.callbacks.EarlyStopping(
        monitor='val_loss',
        patience=early_stopping_patience,
        restore_best_weights=True,
        verbose=1
    )

    # Training the model
    history = model.fit(
        x_train,
        y_train,
        epochs=epochs,
        batch_size=batch_size,
        validation_data=(x_val, y_val),
        class_weight=class_weight_dict,
        callbacks=early_stopping_callback
    )


    return model, history
