from pydantic import BaseModel


class DocumentCreate(BaseModel):
    """Schema for creating a new document."""
    mechanic_id: int
    type: str
    file_path: str


class DocumentRead(BaseModel):
    """Schema for reading document details."""
    document_id: int
    mechanic_id: int
    type: str
    file_path: str

    class Config:
        orm_mode = True
