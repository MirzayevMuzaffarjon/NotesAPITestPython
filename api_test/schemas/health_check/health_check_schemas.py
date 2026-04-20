from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Union

class SchemaHealthCheck(BaseModel):
    success: bool
    status: int
    message: str = Field(min_length=20, max_length=500)