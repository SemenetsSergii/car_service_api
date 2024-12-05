from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    """Schema for creating a new user."""
    name: str
    email: EmailStr
    password: str
    role: str = "customer"


class UserRead(BaseModel):
    """Schema for reading user details."""
    user_id: int
    name: str
    email: EmailStr
    role: str

    class Config:
        orm_mode = True
