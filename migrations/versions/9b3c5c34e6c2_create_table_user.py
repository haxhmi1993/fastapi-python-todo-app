"""create table user

Revision ID: 9b3c5c34e6c2
Revises: 55af536711b1
Create Date: 2023-07-12 17:47:00.696017

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9b3c5c34e6c2'
down_revision = '55af536711b1'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True,
                  index=True, nullable=False),
        sa.Column('email', sa.String(length=100), unique=True, nullable=False),
        sa.Column('username', sa.String(length=100),
                  unique=True, nullable=False),
        sa.Column('first_name', sa.String(length=100), nullable=True),
        sa.Column('last_name', sa.String(length=100), nullable=True),
        sa.Column('hashed_password', sa.String(length=200)),
        sa.Column('is_active', sa.Boolean(), default=False),
        sa.Column('phone_number', sa.String(length=20), nullable=True),
    )


def downgrade():
    op.drop_table('users')
