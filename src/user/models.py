# pyright: reportUndefinedVariable=false
from __future__ import annotations

from sqlalchemy import Column, ForeignKey, String, Table
from sqlalchemy.orm import Mapped, relationship

from src.db.base import Base

users_roles = Table(
    "users_roles",
    Base.metadata,
    Column(
        "user_id", ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True
    ),
    Column("role_id", ForeignKey("roles.id"), primary_key=True),
)

roles_permissions = Table(
    "roles_permissions",
    Base.metadata,
    Column(
        "role_id", ForeignKey("roles.id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True
    ),
    Column(
        "permission_id",
        ForeignKey("permissions.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
    ),
)


class User(Base):
    __tablename__ = "users"

    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)

    # relationships
    roles: Mapped[list["Role"]] = relationship(
        secondary=users_roles,
        back_populates="users",
        cascade="all, delete",
    )
    parkings: Mapped[list["Parking"]] = relationship(  # type: ignore  # noqa: F821
        back_populates="owner", cascade="all, delete"
    )
    bookings: Mapped[list["Booking"]] = relationship(  # type: ignore  # noqa: F821
        back_populates="booker", cascade="all, delete"
    )


class Role(Base):
    __tablename__ = "roles"

    name = Column(String(100), unique=True, nullable=False)
    description = Column(String(255))

    # relationships
    users: Mapped[list["User"]] = relationship(
        secondary=users_roles,
        back_populates="roles",
    )
    permissions: Mapped[list["Permission"]] = relationship(
        secondary=roles_permissions,
        back_populates="roles",
        cascade="all, delete",
        passive_deletes=True,
    )


class Permission(Base):
    __tablename__ = "permissions"

    name = Column(String(100), unique=True)
    description = Column(String(1000))

    # relationships
    roles: Mapped[list["Role"]] = relationship(
        secondary=roles_permissions,
        back_populates="permissions",
        cascade="all, delete",
        passive_deletes=True,
    )
