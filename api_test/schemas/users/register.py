from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class Data(BaseModel):
    id: str
    name: str
    email: EmailStr


class SchemaRegisterSuccess(BaseModel):
    success: bool
    status: int
    message: str
    data: Data


class SchemaRegisterErrorCase(BaseModel):
    success: bool
    status: int
    message: str = Field(min_length=10, max_length=500)
