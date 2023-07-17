"""create table todo

Revision ID: 55af536711b1
Revises: 
Create Date: 2023-07-12 17:31:27.979789

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '55af536711b1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('todos',
                    sa.Column('id', sa.Integer(),
                              nullable=False, primary_key=True, index=True),
                    sa.Column('title', sa.String(length=255), nullable=False),
                    sa.Column('description', sa.String(
                        length=255), nullable=False),
                    sa.Column('priority', sa.Integer(), nullable=False),
                    sa.Column('complete', sa.Boolean(), nullable=False))


def downgrade() -> None:
    op.drop_table('todos')
