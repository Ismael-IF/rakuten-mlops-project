from pymongo import mongo_client


from datetime import datetime, timedelta
from pydantic import BaseModel, Field, EmailStr ,constr
from bson import ObjectId
from typing import Optional
#from config.database import Users_db



from fastapi.encoders import jsonable_encoder

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


########################################Connect to data end#############################################    

# # List Databases
# dblist = client.list_database_names()
# if "rakuten_db" in dblist:
#   print("The database exists.")

#   collection = db.rakuten_users
  

# Creating a Admin User class
class CreateUserSchema(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    full_name: str
    email: str #username   
    password: str  
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

##### Add Admin #1============================================================================
created_at = datetime.utcnow()
updated_at =  created_at


def initialse_db (Users_db):

##### Add Admin #1============================================================================
    new_user_1 = CreateUserSchema(

    # id = Field(default_factory=PyObjectId, alias="_id"),
        full_name= 'Administrator',
        email= 'admin_account1@example.com',
        password= '$2b$12$sy2Kg./oIoFnGBB3Jpe/9.OLAwcgZ39X9AYEAj8DAIF8f4E34Z2iS',
        role = 'admin',
        is_active = 'true',
        created_at= datetime.utcnow(),
        updated_at=  datetime.utcnow(),
        is_verified= False,
        last_login= None

        )
    try:
        user_db_1 = jsonable_encoder(new_user_1)    
        new_user_db_1 = Users_db.insert_one(user_db_1)
        Users_db.update_one({"_id": new_user_db_1.inserted_id}, {"$rename": {"password": "hashed_pass"}})
        created_user =  Users_db.find_one({"_id": new_user_db_1.inserted_id})

    except Exception:
            pass

    #============================================================================================



    # Add user #2================================================================================
    new_user_2 = CreateUserSchema (
        full_name= 'Alice Wonderson',
        email = 'alicewonderson@example.com',
        password = '$2b$12$UbQb.M.BZQqHuoI2qYFwbeT3B4G6.9WVdkVhHj7gOpds0n4ttiVri',   
        role = 'user' ,
        is_active = 'true',
        created_at= datetime.utcnow(),
        updated_at=  datetime.utcnow(),
        is_verified= False,
        last_login= None
    )
    try:
        user_db_2 = jsonable_encoder(new_user_2)    
        new_user_db_2 = Users_db.insert_one(user_db_2)
        Users_db.update_one({"_id": new_user_db_2.inserted_id}, {"$rename": {"password": "hashed_pass"}})
        created_user =  Users_db.find_one({"_id": new_user_db_2.inserted_id})
    except Exception:
           pass
    #print("User #2 inserted with record ids \n ",created_user)
    #============================================================================================

    # Add user #3=================================================================================
    new_user_3 = CreateUserSchema (
        full_name= 'John Doe',
        email = 'johndoe@example.com',
        password = '$2b$12$DCK0M3l7U9gi1JrPr.FenO6CsKJ1sL02wG17QWx0RXzAI.aG5h7ri',   
        role = 'user' ,
        is_active = 'true',
        created_at= datetime.utcnow(),
        updated_at=  datetime.utcnow(),
        is_verified= False,
        last_login= None
    )
    try:
        user_db_3 = jsonable_encoder(new_user_3)    
        new_user_db_3 = Users_db.insert_one(user_db_3)
        Users_db.update_one({"_id": new_user_db_3.inserted_id}, {"$rename": {"password": "hashed_pass"}})
        created_user =  Users_db.find_one({"_id": new_user_db_3.inserted_id})
    except Exception:
           pass
    #print("User #2 inserted with record ids \n ",created_user)
    #============================================================================================

    # Add user #4=================================================================================
    new_user_4 = CreateUserSchema (
        full_name= 'Clementine Mandarine',
        email = 'clementinemandarine@example.com',
        password = '$2b$12$ttMgcORj/PsDOwLSciW4Gu5UkaFkfNW37n3oi6ptgpP0MARROU5ra',   
        role = 'user' ,
        is_active = 'true',
        created_at= datetime.utcnow(),
        updated_at=  datetime.utcnow(),
        is_verified= False,
        last_login= None
    )
    try:
        user_db_4 = jsonable_encoder(new_user_4)    
        new_user_db_4 = Users_db.insert_one(user_db_4)
        Users_db.update_one({"_id": new_user_db_4.inserted_id}, {"$rename": {"password": "hashed_pass"}})
        created_user =  Users_db.find_one({"_id": new_user_db_4.inserted_id})
    except Exception:
           pass
    #print("User #2 inserted with record ids \n ",created_user)
    #============================================================================================