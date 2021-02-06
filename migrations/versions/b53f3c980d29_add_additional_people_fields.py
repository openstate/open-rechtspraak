"""add additional people fields

Revision ID: b53f3c980d29
Revises: 6472e29d7a3b
Create Date: 2021-02-06 15:23:47.451172

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "b53f3c980d29"
down_revision = "6472e29d7a3b"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("people", sa.Column("toon_naam", sa.Text(), nullable=True))
    op.add_column("people", sa.Column("toon_naam_kort", sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("people", "toon_naam_kort")
    op.drop_column("people", "toon_naam")
    # ### end Alembic commands ###