from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base
from db.tools import uuid_column


class Parking(Base):
    __tablename__ = "parkings"

    id: Mapped[str] = uuid_column()
    name = Column(String, nullable=False)
    address_id: Mapped[str] = mapped_column(ForeignKey("addresses.id"), nullable=False)
    owner_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)

    # relationships
    address: Mapped["Address"] = relationship()  # type: ignore
    owner: Mapped["User"] = relationship()  # type: ignore
