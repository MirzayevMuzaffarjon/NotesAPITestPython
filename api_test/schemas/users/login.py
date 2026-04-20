from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Union

class Data(BaseModel):
    id: str
    name: str
    email: EmailStr
    token: str = Field(min_length=20, max_length=500)

class SchemaLoginSuccess(BaseModel):
    success: bool
    status: int
    message: str
    data: Data


class SchemaLoginErrorCase(BaseModel):
    success: bool
    status: int
    message: str = Field(min_length=20, max_length=500)