from pydantic import BaseModel


class CarCreate(BaseModel):
    """Schema for creating a new car."""
    user_id: int
    brand: str
    model: str
    year: int
    plate_number: str
    vin: str


class CarRead(BaseModel):
    """Schema for reading car details."""
    car_id: int
    user_id: int
    brand: str
    model: str
    year: int
    plate_number: str
    vin: str

    class Config:
        orm_mode = True
