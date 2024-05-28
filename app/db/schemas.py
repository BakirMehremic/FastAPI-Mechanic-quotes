from pydantic import BaseModel, StringConstraints, ConfigDict
from typing import Optional, Annotated
from .models import QuoteStatus, AdminPermissions
from datetime import datetime

"""
    The pydantic models for requests are defined in this file
"""


class CreateUserRequest(BaseModel):
    username: Annotated[str, StringConstraints(max_length=50, min_length=5)]
    password: str
    name: Annotated[str, StringConstraints(max_length=50, min_length=5)]
    contact_number: Optional[int]

    # example request data, visible in swagger
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "username": "exampleusername",
                    "password": "your password",
                    "name": "john doe",
                    "contact_number": 387123,
                }
            ]
        }
    }


class CreateMechanicRequest(BaseModel):
    username: Annotated[str, StringConstraints(max_length=50, min_length=5)]
    password: str
    workshop: str | None = None  # same purpose as Optional[str]
    contact_number: int 
    address: str | None = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "username": "exampleusername",
                    "password": "your password",
                    "workshop": "some workshop name",
                    "address": "Street 123",
                    "contact_number": 387123,
                }
            ]
        }
    }


class ViewMechanic(BaseModel):
    username: str
    workshop: str | None = None  
    contact_number: int 
    address: str | None = None

    # orm_mode is deprecated
    model_config = ConfigDict(from_attributes=True)
    

class ViewUser(BaseModel):
    username: str 
    name: str 
    contact_number: int | None=None

    model_config = ConfigDict(from_attributes=True)


class NewRequest(BaseModel):
    mechanic_id: int 
    car: Annotated[str, StringConstraints(max_length=100)]
    description: str | None = None
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "user_id": 1,
                    "mechanic_id": 2,
                    "car": "BMW 535d",
                    "description": "Oil leak"
                }
            ]
        }
    }


class Token(BaseModel):
    access_token: str
    token_type: str 


class NewQuote(BaseModel):
    request_id: int
    amount: float 
    description: str | None = None


class AcceptOrDecline(BaseModel):
    quote_id: int 
    status: QuoteStatus


class ViewQuote(BaseModel):
    quote_id: int 
    request_id: int 
    amount: float 
    description: str | None=None
    status: str 
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ViewRequest(BaseModel):
    request_id: int 
    user_id: int 
    mechanic_id: int 
    car: str 
    description: Optional[str]
    created_at: datetime 

    model_config = ConfigDict(from_attributes=True)


class EditUser(BaseModel):
    name: Annotated[str, StringConstraints(max_length=50, min_length=5)]
    contact_number: int | None = None


class EditMechanic(BaseModel):
    workshop: str | None = None
    contact_number : int | None = None
    address: str | None = None


class CreateAdmin(BaseModel):
    username: str 
    password: str 
    permissions: AdminPermissions

