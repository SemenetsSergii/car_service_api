from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, model_validator
from datetime import datetime, timezone


class AppointmentStatus(str, Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    CANCELED = "CANCELED"


class AppointmentCreate(BaseModel):
    user_id: int
    car_id: int
    service_id: int
    mechanic_id: int
    appointment_date: str = Field(..., json_schema_extra={"example": "2024-12-10T10:00:00.000Z"})
    status: str = Field(..., json_schema_extra={"example": "PENDING"})

    @model_validator(mode="before")
    @classmethod
    def validate_date(cls, values):
        """Ensure the appointment date is not in the past."""
        appointment_date = values.get("appointment_date")
        if appointment_date:
            try:
                appointment_date_obj = datetime.fromisoformat(appointment_date.replace("Z", "+00:00"))
            except ValueError:
                raise ValueError("Invalid date format. Use ISO 8601 format, e.g., '2024-12-10T10:00:00.000Z'.")

            if appointment_date_obj <= datetime.now(timezone.utc):
                raise ValueError("Appointment date must be in the future.")

        return values


class AppointmentRead(BaseModel):
    """Schema for reading appointment details."""
    appointment_id: int
    user_id: int
    car_id: int
    service_id: int
    mechanic_id: Optional[int]
    appointment_date: datetime
    status: AppointmentStatus

    model_config = {"from_attributes": True}


class AppointmentUpdate(BaseModel):
    """Schema for updating an appointment."""
    user_id: Optional[int] = None
    car_id: Optional[int] = None
    service_id: Optional[int] = None
    mechanic_id: Optional[int] = None
    appointment_date: Optional[datetime] = None
    status: Optional[AppointmentStatus] = None

    @model_validator(mode="before")
    @classmethod
    def validate_date(cls, values):
        appointment_date = values.get("appointment_date")
        if appointment_date and appointment_date <= datetime.now():
            raise ValueError("Appointment date must be in the future.")
        return values
