# -*- coding: utf-8 -*-

import numpy as np
from PIL import Image
from tensorflow.keras.applications import ResNet50, imagenet_utils
from tensorflow.keras.applications.imagenet_utils import (decode_predictions,preprocess_input)
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
from config.inputs import *
from PIL import Image
import pickle
from cleaning.text_cleaning import *
from config.debug import log
from tabulate import tabulate
from pydantic import parse_obj_as
from fastapi.encoders import jsonable_encoder
import os
from  functools import lru_cache
import mlflow
from mlflow.tracking import MlflowClient
import joblib

module_name =  'models'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models/trained_models/final_model.pkl")

@lru_cache()
def load_tokenizer():
    """
    Loads and returns the Fitted Tokenizer
    """
 
    with open(tokenizer_dir + fitted_tokenizer_name, 'rb') as handle:
        fitted_tokenizer = pickle.load(handle)
      #log(module_name, 'load_tokenizer', "Fitted Tokenizer loaded")    
   
    return fitted_tokenizer



@lru_cache()
def load_conv1D():
    """
    Loads and returns the pretrained model
    """
    # Load Conv1D
 
    model = load_model(model_dir + conv1D_fname ,  compile = False )    

    #log(module_name, 'load_conv1D', "Conv1D loaded")
   
    return model
   

@lru_cache()
def load_simpleDNN():
    """
    Loads and returns the pretrained model
    """
    # Load Conv1D
 
    model = load_model(model_dir + simpleDNN_fname ,  compile = True )    

    #log(module_name, 'load_simpleDNN', "Simple DDN loaded")
   
    return model

@lru_cache()
def load_xception():
    """
    Loads and returns the pretrained model
    """
    # Load xception  
    model = load_model(model_dir + xception_fname ,  compile = True )   
    #log(module_name, 'load_xception', "Model Xception loaded")
    
    return model


@lru_cache()
def load_inception():
    """
    Loads and returns the pretrained model
    """
    # Load xception  
    model = load_model(model_dir + inception_fname ,  compile = True )   
    #log(module_name, 'load_xception', "Model Inception loaded")
    
    return model


def prepare_image(image, target):
    # resize the input image and preprocess it
    image = image.resize(target)
    image = img_to_array(image)
    image = image/255    
    image = np.expand_dims(image, axis=0)
    return image



def tokenize_text(input_text):
    
    fitted_tokenizer = load_tokenizer()
    
    maxlen = 500 
    text = fitted_tokenizer.texts_to_sequences(input_text)
    text = tf.keras.preprocessing.sequence.pad_sequences(text,
                                                            maxlen = maxlen,
                                                            padding='post')       
    return text


def prepare_text(text_desig, text_descrip):
       
     df = createdfManuel(text_desig, text_descrip)
     df_cleaned = CreateTextANDcleaning(df)

    #  print('-------------------------------------------------\n')  
    #  print(df_cleaned.to_markdown())
    #  print('-------------------------------------------------\n')  
     return df_cleaned   
    

def predict_text_conv1D(text_cleaned): 
    
    text_tokenized = tokenize_text(text_cleaned)
    model = load_conv1D()
    #model.summary()
    y_pred_proba = model.predict(text_tokenized)
    y_pred_class = np.argmax(y_pred_proba,axis = 1).astype(int)    
    
    # Prediction
    y_pred = y_pred_class[0]
    pred_class = get_class_code(y_pred)
    pred_label = get_label(pred_class)
    
    precision = np.amax(y_pred_proba)
    precision = precision * 100
    precision = np.round(precision,2)

    pred_dict = {"predicted_class": pred_class,
                 "predicted_label":pred_label,
                 "predicted_proba":y_pred_proba,
                 "precision": str(precision)+'%'
                    }
    return pred_dict    
    
def predict_text_simpleDNN(text_cleaned): 
    
    text_tokenized = tokenize_text(text_cleaned)
    model = load_simpleDNN()
    #model.summary()
    y_pred_proba = model.predict(text_tokenized)
    y_pred_class = np.argmax(y_pred_proba,axis = 1).astype(int)    
    
    # Prediction
    y_pred = y_pred_class[0]
    pred_class = get_class_code(y_pred)
    pred_label = get_label(pred_class)
    
    precision = np.amax(y_pred_proba)
    precision = precision * 100
    precision = np.round(precision,2)
   
        
    pred_dict = {"predicted_class": pred_class,
                 "predicted_label":pred_label,
                 "predicted_proba":y_pred_proba,
                 "precision": str(precision)+'%'
                    }
    return pred_dict  


def predict_image_xception(image): 
    
        model = load_xception()   
        out_proba = model.predict(image)
        im_pred= np.argmax(out_proba)
        
        # To matches with data-generator labels 
        permutation = [0, 1, 12, 20, 21, 22, 23, 24, 25, 26, 2, 3,
                 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16
                 ,17, 18, 19]
        
        out_proba = out_proba[:, permutation] 
        
        im_pred_target = get_real_target(im_pred)
        im_pred_code = get_class_code(im_pred_target)
        im_pred_label = get_label(im_pred_code)
        
        precision = np.amax(out_proba)
        precision = precision * 100
        precision = np.round(precision,2)
               

        
        pred_dict = {"predicted_class": im_pred_code,
                    "predicted_label":im_pred_label,
                    "predicted_proba":out_proba,
                    "precision": str(precision)+'%'
                    }     
        return pred_dict
    
def predict_image_inception(image): 
    
        model = load_inception()   
        out_proba = model.predict(image)
        im_pred= np.argmax(out_proba)
        
        # To matches with data-generator labels 
        permutation = [0, 1, 12, 20, 21, 22, 23, 24, 25, 26, 2, 3,
                 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16
                 ,17, 18, 19]
        
        out_proba = out_proba[:, permutation] 
        
        im_pred_target = get_real_target(im_pred)
        im_pred_code = get_class_code(im_pred_target)
        im_pred_label = get_label(im_pred_code)
        
        precision = np.amax(out_proba)
        precision = precision * 100
        precision = np.round(precision,2)
               

        
        pred_dict = {"predicted_class": im_pred_code,
                    "predicted_label":im_pred_label,
                    "predicted_proba":out_proba,
                    "precision": str(precision)+'%'
                    }
        

        return pred_dict

def predict_conv1D_simpleDNN_xception(text_cleaned, image): 
    
    pred_dict_conv1D  = predict_text_conv1D(text_cleaned)
    pred_dict_simpDnn  = predict_text_simpleDNN(text_cleaned)
    pred_dict_xception  = predict_image_xception(image) 

    weighted_proba = ((pred_dict_conv1D['predicted_proba'] * conv1D_SC) + (pred_dict_simpDnn['predicted_proba']  * simplDNN_SC) + \
                     (pred_dict_xception['predicted_proba']  * xception_SC)) / (conv1D_SC + simplDNN_SC + xception_SC)
       
    
    y_pred_class = np.argmax(weighted_proba,axis = 1).astype(int)  

    y_pred = y_pred_class[0]
    pred_class = get_class_code(y_pred)
    pred_label = get_label(pred_class)
    proba = np.amax(weighted_proba) 

    precision = np.amax(proba)
    precision = precision * 100
    precision = np.round(precision,2)
 

    pred_dict = {"predicted_class": pred_class,
                 "predicted_label":pred_label,
                 "predicted_proba":proba,
                 "precision": str(precision)+'%'
               }

    return pred_dict_conv1D,  pred_dict_simpDnn, pred_dict_xception, pred_dict

def predict_conv1D_simpleDNN_inception(text_cleaned, image): 

    
    pred_dict_conv1D  = predict_text_conv1D(text_cleaned)
    pred_dict_simpDnn  = predict_text_simpleDNN(text_cleaned)
    pred_dict_inception  = predict_image_inception(image)


    weighted_proba = ((pred_dict_conv1D['predicted_proba'] * conv1D_SC) + (pred_dict_simpDnn['predicted_proba']  * simplDNN_SC) + \
                     (pred_dict_inception['predicted_proba']  * inception_SC)) / (conv1D_SC + simplDNN_SC + inception_SC)
       
    
    y_pred_class = np.argmax(weighted_proba,axis = 1).astype(int)  

    y_pred = y_pred_class[0]
    pred_class = get_class_code(y_pred)
    pred_label = get_label(pred_class)
    proba = np.amax(weighted_proba) 

    precision = np.amax(proba)
    precision = precision * 100
    precision = np.round(precision,2)
   

    pred_dict = {"predicted_class": pred_class,
                 "predicted_label":pred_label,
                 "predicted_proba":proba,
                 "precision": str(precision)+'%'
               }

    return pred_dict_conv1D,  pred_dict_simpDnn, pred_dict_inception, pred_dict
    
def get_real_target(val):
    
    dict_labels = {'0': 0,
                 '1': 1,
                 '10': 2,
                 '11': 3,
                 '12': 4,
                 '13': 5,
                 '14': 6,
                 '15': 7,
                 '16': 8,
                 '17': 9,
                 '18': 10,
                 '19': 11,
                 '2': 12,
                 '20': 13,
                 '21': 14,
                 '22': 15,
                 '23': 16,
                 '24': 17,
                 '25': 18,
                 '26': 19,
                 '3': 20,
                 '4': 21,
                 '5': 22,
                 '6': 23,
                 '7': 24,
                 '8': 25,
                 '9': 26}
        
    
    for real_cls, gen_label in dict_labels.items():
         if val == gen_label:
            return int(real_cls)

    return "class doesn't exist"

def get_class_code(val):
    dict_class =       {0:10, 1:40, 2:50, 3:60, 4:1140,
                        5:1160, 6:1180, 7:1280, 8:1281,
                        9:1300, 10:1301, 11:1302, 12:1320,
                        13:1560, 14:1920, 15:1940, 16:2060,
                        17:2220, 18:2280, 19:2403, 20:2462,
                        21:2522, 22:2582, 23:2583, 24:2585,
                        25:2705, 26:2905,
                        }   
    return dict_class[val]
    dict_class =       {0:10, 1:40, 2:50, 3:60, 4:1140,
                        5:1160, 6:1180, 7:1280, 8:1281,
                        9:1300, 10:1301, 11:1302, 12:1320,
                        13:1560, 14:1920, 15:1940, 16:2060,
                        17:2220, 18:2280, 19:2403, 20:2462,
                        21:2522, 22:2582, 23:2583, 24:2585,
                        25:2705, 26:2905,
                        }   
    return dict_class[val]


def get_label(code):
    dict_code_label =  { 50: 'video games accessories',
                         2705: 'books',
                         2522: 'stationery',
                         2582: 'furniture kitchen and garden',
                         1560: 'interior furniture and bedding',
                         1281: 'board games',
                         1920: 'interior accessories',
                         1280: 'toys for children',
                         1140: 'figurines and Toy Pop',
                         1300: 'remote controlled models',
                         2060: 'decoration interior',
                         2583: 'piscine spa',
                         60: 'games and consoles',
                         1320: 'early childhood',
                         2280: 'magazines',
                         1302: 'toys, outdoor playing, clothes',
                         2220: 'supplies for domestic animals',
                         40: 'imported video games',
                         2905: 'online distribution of video games',
                         2585: 'gardening and DIY',
                         1940: 'Food',
                         1160: 'playing cards',
                         1301: 'accessories children',
                         10: 'adult books',
                         1180: 'figurines, masks and role playing games',
                         2403: 'children books and magazines',
                         2462: 'games'}
   
    return dict_code_label[code]