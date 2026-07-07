from io import BytesIO
from typing import Union, Optional, List
from fastapi import FastAPI, Depends, Request, status, HTTPException
from pydantic import BaseModel
from dependecies.dependecies import authenticate_user
from routers.admin import adminRouter
from routers.users import usersRouter
from routers.pred import predRouter
from config.debug import log
import base64
import binascii
import uvicorn

from config.settings import ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta

from dependecies.dependecies import (
    get_current_user,
    authenticate_user,
    create_access_token,
    get_password_hash
)
from config.database import Users_db

description = """
This challenge focuses on the topic of large-scale product type code multimodal (text and image) classification where the goal is to predict each product’s type code as defined in the catalog of Rakuten France.
"""

app = FastAPI(
    openapi_tags=[                  
                    {
                         'name': 'Default'
                         #'description': 'Root'
                     },

                    {
                        'name': 'Admin',
                        'description': 'Admin functionalities'
                    },

                    {
                        'name': 'Users',
                        'description': 'Users functionalities'
                    },
                    
                    {
                        'name': 'Predictions',
                        'description': 'NLP, Computer Vision functionalities'
                    }
                            
                        ],
    
 title="API - Rakuten France Multimodal Product Data Classification",
 description=description,
 version="0.0.1",
contact={
    "name": "Ismael Foudjo",
    "url": "https://github.com/Ismael-IF"
        }
    )
                                      
#authenticate                   
@app.middleware("http")
async def authenticate(request: Request, call_next):

#-------------------- Authentication basic scheme -----------------------------
    if "Authorization" in request.headers:
        auth = request.headers["Authorization"]
        try:
            scheme, credentials = auth.split()
            if scheme.lower() == 'basic':
                decoded = base64.b64decode(credentials).decode("ascii")
                username, _, password = decoded.partition(":")
                request.state.user = await authenticate_user(username, password)
        except (ValueError, UnicodeDecodeError, binascii.Error):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid basic auth credentials"
            )

    response = await call_next(request)
    return response


#-------------------------Default Routes--------------------------------------------------------                     
#-----------------------------------------------------------------------------------------------
@app.get("/",tags=['Default'])
async def root():
    """  
     This route allows to check if API is operational 
    """    
    return {"message": "Welcome to Rakuten API"}


@app.post("/token",tags=['Default'])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """  
     Route login Access Token Post 
    """
    user = await authenticate_user(form_data.username, form_data.password)
   
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorect ID or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["email"]}, expires_delta=access_token_expires
    )
  
    Users_db.update_one({"email": form_data.username}, {"$set": {
        "last_login": datetime.now().strftime("%m/%d/%y %H:%M:%S"),
        "is_active": "true"
    }})

    return {"access_token": access_token, "token_type": "bearer"}
#-----------------------------------------------------------------------------------------------



#-------------------------Include Admin , Users and Models predictions Routes-------------------                     
#-----------------------------------------------------------------------------------------------
app.include_router(adminRouter,tags=['Admin']) # Admin Routes
app.include_router(usersRouter,tags=['Users']) # Users Routes
app.include_router(predRouter,tags=['Predictions']) # Predictions Routes
#-----------------------------------------------------------------------------------------------

