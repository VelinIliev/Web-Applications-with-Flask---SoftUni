"""add role

Revision ID: a32a3640415f
Revises: e0c759a959ff
Create Date: 2023-03-14 15:33:11.320875

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = 'a32a3640415f'
down_revision = 'e0c759a959ff'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    userrolesenum = postgresql.ENUM('super_admin', 'admin', 'user', name='userrolesenum')
    userrolesenum.create(op.get_bind())
    op.add_column('user', sa.Column('role', sa.Enum('super_admin', 'admin', 'user', name='userrolesenum'), nullable=False, server_default='user'))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('role')

    # ### end Alembic commands ###
