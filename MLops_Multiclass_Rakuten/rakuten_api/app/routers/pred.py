from bson import ObjectId
from pydantic import BaseModel, Field, EmailStr
from typing import Union, Optional, List
from fastapi.exceptions import RequestValidationError
from fastapi import (
    APIRouter,
    FastAPI, Depends, 
    Request, status, 
    Form, HTTPException ,
    File, 
    UploadFile)
from io import BytesIO
from PIL import Image
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from predictions.dlModels import (
     load_xception, load_conv1D,
     prepare_image, 
     predict_image_xception,
    predict_image_inception)
from predictions.dlModels import (
    predict_text_conv1D, 
    predict_text_simpleDNN, 
    prepare_text,
    predict_conv1D_simpleDNN_xception, 
    predict_conv1D_simpleDNN_inception)

from datetime import datetime, timedelta
from dependecies.dependecies import (
    get_current_user,
)
from users.predModel import (
  TextPrediction,
  ImagePrediction,
  MultiModalPrediction,
  predUserModel
)
from config.settings import ACCESS_TOKEN_EXPIRE_MINUTES
from config.database import db


predRouter = APIRouter()


# ============= ROUTES=============================================================================================================
@predRouter.post("/predict_with_text_Conv1D",  name= 'Based on Text Only - Conv1D', tags=['Predictions'], response_model=TextPrediction)
async def predict_with_text_Conv1D(designation: str = Form(), description: Optional[str] = Form(None),
                                   current_user: predUserModel = Depends(get_current_user)):
    """
    Allows you to make a prediction using Conv1D Model based on Text data with the designation field (mandatory) and the description field (optional).
    """
    text = prepare_text(designation, description)      
    response = predict_text_conv1D(text)  

    keys = ["designation_text", "description_text", "predicted_class", "predicted_label","precision" ]
    resp_keys = dict.fromkeys(keys)

 
    resp_keys["designation_text"] =   designation
    resp_keys["description_text"] =   description
    resp_keys["predicted_class"] =    response['predicted_class']
    resp_keys["predicted_label"] =    response['predicted_label']
    resp_keys["precision"] =          response['precision']
    
    return resp_keys


# ============================================================================================================================================
@predRouter.post("/predict_with_text_SimpleDN",  name= 'Based on Text Only - Simple DNN', tags=['Predictions'], response_model=TextPrediction)
async def predict_with_text_SimpleDNN(designation: str = Form(), description: Optional[str] = Form(None),
                                      current_user: predUserModel = Depends(get_current_user)):
    """
    Allows you to make a prediction using Simple DNN Model based on Text data with the designation field (mandatory) and the description field (optional)
    """
    text = prepare_text(designation, description)   
    response = predict_text_simpleDNN(text)  

    keys = ["designation_text", "description_text", "predicted_class", "predicted_label","precision" ]
    resp_keys = dict.fromkeys(keys)

  
    resp_keys["designation_text"] =   designation
    resp_keys["description_text"] =   description
    resp_keys["predicted_class"] =    response['predicted_class']
    resp_keys["predicted_label"] =    response['predicted_label']
    resp_keys["precision"] =          response['precision']
    
    return resp_keys


# ============================================================================================================================================
@predRouter.post("/predict_with_image_Xception",  name= 'Based on Image Only -  Xception', tags=['Predictions'], response_model=ImagePrediction)
async def predict_with_image_Xception(image_file: UploadFile = File(...), current_user: predUserModel = Depends(get_current_user)):

    """
    Allows you to make a prediction using Xception Model based on Image with a product image 
    """    
    # Ensure that the file is an image
    if not image_file.content_type.startswith("image"):
        raise HTTPException(status_code=400, detail="File provided is not an image.")

    content = await image_file.read()
    image = Image.open(BytesIO(content)).convert("RGB")

    # preprocess the image and prepare it for classification
    image = prepare_image(image, target=(299, 299))

  # Predict class preprocessed image  
    response = predict_image_xception(image)

    # return the response as a JSON
    return {
        "filename"        : image_file.filename,
        "content_type"    : image_file.content_type,
        "predicted_class" : response['predicted_class'],
        "predicted_label" : response['predicted_label'],
        "precision"       : response['precision'],
        
        }

# ============================================================================================================================================
@predRouter.post("/predict_with_image_Inception",  name= 'Based on Image Only -  Inception', tags=['Predictions'], response_model=ImagePrediction)
async def predict_with_image_Inception(image_file: UploadFile = File(...), current_user: predUserModel = Depends(get_current_user)):
    
    """
    Allows you to make a prediction using Inception Model based on Image with a product image 
    """       
    # Ensure that the file is an image
    if not image_file.content_type.startswith("image"):
        raise HTTPException(status_code=400, detail="File provided is not an image.")

    content = await image_file.read()
    image = Image.open(BytesIO(content)).convert("RGB")

    # preprocess the image and prepare it for classification
    image = prepare_image(image, target=(299, 299))

   # Predict class preprocessed image 
    response = predict_image_inception(image)

    # return the response as a JSON
    return {
        "filename"        : image_file.filename,
        "content_type"    : image_file.content_type,
        "predicted_class" : response['predicted_class'],
        "predicted_label" : response['predicted_label'],
        "precision"       : response['precision'],
        
        }


# ============================================================================================================================================
@predRouter.post("/predict_with_text_and_image_Conv1D_SimpleDNN_Xception", name= 'Multimodal(Text and Image) -  Conv1D, Simple DNN and Xception', tags=['Predictions']
                   , response_model=MultiModalPrediction)
async def predict_with_text_and_image_Conv1D_SimpleDNN_Xception( designation: str = Form(), description: Optional[str] = Form(None),
                                                                image_file: UploadFile = File(...),
                                                                current_user: predUserModel = Depends(get_current_user)):
    
    """
    Allows you to make a prediction using Text and Image data using Conv1D, Simple DNN and Xception Models 
    """  
    # Ensure that the file is an image
    if not image_file.content_type.startswith("image"):
        raise HTTPException(status_code=400, detail="File provided is not an image.")

    content = await image_file.read()
    image = Image.open(BytesIO(content)).convert("RGB")


    text = prepare_text(designation, description)  
    image = prepare_image(image, target=(299, 299))

    response_conv1d, response_simpDNN,  response_Xcep, pred_dict = predict_conv1D_simpleDNN_xception(text,image)   
  
   
    return {      
    "designation_txt":                designation,
    "description_text":               description,
    "image_filename":                 image_file.filename,
    "content_type":                   image_file.content_type ,    
    #  
    "predicted_class" :               pred_dict['predicted_class'],
    "predicted_label" :               pred_dict["predicted_label"] ,
    "precision" :                     pred_dict["precision"],

    "predicted_class_text_Model1" :   response_conv1d['predicted_class'],
    "predicted_label_text_Model1" :   response_conv1d["predicted_label"] ,
    "precision_text_Model1" :         response_conv1d["precision"],


    "predicted_class_text_Model2" :   response_simpDNN['predicted_class'],
    "predicted_label_text_Model2" :   response_simpDNN["predicted_label"] ,
    "precision_text_Model2" :         response_simpDNN["precision"],


    "predicted_class_image_model" :   response_Xcep['predicted_class'],
    "predicted_label_image_model" :   response_Xcep["predicted_label"] ,
    "precision_image_model" :         response_Xcep["precision"] ,
    }


# ============================================================================================================================================
@predRouter.post("/predict_with_text_and_image_Conv1D_SimpleDNN_Inception", name= 'Multimodal(Text and Image) - Conv1D, Simple DNN and Inception', tags=['Predictions']
                   , response_model=MultiModalPrediction)
async def predict_with_text_and_image_Conv1D_SimpleDNN_Inception( designation: str = Form(), description: Optional[str] = Form(None),
                                                                  image_file: UploadFile = File(...),
                                                                  current_user: predUserModel = Depends(get_current_user)):
    """
    Allows you to make a prediction using Text and Image data using Conv1D, Simple DNN and Inception Models 
    """ 
    # Ensure that the file is an image
    if not image_file.content_type.startswith("image"):
        raise HTTPException(status_code=400, detail="File provided is not an image.")

    content = await image_file.read()
    image = Image.open(BytesIO(content)).convert("RGB")


    text = prepare_text(designation, description)  
    image = prepare_image(image, target=(299, 299))

    response_conv1d, response_simpDNN,  response_incep, pred_dict = predict_conv1D_simpleDNN_inception(text,image)   
  
   
    return {      
    "designation_txt":                designation,
    "description_text":               description,
    "image_filename":                 image_file.filename,
    "content_type":                   image_file.content_type ,    
    #  
    "predicted_class" :               pred_dict['predicted_class'],
    "predicted_label" :               pred_dict["predicted_label"] ,
    "precision" :                     pred_dict["precision"],

    "predicted_class_text_Model1" :   response_conv1d['predicted_class'],
    "predicted_label_text_Model1" :   response_conv1d["predicted_label"] ,
    "precision_text_Model1" :         response_conv1d["precision"],


    "predicted_class_text_Model2" :   response_simpDNN['predicted_class'],
    "predicted_label_text_Model2" :   response_simpDNN["predicted_label"] ,
    "precision_text_Model2" :         response_simpDNN["precision"],


    "predicted_class_image_model" :   response_incep['predicted_class'],
    "predicted_label_image_model" :   response_incep["predicted_label"] ,
    "precision_image_model" :         response_incep["precision"] ,
    }

# ============================================================================================================================================