import tensorflow as tf
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense, Dropout
from tensorflow.keras.regularizers import l2
from tensorflow.keras.models import Model

# is_Debug = True
is_Debug = False

# Model architecture selection
def create_model(model_type="Conv1D", vocab_size=20000, embedding_dim=100, max_sequence_length=500, num_classes=27):
    """
    Create and return a model based on the model_type.
    
    Args:
    - model_type (str): Type of model to create (Conv1D, DNN, RNN_GRU, RNN_LSTM).
    - vocab_size (int): Size of the vocabulary (e.g., the maximum number of unique tokens).
    - embedding_dim (int): Dimension of the embedding layer.
    - max_sequence_length (int): Maximum length of input sequences (e.g., number of tokens in each input).
    - num_classes (int): Number of output classes.
    
    Returns:
    - model: The created Keras model.
    """

    if model_type == "Conv1D":
            model = tf.keras.Sequential([
            tf.keras.layers.Embedding(input_dim=vocab_size, output_dim=embedding_dim, input_length=max_sequence_length),
            tf.keras.layers.SpatialDropout1D(0.2),
            tf.keras.layers.Conv1D(64, 2, activation='relu'),
            tf.keras.layers.GlobalMaxPooling1D(),
            tf.keras.layers.Dense(num_classes, activation='softmax')
        ])
    
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001), 
                  loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    return model
