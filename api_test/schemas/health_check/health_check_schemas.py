from pydantic import BaseModel, Field


class SchemaHealthCheck(BaseModel):
    """Health check response schema."""
    success: bool
    status: int
    message: str = Field(min_length=1)