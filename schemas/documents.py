from pydantic import BaseModel, Field
from typing import Optional


class DocumentCreate(BaseModel):
    """Schema for creating a new document."""
    mechanic_id: int
    type: str = Field(..., json_schema_extra={"example": "passport"})
    file_path: str = Field(
        ..., json_schema_extra={"example": "/path/to/file.pdf"}
    )


class DocumentRead(BaseModel):
    """Schema for reading document details."""
    document_id: int
    mechanic_id: int
    type: str
    file_path: str

    model_config = {"from_attributes": True}


class DocumentUpdate(BaseModel):
    """Schema for updating document details."""
    mechanic_id: Optional[int] = Field(
        None,
        json_schema_extra={"example": 1}
    )
    type: Optional[str] = Field(
        None,
        json_schema_extra={"example": "passport"}
    )
    file_path: Optional[str] = Field(
        None,
        json_schema_extra={"example": "/path/to/new/file.pdf"}
    )
