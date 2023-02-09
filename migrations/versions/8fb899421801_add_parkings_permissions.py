"""add parkings permissions

Revision ID: 8fb899421801
Revises: 0316d94af553
Create Date: 2023-02-06 23:16:23.655669

"""
import sqlalchemy as sa
from alembic import op

from db.models import Permission, Role

# revision identifiers, used by Alembic.
revision = "8fb899421801"
down_revision = "0316d94af553"
branch_labels = None
depends_on = None

permissions = {
    "parking:read": None,
    "parking:delete": None,
    "parking:update": None,
    "parking:create": None,
}


def upgrade() -> None:
    bind = op.get_bind()
    session = sa.orm.Session(bind=bind)

    # get roles
    admin_role: Role = session.query(Role).filter(Role.name == "admin").first()
    user_role: Role = session.query(Role).filter(Role.name == "user").first()

    # create permissions
    permissions = {
        "parking:read": Permission(name="parking:read"),
        "parking:delete": Permission(name="parking:delete"),
        "parking:update": Permission(name="parking:update"),
        "parking:create": Permission(name="parking:create"),
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
