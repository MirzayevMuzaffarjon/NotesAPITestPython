from pydantic import BaseModel
from typing import Optional, Union

class Data(BaseModel):
    id: str
    name: str
    email: str
    token: str

class SchemaLoginSuccess(BaseModel):
    success: bool
    status: int
    message: str
    data: Data