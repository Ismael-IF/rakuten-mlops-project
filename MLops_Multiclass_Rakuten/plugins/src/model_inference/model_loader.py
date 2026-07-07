import tensorflow as tf
import config
import os

# Global variable for debugging
# is_Debug = False  # Set to False to enable debug prints
is_Debug = True  # Set to False to disable debug prints

def load_text_model(model_name):
    """
    Loads a pre-trained text model (Simple DNN or Conv1D) from the specified directory.

    Args:
    - model_name: str, name of the model to load (e.g., 'simple_dnn.h5' or 'conv1d_model.h5').

    Returns:
    - model: Loaded Keras model.
    """
    # Define the path to the pre-trained text model
    text_model_dir = config.NEURAL_MODELS_DIR
    text_model_path = os.path.join(text_model_dir, model_name)
    
    # Show where we're loading models from (once)
    if is_Debug:
        print(f"\n[DEBUG] Base directory for text models: {os.path.relpath(text_model_dir, config.BASE_DIR)}")
      
    
    # Debug prints
    if is_Debug:     
        print(f"[DEBUG] Checking if the model exists at: {os.path.relpath(text_model_path, config.BASE_DIR)}")
    
    # Check if model file exists
    if not os.path.exists(text_model_path):
        print(f"[ERROR] Text model file not found: {text_model_path}")
        raise FileNotFoundError(f"Text model file not found: {text_model_path}")
    
    # Load the model
    if is_Debug: 
        print(f"[INFO] Loading text model from {os.path.relpath(text_model_path, config.BASE_DIR)}")
    model = tf.keras.models.load_model(text_model_path)
    
    # if is_Debug:
    print(f"[✔] Successfully loaded text model: {model_name}")
    
    return model


def load_image_model(model_name):
    """
    Loads a pre-trained image model (e.g., Xception or InceptionV3) from the specified directory.

    Args:
    - model_name: str, name of the model to load (e.g., 'xception_model.h5' or 'inceptionv3_model.h5').

    Returns:
    - model: Loaded Keras model.
    """
    # Define the base directory and full path for the pre-trained image model
    image_model_dir = config.FINAL_TRAINING_DIR
    image_model_path = os.path.join(image_model_dir, model_name)

    # Debug output for clarity
    if is_Debug:
        # print(f"\n[DEBUG] Base directory for image models: {image_model_dir}")
        print(f"\n[DEBUG] Base directory for image models: {os.path.relpath(image_model_dir, config.BASE_DIR)}")
      

    
    # Debug prints
    if is_Debug:
        # print(f"[DEBUG] Checking if the model exists at: {image_model_path}")
        print(f"[DEBUG] Checking if the model exists at: {os.path.relpath(image_model_path, config.BASE_DIR)}")
    
    # Check if model file exists
    if not os.path.exists(image_model_path):
        print(f"[ERROR] Image model file not found: {image_model_path}")
        raise FileNotFoundError(f"Image model file not found: {image_model_path}")
    
    # Load the model
    if is_Debug:
        # print(f"[INFO] Loading image model from {image_model_path}")
        print(f"[DEBUG] Loading image model from : {os.path.relpath(image_model_path, config.BASE_DIR)}")

    model = tf.keras.models.load_model(image_model_path)
    
    # if is_Debug:
    print(f"[✔] Successfully loaded image  model: {model_name}")
    
    return model
