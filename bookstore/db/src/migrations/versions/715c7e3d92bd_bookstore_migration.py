"""bookstore migration

Revision ID: 715c7e3d92bd
Revises: 
Create Date: 2024-06-06 17:46:56.495436

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '715c7e3d92bd'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        't_bookstore',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('title', sa.String, nullable=False),
        sa.Column('author', sa.String, nullable=False),
        sa.Column('category', sa.String, nullable=False),
        sa.Column('description', sa.String, nullable=False),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('t_bookstore')
