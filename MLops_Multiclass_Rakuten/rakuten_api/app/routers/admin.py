from fastapi import (
    APIRouter,
    Depends,
    Query,
    status,
    HTTPException,
    Response
)
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm
from users.adminModels import (
    AdminCreateUserSchema, 
    AdminShowUserModel,
    AdminUpdateUserModel   
)
from dependecies.dependecies import (
    get_current_user,
    authenticate_user,
    create_access_token,
    get_password_hash
)
from config.settings import ACCESS_TOKEN_EXPIRE_MINUTES
from config.database import Users_db
from pydantic import EmailStr, Required ,SecretStr
from typing import List
from datetime import datetime, timedelta
import re


adminRouter = APIRouter()


# ============= ROUTES=============================================================================================================
@adminRouter.post("/Admin/add_user", response_description="Add new user", response_model=AdminCreateUserSchema)
async def add_user(user: AdminCreateUserSchema,current_user: AdminCreateUserSchema = Depends(get_current_user)):

    """  
     This route allows to add a new user and assign him a role (admin, dev or user) 
    """

    if not current_user["role"] != "admin":  

        if not Users_db.find_one({'email': user.email.lower()}):
        
            if user.role in ["admin", "dev","user"]:
            
                if user.is_active in ["true", "false"]:

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
                    user.created_at = datetime.utcnow()
                    user.updated_at =  user.created_at
                    user.password = get_password_hash(user.password)
                    user = jsonable_encoder(user)    
                    new_user = Users_db.insert_one(user)
                    Users_db.update_one({"_id": new_user.inserted_id}, {
                                                "$rename": {"password": "hashed_pass"}})

                    created_user =  Users_db.find_one({"_id": new_user.inserted_id})
                    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_user)

                raise HTTPException(status_code=406, detail="User is_active field not acceptable. Valide states true or false ")

            raise HTTPException(status_code=406, detail="User role not acceptable. Valide roles are admin, dev or user. ")

        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail='There already exists a user account with this email address')

    raise HTTPException(status_code=403, detail=f"Not having sufficient rights to access this resource") 

# ============================================================================================================================================
@adminRouter.get("/Admin/current", response_description="Current User", response_model=AdminShowUserModel)
async def current_user(current_user: AdminShowUserModel = Depends(get_current_user)):
    """  
     Read current user  
    """
    if not current_user["role"] != "admin":
     return current_user
    raise HTTPException(status_code=403, detail=f"Not having sufficient rights to access this resource")



# ============================================================================================================================================
@adminRouter.get("/Admin/list_users/", response_description="List of n users", response_model=List[AdminShowUserModel])
async def list_users(nbr_of_users:int = Query(default=100 , alias="Number of users",
                                  description="Desired number of users "),
                    users_states : str = Query(default='All', enum = ['All','Is Active','Is Not Active'],
                                    description="Users activity state", alias="Users activity state"),
                                    current_user: AdminCreateUserSchema = Depends(get_current_user)):
   """  
     Allows to display users registered users in the database. The user can choose the desired number of users to display and their status
   """

   if not current_user["role"] != "admin":
        if  nbr_of_users > 0:
         try:
                if users_states in ['All', None]:
                    myquery = {}
                else:
                    if  users_states == 'Is Active':
                        myquery = { "is_active": 'true' }

                    elif users_states == 'Is Not Active':
                        myquery = { "is_active": 'false' }
                
                users = Users_db.find(myquery).limit(nbr_of_users)                
                user_list = list(users)
                return JSONResponse(user_list)  # All filed 
   
         except Exception:
           raise HTTPException(status_code=404, detail="Error occurred while Trying to Access the Requested Resource")
            
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Please enter a valid number of users')

   raise HTTPException(status_code=403, detail=f"Not having sufficient rights to access this resource")


@adminRouter.put("/Admin/update_user/{user_email}", response_description="Update a user")
 #response_model=AdminCreateUserSchema)
async def update_user(user_email: EmailStr, user: AdminUpdateUserModel, current_user: AdminCreateUserSchema = Depends(get_current_user)):

    """  
     Allows to update user informations of a given user 
    """
    
    if not current_user["role"] != "admin":

        if  Users_db.find_one({'email': user_email.lower()}):         
              
                if  user.full_name == "your Full name":
                 raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Please enter a valid Full name')
                if  user.password == "yourNewpassword":
                 raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Please enter a valid Password')                 
                if user.password != user.passwordConfirm:
                 raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Passwords do not match')  
                if  user.role not in ["admin","dev","user"]:
                 raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Please enter valid a role') 
                if  user.is_active not in ["true","false"]:
                 raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Please enter valid activity state')  
        
                
                del user.passwordConfirm
                user.password = get_password_hash( user.password)
                user.updated_at = datetime.utcnow()             
             
                user_update = jsonable_encoder(user)
                user_update['hashed_pass'] =user_update['password'] 
                del user_update['password'] 
           
                updated_result =  Users_db.update_one({"email": user_email}, {"$set": user_update})   # {"$rename": {"password": "hashed_pass"}})                                                                 
                updated_user = Users_db.find_one({"email": user_email})

                return JSONResponse(status_code=status.HTTP_201_CREATED, content=updated_user)

        raise HTTPException(status_code=404, detail=f"User {user_email} not found")

    raise HTTPException(status_code=403, detail=f"Not having sufficient rights to access this resource")



# ============================================================================================================================================
@adminRouter.delete("/Admin/delete_user/{user_email}", response_description="Delete a user")
async def delete_user(user_email: EmailStr, current_user: AdminCreateUserSchema = Depends(get_current_user)):
    """  
     Allows to delete a given user from data base
    """
    if current_user["role"] == "admin":
      
        delete_result =  Users_db.delete_one({"email": user_email})

        if delete_result.deleted_count == 1:
            return Response(status_code=status.HTTP_204_NO_CONTENT, content=None)

        raise HTTPException(status_code=404, detail=f"User: {user_email} not found")
    
    else:
        raise HTTPException(status_code=403, detail=f"Not having sufficient rights to access this resource")
# ============================================================================================================================================