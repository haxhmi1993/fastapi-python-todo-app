"""Create Channel table

Revision ID: f6752b58d784
Revises: 204511b9aee6
Create Date: 2023-07-21 14:47:57.281743

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f6752b58d784'
down_revision = '204511b9aee6'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('channels',
                    sa.Column('id', sa.Integer(), nullable=False,
                              primary_key=True, index=True),
                    sa.Column('name', sa.String(length=60), nullable=False),
                    sa.Column('is_private', sa.Boolean(), nullable=False, default=False))


def downgrade() -> None:
    op.drop_table('channels')
