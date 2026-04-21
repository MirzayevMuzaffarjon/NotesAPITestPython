from pydantic import BaseModel, EmailStr


class RegisterData(BaseModel):
    """Register response data model."""
    id: str
    name: str
    email: EmailStr


class SchemaRegisterSuccess(BaseModel):
    """Successful registration response schema."""
    success: bool
    status: int
    message: str
    data: RegisterData


class SchemaRegisterErrorCase(BaseModel):
    """Error case registration response schema."""
    success: bool
    status: int
    message: str
