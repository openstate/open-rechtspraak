"""Add professional details

Revision ID: 9608dea2653e
Revises: f2e19ac382a2
Create Date: 2021-02-06 19:04:18.277334

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "9608dea2653e"
down_revision = "f2e19ac382a2"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "professional_details",
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("start_date", sa.DateTime(), nullable=True),
        sa.Column("end_date", sa.DateTime(), nullable=True),
        sa.Column("main_job", sa.Boolean(), nullable=True),
        sa.Column("function", sa.Text(), nullable=False),
        sa.Column("historical", sa.Boolean(), nullable=True),
        sa.Column("remarks", sa.Text(), nullable=True),
        sa.Column("person_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["person_id"],
            ["people.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("professional_details")
    # ### end Alembic commands ###
