from sqlalchemy import Column, Integer, String, Date, Enum
from db.engine import Base
from enum import Enum as PyEnum


class MechanicRole(PyEnum):
    ADMIN = "ADMIN"
    MECHANIC = "MECHANIC"


class Mechanic(Base):
    __tablename__ = "mechanics"

    mechanic_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    birth_date = Column(Date, nullable=False)
    login = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(Enum(MechanicRole), nullable=False, default=MechanicRole.MECHANIC)
    position = Column(String(100), nullable=False)
