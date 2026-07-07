import os
import numpy as np

import tensorflow as tf
from sklearn.metrics import f1_score

# Assurez-vous que is_Debug est défini en global
# is_Debug = True
is_Debug = False

def predict_text_model(text_model, x_val_text, y_val=None, max_sequence_length=500, return_proba=False):
    """
    Predict using the pre-trained text model on the validation data.

    Args:
    - text_model: Loaded text model.
    - x_val_text: Raw text data (string or list).
    - y_val: True labels (optional).
    - max_sequence_length: Sequence length for padding.
    - return_proba: If True, returns probabilities instead of class predictions.

    Returns:
    - predictions or probabilities
    - evaluation_metrics if y_val provided
    """

    if is_Debug:
        print(f"[INFO] Loading tokenizer and applying preprocessing on validation text data.")

    _, _, tokenizer = load_tokenized_text_data(num_samples=None)

    if isinstance(x_val_text, str):
        x_val_text = [x_val_text]
        if is_Debug:
            print(f"[INFO] x_val_text is a single string.")

    x_val_text_tokenized = tokenizer.texts_to_sequences(x_val_text)
    x_val_text_padded = tf.keras.preprocessing.sequence.pad_sequences(
        x_val_text_tokenized,
        padding='post',
        maxlen=max_sequence_length
    )

    if is_Debug:
        print(f"[INFO] Tokenization & Padding done.")
        print(f"[DEBUG] Sample padded data : {x_val_text_padded[:5]}")

    y_proba = text_model.predict(x_val_text_padded, verbose=0)

    if return_proba:
        return y_proba  # Direct return of probabilities

    predictions = np.argmax(y_proba, axis=-1)

    if y_val is not None:
        if is_Debug:
            print("[INFO] Evaluating predictions with true labels.")

        accuracy = np.mean(predictions == y_val)
        f1_score_value = compute_f1_score(y_val, predictions)

        if is_Debug:
            print(f"[INFO] Accuracy: {accuracy:.4f} | F1 Score: {f1_score_value:.4f}")

        evaluation_metrics = {
            "accuracy": accuracy,
            "f1_score": f1_score_value
        }

        return predictions, evaluation_metrics
    else:
        return predictions



def compute_f1_score(y_true, y_pred):
    """
    Compute F1 Score between true and predicted labels.
    """
    from sklearn.metrics import f1_score
    return f1_score(y_true, y_pred, average='weighted')


def evaluate_combined_predictions(y_val, predictions, metric="f1"):
    """
    Evaluate the performance of the combined model predictions using F1-score.

    Args:
    - y_val: True labels.
    - predictions: Predicted labels.

    Returns:
    - score: The F1-score of the combined predictions.
    """
    if is_Debug:
        print(f"[INFO] Evaluating combined model predictions.")
    
    if metric == "f1":
        score = f1_score(y_val, predictions, average='weighted')
    else:
        raise ValueError(f"[ERROR] Metric {metric} not supported.")
    
    return score



