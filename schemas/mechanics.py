from pydantic import BaseModel


class MechanicCreate(BaseModel):
    """Schema for creating a new mechanic."""
    name: str
    birth_date: str
    login: str
    password: str
    role: str = "mechanic"
    position: str


class MechanicRead(BaseModel):
    """Schema for reading mechanic details."""
    mechanic_id: int
    name: str
    birth_date: str
    login: str
    role: str
    position: str

    class Config:
        orm_mode = True
