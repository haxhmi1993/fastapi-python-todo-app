"""Create Messages table

Revision ID: 7aad9a41c3de
Revises: c7bfb88d5efe
Create Date: 2023-07-21 18:19:05.937043

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7aad9a41c3de'
down_revision = 'c7bfb88d5efe'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'messages',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('message', sa.Text(), nullable=True),
        sa.Column('sender_id', sa.Integer(),
                  sa.ForeignKey('users.id'), nullable=False),
        sa.Column('receiver_id', sa.Integer(),
                  sa.ForeignKey('users.id'), nullable=False),
        sa.Column('channel_id', sa.Integer(), sa.ForeignKey(
            'channels.id'), nullable=False),
        sa.Column('group_id', sa.Integer(), sa.ForeignKey(
            'groups.id'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('messages')
