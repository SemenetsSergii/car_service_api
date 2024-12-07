from pydantic import BaseModel, EmailStr, Field
from enum import Enum
from typing import Optional


class UserRole(str, Enum):
    ADMIN = "ADMIN"
    CUSTOMER = "CUSTOMER"


class UserCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=50, example="John Doe")
    email: EmailStr = Field(..., example="john.doe@example.com")
    password: str = Field(..., min_length=8, example="SecureP@ssw0rd")
    role: UserRole = Field(default=UserRole.CUSTOMER, example=UserRole.CUSTOMER.value)


class UserRead(BaseModel):
    user_id: int
    name: str
    email: EmailStr
    role: UserRole

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=50)
    email: Optional[EmailStr]
    password: Optional[str] = Field(None, min_length=8)
    role: Optional[UserRole] = Field(None, example=UserRole.CUSTOMER.value)
