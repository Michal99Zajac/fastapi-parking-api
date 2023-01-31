from sqlalchemy import Column, String
from sqlalchemy.orm import Mapped, relationship

from db.base import Base
from db.tools import uuid_column


class Address(Base):
    __tablename__ = "addresses"

    id: Mapped[str] = uuid_column()
    street = Column(String(100), nullable=False)
    zip_code = Column(String(20), nullable=False)
    city = Column(String(100), nullable=False)
    country = Column(String(100), nullable=False)

    # relationships
    parking: Mapped["Parking"] = relationship()  # type: ignore
