import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

import argparse
import os
import sys
from pathlib import Path
import importlib
import pandas as pd
import tensorflow as tf
from nltk.corpus import stopwords

from tensorflow import keras
import logging
from src.data_preprocessing import text_cleaning
from sklearn.model_selection import train_test_split

logger = logging.getLogger(__name__)

TRAIN_FILE = "X_train_update.csv"
TARGET_FILE = "Y_train_CVw08PX.csv"
TEST_FILE = "X_test_update.csv"

# Define the mapping of prdtypecode to category labels

dict_code_label = {
    10: "Adult Books",
    40: "Imported Video Games",
    50: "Video Games Accessories",
    60: "Games and Consoles",
    1140: "Figurines and Toy Pop",
    1160: "Playing Cards",
    1180: "Figurines, Masks, and Role-Playing Games",
    1280: "Toys for Children",
    1281: "Board Games",
    1300: "Remote Controlled Models",
    1301: "Accessories for Children",
    1302: "Toys, Outdoor Playing, and Clothes",
    1320: "Early Childhood",
    1560: "Interior Furniture and Bedding",
    1920: "Interior Accessories",
    1940: "Food",
    2060: "Decoration Interior",
    2220: "Supplies for Domestic Animals",
    2280: "Magazines",
    2403: "Children Books and Magazines",
    2462: "Games",
    2522: "Stationery",
    2582: "Furniture, Kitchen, and Garden",
    2583: "Piscine and Spa",
    2585: "Gardening and DIY",
    2705: "Books",
    2905: "Online Distribution of Video Games"
}

# === 🔹 FUNCTION TO LOAD DATA === #
def load_data(file_name, data_path):
    """
    Load a dataset from the given file path.

    Parameters:
    - file_name (str): Name of the file to load.
    - data_path (str): Path where the file is located.

    Returns:
    - pd.DataFrame: Loaded dataset as a pandas DataFrame.
    """
    file_path = os.path.join(data_path, file_name)
    
    try:
        df = pd.read_csv(file_path,index_col=0)
        print(f"Successfully loaded {file_name} | Shape: {df.shape}")
        return df
    except FileNotFoundError:
        print(f"Error: The file {file_name} was not found in {data_path}")
        return None
    except Exception as e:
        print(f"Error loading {file_name}: {e}")
        return None
    
def data_prepped(input_folder, output_folder):
    """
    Prépare les données et sauvegarde les splits
    """
    # === 🔹 LOAD DATASETS === #
    X_train  = load_data(TRAIN_FILE,input_folder)
    y_train  = load_data(TARGET_FILE,input_folder)
    X_test   = load_data(TEST_FILE,input_folder)
    
    X_full_train  = X_train.copy()
    X_full_train["prdtypecode"] = y_train["prdtypecode"]
    
    # ============================================================= #
    #  CLEANING 'designation' COLUMN
    # ============================================================= #
    print("\n[INFO] Cleaning 'designation' column...")
    X_full_train["designation"] = X_full_train["designation"].apply(text_cleaning.clean_text_pipeline)
    X_test["designation"] = X_test["designation"].apply(text_cleaning.clean_text_pipeline)

    # ============================================================= #
    #  CREATING & CLEANING 'text' COLUMN
    # ============================================================= #
    print("\n[INFO] Creating and cleaning 'text' column...")
    X_full_train["text"] = X_full_train.apply(lambda row: text_cleaning.create_clean_text(row["designation"], row["description"]), axis=1)
    X_test["text"] = X_test.apply(lambda row: text_cleaning.create_clean_text(row["designation"], row["description"]), axis=1)

    X_full_train["text"] = X_full_train["text"].apply(text_cleaning.clean_text_pipeline)
    X_test["text"] = X_test["text"].apply(text_cleaning.clean_text_pipeline)

    mapping_df = pd.DataFrame(list(dict_code_label.items()), columns=["prdtypecode", "Category"])
    
    # Add the category labels to X_train
    
    X_full_train["Label"] = X_full_train["prdtypecode"].map(mapping_df.set_index("prdtypecode")["Category"])
    
    # Convert product codes to numerical labels
    
    prdtypecodes = sorted(X_full_train["prdtypecode"].unique())  # Ensure consistent order
    target_mapping = {code: i for i, code in enumerate(prdtypecodes)}  # Mapping {prdtypecode: numeric_label}

    # Apply mapping to encode target variable
    y_train_encoded = y_train["prdtypecode"].map(target_mapping).astype("int8")  # Memory optimization

    # Apply encoding to X_train
    X_full_train["prdtypecode_encoded"] = X_full_train["prdtypecode"].map(target_mapping).astype("int8")
    

    # Reorder columns in X_train
    X_full_train = X_full_train[[
        "designation", "description", "text", "productid", "imageid", 
        "prdtypecode", "prdtypecode_encoded", "Label"
    ]]

    # Reorder columns in X_test_sub for consistency (no prdtypecode column)
    X_test = X_test[[
        "designation", "description", "text", "productid", "imageid"
    ]]
    
    TEST_SIZE = 0.2
    RANDOM_STATE = 42

    # Split the dataset into training and validation sets (stratified on prdtypecode_encoded)
    X_train_split, X_val_split = train_test_split(
        X_full_train, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=X_full_train["prdtypecode_encoded"]
    )
    
    X_train_split_path = os.path.join(output_folder, "X_train_split.csv")
    X_val_split_path = os.path.join(output_folder, "X_val_split.csv")
    X_test_path = os.path.join(output_folder, "X_test.csv")
    
    X_train_split.to_csv(X_train_split_path, index=False)
    X_val_split.to_csv(X_val_split_path, index=False)
    X_test.to_csv(X_test_path, index=False)
    
    return {
        "X_train_split_path": X_train_split_path,
        "X_val_split_path": X_val_split_path,
        "X_test_path": X_test_path
    }

if __name__ == "__main__":
    """Garde le CLI pour usage local"""
    parser = argparse.ArgumentParser(description='data_processing')
    parser.add_argument('--input_folder', type=str, help='Input folder')
    parser.add_argument('--output_folder', type=str, help='Output folder') 
    args = parser.parse_args()
    data_prepped(args.input_folder, args.output_folder)