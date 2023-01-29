"""add parking permissions

Revision ID: ce83c838aa1c
Revises: 79078ab5d369
Create Date: 2023-01-29 10:32:50.536481

"""
from alembic import op
import sqlalchemy as sa
from user.models import Role, Permission
from sqlalchemy import orm, delete


# revision identifiers, used by Alembic.
revision = "ce83c838aa1c"
down_revision = "79078ab5d369"
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
    session = orm.Session(bind=bind)

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
    session = orm.Session(bind=bind)
    statement = delete(Permission).where(Permission.name.in_(permissions.keys()))
    print(statement)
    session.execute(statement)
    session.commit()
