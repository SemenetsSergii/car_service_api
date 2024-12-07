from pydantic import BaseModel, Field, validator
from enum import Enum
from datetime import date, datetime
from typing import Optional


class MechanicRole(str, Enum):
    ADMIN = "ADMIN"
    MECHANIC = "MECHANIC"


class MechanicCreate(BaseModel):
    """Schema for creating a new mechanic."""
    name: str = Field(..., min_length=2, max_length=100, example="Jane Doe")
    birth_date: date = Field(..., example="1985-04-12")
    login: str = Field(..., min_length=4, max_length=50, example="jdoe")
    password: str = Field(..., min_length=8, example="SecureP@ss123")
    role: MechanicRole = Field(default=MechanicRole.MECHANIC, example=MechanicRole.MECHANIC.value)
    position: str = Field(..., min_length=2, max_length=100, example="Senior Technician")

    @validator("birth_date", pre=True)
    def validate_birth_date(cls, value):
        if isinstance(value, str):
            try:
                birth_date = datetime.strptime(value, "%Y-%m-%d").date()
                if birth_date >= date.today():
                    raise ValueError("Birth date must be in the past.")
                return birth_date
            except ValueError:
                raise ValueError("Invalid birth date format. Use YYYY-MM-DD.")
        elif isinstance(value, date):
            if value >= date.today():
                raise ValueError("Birth date must be in the past.")
        return value


class MechanicRead(BaseModel):
    """Schema for reading mechanic details."""
    mechanic_id: int
    name: str
    birth_date: str
    login: str
    role: MechanicRole
    position: str

    @validator("birth_date", pre=True)
    def format_birth_date(cls, value):
        if isinstance(value, date):
            return value.strftime("%Y-%m-%d")
        return value

    class Config:
        from_attributes = True


class MechanicUpdate(BaseModel):
    """Schema for updating mechanic details."""
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    birth_date: Optional[date]
    login: Optional[str] = Field(None, min_length=4, max_length=50)
    password: Optional[str] = Field(None, min_length=8)
    role: Optional[MechanicRole] = Field(None, example=MechanicRole.MECHANIC.value)
    position: Optional[str] = Field(None, min_length=2, max_length=100)
