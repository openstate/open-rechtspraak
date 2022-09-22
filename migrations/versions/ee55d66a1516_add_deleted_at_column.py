"""Add deleted at column

Revision ID: ee55d66a1516
Revises: 24d67ed9a5ec
Create Date: 2022-05-06 12:52:54.813418

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "ee55d66a1516"
down_revision = "24d67ed9a5ec"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "person", sa.Column("removed_from_rechtspraak_at", sa.DateTime(), nullable=True)
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("person", "removed_from_rechtspraak_at")
    # ### end Alembic commands ###