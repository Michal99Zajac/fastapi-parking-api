from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base
from db.tools import uuid_column


class ParkingAddress(Base):
    __tablename__ = "parking_addresses"

    id: Mapped[str] = uuid_column()
    street = Column(String(100), nullable=False)
    zip_code = Column(String(20), nullable=False)
    city = Column(String(100), nullable=False)
    country = Column(String(100), nullable=False)

    # relationships
    parkings: Mapped[list["Parking"]] = relationship("Parking", back_populates="address")


class Parking(Base):
    __tablename__ = "parkings"

    id: Mapped[str] = uuid_column()
    name = Column(String, nullable=False)
    address_id: Mapped[str] = mapped_column(ForeignKey("parking_addresses.id", ondelete="SET NULL"))
    owner_id: Mapped[str] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    # relationships
    address: Mapped["ParkingAddress"] = relationship("ParkingAddress", back_populates="parkings")
    owner: Mapped["User"] = relationship("User", back_populates="parkings")  # type: ignore
