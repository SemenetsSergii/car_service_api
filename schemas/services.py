from pydantic import BaseModel, Field
from typing import Optional


class ServiceCreate(BaseModel):
    """Schema for creating a new service."""
    name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        json_schema_extra={"example": "Oil Change"}
    )
    description: Optional[str] = Field(
        None,
        max_length=255,
        json_schema_extra={
            "example": "Engine oil change and filter replacement."
        }
    )
    price: float = Field(..., gt=0, json_schema_extra={"example": 50.0})
    duration: int = Field(..., gt=0, json_schema_extra={"example": 60})


class ServiceRead(BaseModel):
    """Schema for reading service details."""
    service_id: int
    name: str
    description: Optional[str]
    price: float
    duration: int

    model_config = {"from_attributes": True}


class ServiceUpdate(BaseModel):
    """Schema for updating service details."""
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    description: Optional[str] = Field(None, max_length=255)
    price: Optional[float] = Field(None, gt=0)
    duration: Optional[int] = Field(None, gt=0)
