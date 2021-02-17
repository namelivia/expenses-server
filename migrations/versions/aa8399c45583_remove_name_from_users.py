"""Remove name from users

Revision ID: aa8399c45583
Revises: c1848139ab40
Create Date: 2021-02-17 19:04:56.244566

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "aa8399c45583"
down_revision = "c1848139ab40"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("user_data", schema=None) as batch_op:
        batch_op.drop_column("name")

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("user_data", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("name", sa.VARCHAR(), autoincrement=False, nullable=True)
        )

    # ### end Alembic commands ###