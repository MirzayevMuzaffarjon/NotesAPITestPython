from pydantic import BaseModel, EmailStr, Field


class LoginData(BaseModel):
    """Login response data model."""
    id: str
    name: str
    email: EmailStr
    token: str = Field(min_length=20, max_length=500)


class SchemaLoginSuccess(BaseModel):
    """Successful login response schema."""
    success: bool
    status: int
    message: str
    data: LoginData


class SchemaLoginErrorCase(BaseModel):
    """Error case login response schema."""
    success: bool
    status: int
    message: str = Field(min_length=20, max_length=500)