from sqlalchemy import Column, Integer, String, ForeignKey
from db.engine import Base


class Document(Base):
    __tablename__ = "documents"

    document_id = Column(Integer, primary_key=True, index=True)
    mechanic_id = Column(Integer, ForeignKey("mechanics.mechanic_id"), nullable=False)
    type = Column(String(50), nullable=False)
    file_path = Column(String(255), nullable=False)
