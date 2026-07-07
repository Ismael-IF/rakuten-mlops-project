from bson import ObjectId
from pydantic import BaseModel, Field, EmailStr,constr
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

class UserRegisterSchema(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    full_name: Optional[str]
    email:    Optional[EmailStr] 
    password: constr(min_length=4)
    passwordConfirm: str
    
      
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
                        
            }
        }

class UserRegisterSchemaOut(BaseModel):
    full_name: Optional[str]
    email:    Optional[EmailStr] 


class UserShowSchema(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    full_name: Optional[str]
    email:    Optional[EmailStr] 
    role: Optional[str]
    is_active: Optional[str]
    created_at: Optional[str]
    last_login: Optional[str]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "full_name": "your Full name",
                "email": "Doe",
                "role": "user",
                "created_at": "datetime",
                "last_login": "datetime",
            }
        }



class UpdateUserModelOld(BaseModel):
    full_name: Optional[str] 
    email:    Optional[EmailStr]  
    role: Optional[str]
    is_active: Optional[str]
    created_at: Optional[str]
    last_login: Optional[str]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "full_name": "your Full name",
                "email": "your@email.com",
                "role": "user",
                "is_active": "true",
                "created_at": "datetime",
                "last_login": "datetime",
            }
        }

class UpdateUserModel(BaseModel):
    full_name: Optional[str] 
    #email:    EmailStr
    password: constr(min_length=4)
    passwordConfirm: str    
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "full_name": "your Full name",              
                #"email": "your@email.com",
                "password": "yourNewpassword",
                "passwordConfirm": "yourNewpassword",
            }
        }

class DeactivateUserModel(BaseModel):
 # email:    EmailStr
  is_active : str
  
    
  class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
             #"email": "your@email.com",
             'is_active' : 'false'
            }
        }
