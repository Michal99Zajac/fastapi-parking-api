import uuid

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID  # noqa
from sqlalchemy.orm import MappedColumn, mapped_column


def uuid_column() -> MappedColumn:
    # TODO: use solution belowe along with postgresql
    # return Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # NOTE: Temporarily use less specific approach
    return mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
