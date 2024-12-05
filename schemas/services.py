from pydantic import BaseModel


class ServiceCreate(BaseModel):
    """Schema for creating a new service."""
    name: str
    description: str
    price: float
    duration: int


class ServiceRead(BaseModel):
    """Schema for reading service details."""
    service_id: int
    name: str
    description: str
    price: float
    duration: int

    class Config:
        orm_mode = True
