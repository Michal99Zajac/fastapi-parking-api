from sqlalchemy import Column, String, Table, ForeignKey
from sqlalchemy.orm import relationship

from db.base import Base

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

    id = Column(String, primary_key=True, unique=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    # relationships
    roles = relationship("Role", secondary=users_roles)


class Role(Base):
    __tablename__ = "roles"

    id = Column(String, primary_key=True, unique=True)
    name = Column(String, unique=True, nullable=False)

    # relationships
    permissions = relationship("Permission", secondary=roles_permissions)


class Permission(Base):
    __tablename__ = "permissions"

    id = Column(String, primary_key=True, unique=True)
    name = Column(String, unique=True)
