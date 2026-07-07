from bson import ObjectId
from pydantic import BaseModel, Field, EmailStr ,constr
from typing import Optional
from datetime import datetime

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")



class AdminCreateUserSchema(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    full_name: str
    email: EmailStr #username   
    password: constr(min_length=4)
    passwordConfirm: str
    role : str
    is_active : str
    created_at:  Optional[datetime] = None
    updated_at:  Optional[datetime] = None
    is_verified: Optional[bool]   = False
    last_login:  Optional[datetime] = None
    

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "full_name": "your Full name",              
                "email": "your@email.com",
                "password": "secretpassword",
                "passwordConfirm": "secretpassword",
                "role": "user",
                "is_active" : "true", 
                
            }
        }

class AdminUserResponseSchema(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    full_name: str
    email: EmailStr #username
    password: str
    role : str
    is_active : str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    is_verified: Optional[bool]   = False
    last_login: Optional[datetime] = None
    

class AdminShowUserModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    full_name: Optional[str]
    email:    Optional[str]
    role: Optional[str]
    is_active: Optional[str] 
    created_at: Optional[str]
    updated_at: Optional[str]
    #last_login: Optional[str]
   
    class Config:     
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
#         schema_extra = {
#             "example": {
#                 "full_name": "your Full name",
#                 "email": "email@example.com",
#                 "created_at": "datetime",          
#                 "updated_at": "datetime",
#                  "role": "user",
#                 "is_active":"true"              
# ,
#             }
    #    }

class AdminUpdateUserModel(BaseModel):
    full_name: Optional[str] 
    email:    Optional[EmailStr]  
    role: Optional[str]
    is_active: Optional[str]
    created_at: Optional[str]
    updated_at: Optional[str]
    last_login: Optional[str]
    

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "full_name": "",
                "email": "",
                "role": "user",
                "is_active": "true"
            }
        }



class AdminUpdateUserModel(BaseModel):

    full_name: Optional[str]  
    password: Optional[constr(min_length=4)]
    passwordConfirm: Optional[str]
    role : Optional[str]
    is_active : Optional[str]
    updated_at: Optional[datetime] = None
 
  
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "full_name": "your Full name",            
                 "password": "yourNewpassword",
                 "passwordConfirm": "yourNewpassword",           
                 "role": "admin , dev or user",
                 "is_active": "true or false"
            }
        }
