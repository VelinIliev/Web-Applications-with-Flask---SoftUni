"""add reader table and on to many relation

Revision ID: 81fe70c5b62e
Revises: b7db39e4d5d6
Create Date: 2023-02-14 13:51:03.608946

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '81fe70c5b62e'
down_revision = 'b7db39e4d5d6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('readers',
    sa.Column('pk', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=False),
    sa.Column('last_name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('pk')
    )
    op.add_column('books', sa.Column('reader_pk', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'books', 'readers', ['reader_pk'], ['pk'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'books', type_='foreignkey')
    op.drop_column('books', 'reader_pk')
    op.drop_table('readers')
    # ### end Alembic commands ###
