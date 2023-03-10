"""add new column to books model

Revision ID: b7db39e4d5d6
Revises: b5911adcf28c
Create Date: 2023-02-14 13:13:46.599295

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b7db39e4d5d6'
down_revision = 'b5911adcf28c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('books', sa.Column('just_test', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('books', 'just_test')
    # ### end Alembic commands ###
