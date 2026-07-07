import os

# 📌 Base directory of the project (local execution)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 📂 Data directory
DATA_DIR = os.path.join(BASE_DIR, "data")

# 📂 Data directory
SUBMISSION_DIR = os.path.join(BASE_DIR, "submissions")


# 📂 Raw Data Paths
RAW_CSV_DIR = os.path.join(DATA_DIR, "raw_csv")  # Raw CSV files (metadata + text)
RAW_IMAGES_DIR = os.path.join(DATA_DIR, "raw_images")  # Raw images (train/test)
RAW_IMAGE_TRAIN_DIR = os.path.join(RAW_IMAGES_DIR, "image_train")
RAW_IMAGE_TEST_SUB_DIR = os.path.join(RAW_IMAGES_DIR, "image_test")

# 📂 Processed Data Paths
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")

# 📂 Interim Text Data
INTERIM_DIR = os.path.join(DATA_DIR, "interim")

# 📂 Processed Text Data
PROCESSED_TEXT_DIR = os.path.join(PROCESSED_DIR, "text")



# Text_Vectorization_TF-IDF
XTRAIN_MATRIX_PATH = os.path.join(PROCESSED_TEXT_DIR, "Xtrain_matrix.pkl")
XVAL_MATRIX_PATH = os.path.join(PROCESSED_TEXT_DIR, "Xval_matrix.pkl")
XTEST_MATRIX_PATH = os.path.join(PROCESSED_TEXT_DIR, "Xtest_matrix.pkl")
TFIDF_VECTORIZER_PATH = os.path.join(PROCESSED_TEXT_DIR, "tfidf_vectorizer.pkl")

#The encoded labels (0-26) and their original product code classes
YTRAIN_ENCODED_PATH = os.path.join(PROCESSED_TEXT_DIR, "y_train_encoded.pkl")
PRDTYPECODE_MAPPING_PATH = os.path.join(PROCESSED_DIR, "prdtypecode_mapping.pkl")

# Text Tokenization_and_Sequencing
TOKENIZER_PATH =  os.path.join(PROCESSED_TEXT_DIR, "tokenizer.pkl")
X_TRAIN_SPLIT_TOKENIZED_PATH =  os.path.join(PROCESSED_TEXT_DIR, "X_train_TokenizationSequencing.pkl")
X_TEST_SPLIT_TOKENIZED_PATH =  os.path.join(PROCESSED_TEXT_DIR, "X_test_TokenizationSequencing.pkl")
Y_TRAIN_SPLIT_PATH =  os.path.join(PROCESSED_TEXT_DIR, "y_train_split.pkl")
Y_TEST_SPLIT_PATH =  os.path.join(PROCESSED_TEXT_DIR, "y_test_split.pkl")

X_SUBMISSION_TOKENIZED_PATH =  os.path.join(PROCESSED_TEXT_DIR, "X_submission_TokenizationSequencing.pkl")


# 📂 Processed Image Data
PROCESSED_IMAGES_DIR = os.path.join(PROCESSED_DIR, "images")
RESIZED_IMAGE_DIR = os.path.join(PROCESSED_IMAGES_DIR, "resized")
RESIZED_IMAGE_TRAIN_DIR = os.path.join(RESIZED_IMAGE_DIR, "image_train")
RESIZED_IMAGE_TEST_DIR = os.path.join(RESIZED_IMAGE_DIR, "image_test")

IMAGE_FEATURES_DIR = os.path.join(PROCESSED_IMAGES_DIR, "features")
CNN_FEATURES_TRAIN = os.path.join(IMAGE_FEATURES_DIR, "cnn_features_train.pkl")
CNN_FEATURES_TEST = os.path.join(IMAGE_FEATURES_DIR, "cnn_features_test.pkl")
HOG_FEATURES_PATH = os.path.join(IMAGE_FEATURES_DIR, "hog_features.pkl")
SIFT_FEATURES_PATH = os.path.join(IMAGE_FEATURES_DIR, "sift_features.pkl")
PCA_IMAGES_PATH = os.path.join(IMAGE_FEATURES_DIR, "pca_images.pkl")

# 📄 Final Datasets
XTRAIN_FINAL_PATH = os.path.join(PROCESSED_DIR, "X_train_final.pkl") 
XTRAIN_FINAL_ENCODED_PATH = os.path.join(PROCESSED_DIR, "X_train_final_encoded.pkl") 
XTEST_SUB_FINAL_PATH = os.path.join(PROCESSED_DIR, "X_test_Submission_final.pkl")
YTRAIN_FINAL_PATH = os.path.join(PROCESSED_DIR, "y_train_final.pkl")


# 📂 Models directory
MODELS_DIR = os.path.join(BASE_DIR, "models")

# 📂 Text Models directory
TEXT_MODELS_DIR = os.path.join(MODELS_DIR, "text")
# 📂 Classical models
CLASSICAL_MODELS_DIR = os.path.join(TEXT_MODELS_DIR, "classical")

# 📂 Neural models
NEURAL_MODELS_DIR = os.path.join(TEXT_MODELS_DIR, "neural")

# 📂 Benchmak text model
BENCHMARK_TEXT_MODEL_DIR = os.path.join(TEXT_MODELS_DIR, "benchmark")


# 📂 Image Models directory
IMAGE_MODELS_DIR = os.path.join(MODELS_DIR, "image")

# 📂 Benchmak image model
BENCHMARK_IMG_MODEL_DIR = os.path.join(IMAGE_MODELS_DIR, "benchmark")

# 📂 Subdirectories for Image Models (steps of training pipeline)
# 📂 Data Augmentation
DATA_AUGMENTATION_DIR = os.path.join(IMAGE_MODELS_DIR, "data_augmentation")

# 📂 Fine-Tuning
FINE_TUNING_DIR = os.path.join(IMAGE_MODELS_DIR, "fine_tuning")

# 📂 Learning Rate Optimization
LR_OPTIMIZATION_DIR = os.path.join(IMAGE_MODELS_DIR, "lr_optimization")

# 📂 Final Training
FINAL_TRAINING_DIR = os.path.join(IMAGE_MODELS_DIR, "final_training")


# 📄 Best model filenames (Text + Image)
BEST_TEXT_MODEL_CONV1D = "Model_Texte_Conv1D.hdf5"
BEST_TEXT_MODEL_DNN = "Model_Texte_SimpleDNN.hdf5"
BEST_IMAGE_MODEL_XCEPTION = "Model_Images_Xception.hdf5"
BEST_IMAGE_MODEL_INCEPTION = "Model_Images_InceptionV3.hdf5"



# 📂 Notebooks directory
NOTEBOOKS_DIR = os.path.join(BASE_DIR, "notebooks")
EDA_NOTEBOOKS_DIR = os.path.join(NOTEBOOKS_DIR, "eda_and_processing")
TEXT_MODELING_NOTEBOOKS_DIR = os.path.join(NOTEBOOKS_DIR, "modeling/text")
IMAGE_MODELING_NOTEBOOKS_DIR = os.path.join(NOTEBOOKS_DIR, "modeling/image")
BIMODAL_MODELING_NOTEBOOKS_DIR = os.path.join(NOTEBOOKS_DIR, "modeling/bimodal")

# 📂 Reports Directory
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
CLASSIFICATION_REPORTS_DIR = os.path.join(REPORTS_DIR, "classification_reports")

# 📂 Classification Reports for Different Modalities
TEXT_REPORTS_DIR = os.path.join(CLASSIFICATION_REPORTS_DIR, "text")
IMAGE_REPORTS_DIR = os.path.join(CLASSIFICATION_REPORTS_DIR, "image")
BIMODAL_REPORTS_DIR = os.path.join(CLASSIFICATION_REPORTS_DIR, "bimodal")


