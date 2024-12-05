from sqlalchemy import Column, Integer, String, ForeignKey
from db.engine import Base


class Car(Base):
    __tablename__ = "cars"

    car_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    brand = Column(String(50), nullable=False)
    model = Column(String(50), nullable=False)
    year = Column(Integer, nullable=False)
    plate_number = Column(String(), nullable=False)
    vin = Column(String(17), unique=True, nullable=False)
