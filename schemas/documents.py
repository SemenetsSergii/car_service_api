from pydantic import BaseModel, Field
from typing import Optional


class DocumentCreate(BaseModel):
    """Schema for creating a new document."""
    mechanic_id: int
    type: str = Field(..., example="passport")
    file_path: str


class DocumentRead(BaseModel):
    """Schema for reading document details."""
    document_id: int
    mechanic_id: int
    type: str
    file_path: str

    class Config:
        from_attributes = True


class DocumentUpdate(BaseModel):
    """Schema for updating document details."""
    mechanic_id: Optional[int] = None
    type: Optional[str] = None
    file_path: Optional[str] = None
