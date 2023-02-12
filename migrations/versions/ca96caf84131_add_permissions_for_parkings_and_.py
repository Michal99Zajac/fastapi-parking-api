"""add permissions for parkings and bookings

Revision ID: ca96caf84131
Revises: c18e73c205d7
Create Date: 2023-02-12 19:20:22.538153

"""
import sqlalchemy as sa
from alembic import op

from src.db.models import Permission, Role

# revision identifiers, used by Alembic.
revision = "ca96caf84131"
down_revision = "c18e73c205d7"
branch_labels = None
depends_on = None

permissions = {
    "booking:read": None,
    "booking:delete": None,
    "booking:update": None,
    "booking:create": None,
}


def upgrade() -> None:
    bind = op.get_bind()
    session = sa.orm.Session(bind=bind)

    # get roles
    admin_role: Role = session.query(Role).filter(Role.name == "admin").first()
    user_role: Role = session.query(Role).filter(Role.name == "user").first()

    # create permissions
    permissions = {
        "booking:read": Permission(name="booking:read"),
        "booking:delete": Permission(name="booking:delete"),
        "booking:update": Permission(name="booking:update"),
        "booking:create": Permission(name="booking:create"),
    }

    # add permissions the admin and user
    admin_role.permissions.extend(permissions.values())
    user_role.permissions.extend(permissions.values())

    # bulk save to permissions
    session.bulk_save_objects(permissions.values())
    session.bulk_save_objects([admin_role, user_role])

    # commit changes
    session.commit()


def downgrade() -> None:
    bind = op.get_bind()
    session = sa.orm.Session(bind=bind)
    statement = sa.delete(Permission).where(Permission.name.in_(permissions.keys()))
    print(statement)
    session.execute(statement)
    session.commit()
