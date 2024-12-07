from sqlalchemy import Column, Integer, String, Enum
from db.engine import Base
from enum import Enum as PyEnum


class UserRole(PyEnum):
    ADMIN = "ADMIN"
    CUSTOMER = "CUSTOMER"


class Users(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole, native_enum=False), default=UserRole.CUSTOMER, nullable=False)

