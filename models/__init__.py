from sqlalchemy.orm import declarative_base

from models.appointments import Appointment
from models.car import Car
from models.users import Users
from models.documents import Document
from models.mechanics import Mechanic
from models.services import Service


Base = declarative_base()
