"""Create Group table

Revision ID: c7bfb88d5efe
Revises: f6752b58d784
Create Date: 2023-07-21 15:07:44.947143

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c7bfb88d5efe'
down_revision = 'f6752b58d784'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'groups',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=60), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'group_user_association',
        sa.Column('group_id', sa.Integer(), sa.ForeignKey(
            'groups.id'), nullable=False),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey(
            'users.id'), nullable=False),
        sa.PrimaryKeyConstraint('group_id', 'user_id')
    )


def downgrade():
    op.drop_table('group_user_association')
    op.drop_table('groups')
