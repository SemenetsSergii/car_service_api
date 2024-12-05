from sqlalchemy import Column, Integer, String, ForeignKey
from db.engine import Base


class Document(Base):
    __tablename__ = "documents"

    document_id = Column(Integer, primary_key=True, index=True)
    mechanic_id = Column(Integer, ForeignKey("mechanics.mechanic_id"), nullable=False)
    type = Column(String, nullable=False)  # For example, passport, personal identification number, diploma, contract
    file_path = Column(String, nullable=False)  # Road to file
