from __future__ import annotations

from sqlalchemy import Column, ForeignKey, String, Table
from sqlalchemy.orm import relationship

from db.base import Base
from db.tools import uuid_column

users_roles = Table(
    "users_roles",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("role_id", ForeignKey("roles.id"), primary_key=True),
)

roles_permissions = Table(
    "roles_permissions",
    Base.metadata,
    Column("role_id", ForeignKey("roles.id")),
    Column("permission_id", ForeignKey("permissions.id")),
)


class User(Base):
    __tablename__ = "users"

    id = uuid_column()
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)

    # relationships
    roles: list[Role] = relationship(
        "Role", secondary=users_roles, back_populates="users", cascade="all, delete"
    )


class Role(Base):
    __tablename__ = "roles"

    id = uuid_column()
    name = Column(String(100), unique=True, nullable=False)
    description = Column(String(255))

    # relationships
    users: list[User] = relationship(
        "User",
        secondary=users_roles,
        back_populates="roles",
    )
    permissions: list[Permission] = relationship(
        "Permission", secondary=roles_permissions, back_populates="roles", cascade="all, delete"
    )


class Permission(Base):
    __tablename__ = "permissions"

    id = uuid_column()
    name = Column(String(100), unique=True)
    description = Column(String(1000))

    # relationships
    roles: list[Role] = relationship(
        "Role", secondary=roles_permissions, back_populates="permissions", cascade="all, delete"
    )
