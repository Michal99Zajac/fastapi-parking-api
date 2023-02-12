from sqlalchemy.orm import DeclarativeBase

from src.db.tools import uuid_column


class Base(DeclarativeBase):
    id = uuid_column()
