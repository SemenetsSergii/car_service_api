from pydantic import BaseModel
from datetime import datetime


class AppointmentCreate(BaseModel):
    """Schema for creating a new appointment."""
    user_id: int
    car_id: int
    service_id: int
    mechanic_id: int
    appointment_date: datetime
    status: str = "PENDING"


class AppointmentRead(BaseModel):
    """Schema for reading appointment details."""
    appointment_id: int
    user_id: int
    car_id: int
    service_id: int
    mechanic_id: int
    appointment_date: datetime
    status: str

    class Config:
        orm_mode = True
