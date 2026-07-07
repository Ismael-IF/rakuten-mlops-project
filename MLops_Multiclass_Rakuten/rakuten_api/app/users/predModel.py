from bson import ObjectId
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Union, List


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

class predUserModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    full_name: str
    email: EmailStr #username
    password: str
    role : str
    is_active : str
    created_at: Optional[str] = None
    last_login: str

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "full_name": "your Full name",              
                "email": "your@email.com",
                "password": "secretpassword",
                "role": "user",
                "is_active" : "true", 
                "created_at": "datetime",
                "last_login": "datetime",
                
            }
        }


# Define the response JSON
class TextPrediction(BaseModel):
    designation_text: str
    description_text: Union[str, None] = None  # Description filed Optional    
    predicted_class : int
    predicted_label : str
    precision : str

# Define the response JSON for predictions based on text

class TextInput(BaseModel):
    designation_text: str    # Designation filed Required    
    description_text: Union[str, None] = None  # Description filed Optional
   

# Define the response JSON for predictions based on images
class ImagePrediction(BaseModel):
    filename: str
    content_type: str    
    predicted_class : int
    predicted_label : str
    precision : str


class MultiModalPrediction(BaseModel):

    designation_txt: str
    description_text: Union[str, None] = None  # Description filed Optional
    image_filename: str
    content_type: str     
    #  
    predicted_class : int
    predicted_label : str
    precision : str

    predicted_class_text_Model1 : int
    predicted_label_text_Model1 : str
    precision_text_Model1 : str

    predicted_class_text_Model2 : int
    predicted_label_text_Model2 : str
    precision_text_Model2 : str

    predicted_class_image_model : int
    predicted_label_image_model : str
    precision_image_model : str
