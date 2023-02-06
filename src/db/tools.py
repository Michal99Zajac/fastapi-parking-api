import uuid

from sqlalchemy import UUID
from sqlalchemy.orm import MappedColumn, mapped_column


def uuid_column() -> MappedColumn:
    return mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
