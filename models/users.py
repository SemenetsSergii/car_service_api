from sqlalchemy import Column, Integer, String, Enum

from db.engine import Base


class Users(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True)
    email = Column(String(50), unique=True, index=True)
    password = Column(String(50), nullable=False)
    role = Column(Enum("admin", "customer"), default="customer", nullable=False)
