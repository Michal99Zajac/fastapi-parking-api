from sqlalchemy import Column, ForeignKey, Integer, String

from db.base import Base


class Parking(Base):
    __tablename__ = "parkings"

    id = Column(String, primary_key=True, unique=True)
    name = Column(String, nullable=False)
