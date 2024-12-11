from sqlalchemy import (
    Column,
    Integer,
    String,
    Float
)
from db.engine import Base


class Service(Base):
    __tablename__ = "services"

    service_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    price = Column(Float, nullable=False)
    duration = Column(Integer, nullable=False)
