from pydantic import BaseModel, Field, model_validator
from enum import Enum
from datetime import date, datetime
from typing import Optional


class MechanicRole(str, Enum):
    ADMIN = "ADMIN"
    MECHANIC = "MECHANIC"


class MechanicCreate(BaseModel):
    """Schema for creating a new mechanic."""
    name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        json_schema_extra={"example": "Jane Doe"}
    )
    birth_date: date = Field(
        ...,
        json_schema_extra={"example": "1985-04-12"}
    )
    login: str = Field(
        ...,
        min_length=4,
        max_length=50,
        json_schema_extra={"example": "jdoe"}
    )
    password: str = Field(
        ...,
        min_length=8,
        json_schema_extra={"example": "SecureP@ss123"}
    )
    role: MechanicRole = Field(
        default=MechanicRole.MECHANIC,
        json_schema_extra={"example": MechanicRole.MECHANIC.value}
    )
    position: str = Field(
        ...,
        min_length=2,
        max_length=100,
        json_schema_extra={"example": "Senior Technician"}
    )

    @model_validator(mode="before")
    @classmethod
    def validate_birth_date(cls, values):
        """Ensure the birth date is valid and in the past."""
        birth_date = values.get("birth_date")
        if isinstance(birth_date, str):
            try:
                birth_date = datetime.strptime(birth_date, "%Y-%m-%d").date()
            except ValueError:
                raise ValueError("Invalid birth date format. Use YYYY-MM-DD.")

        if birth_date >= date.today():
            raise ValueError("Birth date must be in the past.")
        values["birth_date"] = birth_date
        return values


class MechanicRead(BaseModel):
    """Schema for reading mechanic details."""
    mechanic_id: int
    name: str
    birth_date: str
    login: str
    role: MechanicRole
    position: str

    @model_validator(mode="after")
    @classmethod
    def format_birth_date(cls, instance):
        """Format birth date as a string."""
        if isinstance(instance.birth_date, date):
            instance.birth_date = instance.birth_date.strftime("%Y-%m-%d")
        return instance

    model_config = {"from_attributes": True}


class MechanicUpdate(BaseModel):
    """Schema for updating mechanic details."""
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    birth_date: Optional[date]
    login: Optional[str] = Field(None, min_length=4, max_length=50)
    password: Optional[str] = Field(None, min_length=8)
    role: Optional[MechanicRole] = Field(
        None,
        json_schema_extra={"example": MechanicRole.MECHANIC.value}
    )
    position: Optional[str] = Field(None, min_length=2, max_length=100)

    @model_validator(mode="before")
    @classmethod
    def validate_birth_date(cls, values):
        """Ensure the birth date is valid and in the past."""
        birth_date = values.get("birth_date")
        if isinstance(birth_date, str):
            try:
                birth_date = datetime.strptime(birth_date, "%Y-%m-%d").date()
            except ValueError:
                raise ValueError("Invalid birth date format. Use YYYY-MM-DD.")

        if birth_date and birth_date >= date.today():
            raise ValueError("Birth date must be in the past.")
        values["birth_date"] = birth_date
        return values
