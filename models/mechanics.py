from sqlalchemy import Column, Integer, String, Date, Enum
from db.engine import Base


class Mechanic(Base):
    __tablename__ = "mechanics"

    mechanic_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    birth_date = Column(Date, nullable=False)
    login = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum("admin", "mechanic"), default="mechanic", nullable=False)
    position = Column(String, nullable=False)
