import enum

from sqlalchemy import Column, Integer, ForeignKey, DateTime, Enum
from db.engine import Base


class AppointmentStatus(enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELED = "canceled"


class Appointment(Base):
    __tablename__ = "appointments"

    appointment_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    car_id = Column(Integer, ForeignKey("cars.car_id"), nullable=False)
    service_id = Column(Integer, ForeignKey("services.service_id"), nullable=False)
    mechanic_id = Column(Integer, ForeignKey("mechanics.mechanic_id"), nullable=True)
    appointment_date = Column(DateTime, nullable=False)
    status = Column(Enum(AppointmentStatus), default=AppointmentStatus.PENDING, nullable=False)
