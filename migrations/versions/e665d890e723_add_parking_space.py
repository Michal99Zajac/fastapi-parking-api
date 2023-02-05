"""add parking space

Revision ID: e665d890e723
Revises: bd3adc9c4e27
Create Date: 2023-02-05 21:59:42.032139

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "e665d890e723"
down_revision = "bd3adc9c4e27"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("parkings", "address_id", existing_type=sa.VARCHAR(), nullable=True)
    op.create_table(
        "parking_spaces",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("parking_id", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(["parking_id"], ["parkings.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("parkings", "address_id", existing_type=sa.VARCHAR(), nullable=False)
    op.drop_table("parking_spaces")
    # ### end Alembic commands ###
