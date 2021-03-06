"""add professional detail fk to institution

Revision ID: 6118877635f1
Revises: b8493137763b
Create Date: 2021-02-27 19:04:29.883809

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "6118877635f1"
down_revision = "b8493137763b"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "professional_detail",
        sa.Column("institution_id", postgresql.UUID(as_uuid=True), nullable=True),
    )
    op.create_foreign_key(
        None, "professional_detail", "institution", ["institution_id"], ["id"]
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "professional_detail", type_="foreignkey")
    op.drop_column("professional_detail", "institution_id")
    # ### end Alembic commands ###
