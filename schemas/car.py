from pydantic import BaseModel, Field, model_validator
from typing import Optional


class CarCreate(BaseModel):
    """Schema for creating a new car."""
    user_id: int
    brand: str = Field(..., min_length=2, max_length=50, json_schema_extra={"example": "Mercedes"})
    model: str = Field(..., min_length=1, max_length=50, json_schema_extra={"example": "GLS63"})
    year: int = Field(..., ge=1886, le=2100, json_schema_extra={"example": 2020})
    plate_number: str = Field(..., min_length=1, max_length=10, json_schema_extra={"example": "AA7777AA"})
    vin: str = Field(..., min_length=17, max_length=17, json_schema_extra={"example": "1HGCM82633A123456"})

    @model_validator(mode="before")
    @classmethod
    def validate_vin(cls, values):
        vin = values.get("vin")
        if vin and len(vin) != 17:
            raise ValueError("VIN must be exactly 17 characters long.")
        return values


class CarRead(BaseModel):
    """Schema for reading car details."""
    car_id: int
    user_id: int
    brand: str
    model: str
    year: int
    plate_number: str
    vin: str

    model_config = {"from_attributes": True}


class CarUpdate(BaseModel):
    """Schema for updating car details."""
    brand: Optional[str] = Field(None, min_length=2, max_length=50)
    model: Optional[str] = Field(None, min_length=1, max_length=50)
    year: Optional[int] = Field(None, ge=1886, le=2100)
    plate_number: Optional[str] = Field(None, min_length=1, max_length=10)
    vin: Optional[str] = Field(None, min_length=17, max_length=17)

    @model_validator(mode="before")
    @classmethod
    def validate_vin(cls, values):
        vin = values.get("vin")
        if vin and len(vin) != 17:
            raise ValueError("VIN must be exactly 17 characters long.")
        return values
