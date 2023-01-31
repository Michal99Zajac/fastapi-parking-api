"""add parking permissions

Revision ID: eb6b4e5f1563
Revises: 3bb5d9b0d27b
Create Date: 2023-01-31 22:11:27.992691

"""
from alembic import op
from sqlalchemy import delete, orm

from user.models import Permission, Role

# revision identifiers, used by Alembic.
revision = "eb6b4e5f1563"
down_revision = "3bb5d9b0d27b"
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
