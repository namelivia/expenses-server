"""Initial migration

Revision ID: 3bd3d43e9ffc
Revises: 
Create Date: 2021-02-04 17:08:38.974513

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "3bd3d43e9ffc"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "expenses",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("value", sa.Integer(), nullable=False),
        sa.Column("user", sa.String(), nullable=True),
        sa.Column("category", sa.String(), nullable=True),
        sa.Column("group", sa.String(), nullable=True),
        sa.Column(
            "date",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("expenses", schema=None) as batch_op:
        batch_op.create_index(batch_op.f("ix_expenses_id"), ["id"], unique=False)

    op.create_table(
        "user_data",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column("group", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("user_data", schema=None) as batch_op:
        batch_op.create_index(batch_op.f("ix_user_data_id"), ["id"], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("user_data", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_user_data_id"))

    op.drop_table("user_data")
    with op.batch_alter_table("expenses", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_expenses_id"))

    op.drop_table("expenses")
    # ### end Alembic commands ###