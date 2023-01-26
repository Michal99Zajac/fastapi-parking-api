import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID


def uuid_column():
    # TODO: use solution belowe along with postgresql
    # return Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # NOTE: Temporarily use less specific approach
    return Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
