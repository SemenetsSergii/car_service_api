from pydantic import BaseModel, Field, model_validator
from enum import Enum
from datetime import date, datetime
from typing import Optional


class MechanicRole(str, Enum):
    ADMIN = "ADMIN"
    MECHANIC = "MECHANIC"


def validate_birth_date(value: date) -> date:
    """Validates that the birth date is in the past and properly formatted."""
    if isinstance(value, str):
        try:
            value = datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Invalid birth date format. Use YYYY-MM-DD.")
    if value >= date.today():
        raise ValueError("Birth date must be in the past.")
    return value


class MechanicBase(BaseModel):
    """Base class for mechanic schemas. Contains shared fields and validation logic."""
    name: Optional[str] = Field(
        None,
        min_length=2,
        max_length=100,
        json_schema_extra={"example": "Jane Doe"}
    )
    birth_date: Optional[date] = Field(
        None,
        json_schema_extra={"example": "1985-04-12"}
    )
    login: Optional[str] = Field(
        None,
        min_length=4,
        max_length=50,
        json_schema_extra={"example": "jdoe"}
    )
    password: Optional[str] = Field(
        None,
        min_length=8,
        json_schema_extra={"example": "SecureP@ss123"}
    )
    role: Optional[MechanicRole] = Field(
        default=MechanicRole.MECHANIC,
        json_schema_extra={"example": MechanicRole.MECHANIC.value}
    )
    position: Optional[str] = Field(
        None,
        min_length=2,
        max_length=100,
        json_schema_extra={"example": "Senior Technician"}
    )

    @model_validator(mode="before")
    @classmethod
    def validate_birth_date_field(cls, values):
        """Ensures that the `birth_date` field is valid and in the past."""
        if "birth_date" in values and values["birth_date"] is not None:
            values["birth_date"] = validate_birth_date(values["birth_date"])
        return values


class MechanicCreate(MechanicBase):
    """Schema for creating a new mechanic."""
    name: str
    birth_date: date
    login: str
    password: str
    position: str


class MechanicRead(BaseModel):
    """Schema for reading mechanic details."""
    mechanic_id: int
    name: str
    birth_date: date
    login: str
    role: MechanicRole
    position: str

    @model_validator(mode="after")
    @classmethod
    def format_birth_date(cls, instance):
        """Formats the `birth_date` field as a string in the format YYYY-MM-DD."""
        if isinstance(instance.birth_date, date):
            instance.birth_date = instance.birth_date.strftime("%Y-%m-%d")
        return instance

    model_config = {"from_attributes": True}


class MechanicUpdate(MechanicBase):
    """Schema for updating mechanic details."""
    pass
