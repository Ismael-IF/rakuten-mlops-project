from fastapi import (
    APIRouter,
    Depends,
    status,
    HTTPException,
    Response
)
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm
from users.usersModels import (
    UserRegisterSchema,
    UserRegisterSchemaOut,
    UserShowSchema,
    UpdateUserModel,
    DeactivateUserModel  
)
from dependecies.dependecies import (
    get_current_user,
    #authenticate_user,
   # create_access_token,
    get_password_hash
)
from config.settings import ACCESS_TOKEN_EXPIRE_MINUTES
from config.database import Users_db
from typing import List
from datetime import datetime, timedelta
import re


usersRouter = APIRouter()

from pydantic import BaseModel
class Message(BaseModel):
    message: str
# ============= ROUTES=============================================================================================================
@usersRouter.post("/Users/register_user", response_description="User registration",
response_model=UserRegisterSchemaOut)#, responses={201: {"model": Message}})
async def register_user(user: UserRegisterSchema):

    """  
     This route allows to a new  to register
    """
    
    if not Users_db.find_one({'email': user.email.lower()}):

        # Check if Full name example changed
        if  user.full_name == "your Full name":
           raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Please enter a valid Full name')           
        # Check if email example changed
        if user.email =="your@email.com":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Please set your email address')
        # Check if password example changed
        if user.password =="secretpassword":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Please set a different Password')            
        # Check password  match             
        if user.password != user.passwordConfirm:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Passwords do not match')  

        del user.passwordConfirm
        user.email = user.email.lower() 
        user.password = get_password_hash(user.password)
        userDB = jsonable_encoder(user) 
        userDB['role'] = 'user' 
        userDB['is_active'] = 'true'
        userDB['is_verified'] = 'false'  
        userDB['created_at'] = str(datetime.utcnow())
        userDB['updated_at'] =  userDB['created_at']

        new_user = Users_db.insert_one(userDB)
        Users_db.update_one({"_id": new_user.inserted_id}, {
                                    "$rename": {"password": "hashed_pass"}})

        created_user =  Users_db.find_one({"_id": new_user.inserted_id})
       
        return JSONResponse(status_code=status.HTTP_201_CREATED, content='User successfully created')

    raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail='There already exists a user account with this email address')


# ============================================================================================================================================
@usersRouter.get("/Users/Me", response_description="Me", response_model=UserShowSchema)
async def current_user(current_user: UserShowSchema = Depends(get_current_user)):
    """  
     Read current user 
    """
    return current_user

# ============================================================================================================================================
@usersRouter.put("/Users/update_user/{user_email}", response_description="Update a user", response_model=UpdateUserModel)
async def update_user(user_email: str, user: UpdateUserModel, current_user: UserShowSchema = Depends(get_current_user)):
    """  
     Allows to user to update his data
    """

    if current_user["email"] == user_email : 

               # Check if user changed field
                if  user.full_name == "your Full name":
                 raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Please enter a valid Full name')
                if  user.password == "yourNewpassword":
                 raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Please enter a valid Password')                 
                if user.password != user.passwordConfirm:
                 raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Passwords do not match')  

                del user.passwordConfirm
                #user.email = user.email.lower() 
                user.password = get_password_hash(user.password)
                userDB = jsonable_encoder(user) 
                userDB['role'] = 'user' 
                userDB['is_active'] = 'true'
                userDB['is_verified'] = 'false'  
                userDB['updated_at'] = str(datetime.utcnow())
                userDB['hashed_pass'] =userDB['password'] 
                del userDB['password'] 

                updated_result =  Users_db.update_one({"email": user_email}, {"$set": userDB})  # {"$rename": {"password": "hashed_pass"}})                                                                    
                updated_user = Users_db.find_one({"email": user_email})

                return JSONResponse(status_code=status.HTTP_201_CREATED, content='User successfully updated')
            

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Please enter your own email address')
# ============================================================================================================================================
@usersRouter.put("/Users/deactivate_user/{user_email}", response_description="Delete a user")
async def deactivate_user(user_email: str, user:DeactivateUserModel, current_user: UserShowSchema = Depends(get_current_user)):
   """  
     Allows to user to deactivate  his own account
    """
   if current_user["email"] == user_email : 

          if user.is_active != 'false':
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Please enter false if you want to deactivate your own account')
          elif user.is_active == 'false':
            user_deactivate = jsonable_encoder(user)
            deactivate_result =  Users_db.update_one({"email": user_email}, {"$set": user_deactivate})
            return JSONResponse(status_code=status.HTTP_201_CREATED, content='User successfully deactivated')

   raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Please enter your own email address')
# ============================================================================================================================================