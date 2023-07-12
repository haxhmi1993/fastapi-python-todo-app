"""Create column,constraint in todo

Revision ID: 204511b9aee6
Revises: 9b3c5c34e6c2
Create Date: 2023-07-12 18:33:12.353958

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '204511b9aee6'
down_revision = '9b3c5c34e6c2'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('todos', sa.Column('owner_id', sa.Integer(), nullable=True))
    op.create_foreign_key('users_todos_fk', source_table="todos", referent_table="users",
                          local_cols=["owner_id"], remote_cols=["id"], ondelete="CASCADE")


def downgrade():
    op.drop_constraint("users_todos_fk", table_name="todos")
    op.drop_column("todos", "owner_id")
