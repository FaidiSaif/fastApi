"""create test table

Revision ID: 2bc9289e7d16
Revises: 
Create Date: 2022-07-11 16:37:59.339187

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2bc9289e7d16'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('test', sa.Column('id', sa.Integer(), nullable=False,
                    primary_key=True), sa.Column('other', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table('test')
    pass