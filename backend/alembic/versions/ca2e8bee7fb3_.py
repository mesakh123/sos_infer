"""empty message

Revision ID: ca2e8bee7fb3
Revises: 
Create Date: 2021-12-15 08:00:01.808071

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ca2e8bee7fb3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('events',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('payload_length', sa.String(), nullable=True),
    sa.Column('timestamps', sa.String(), nullable=True),
    sa.Column('ip_address', sa.String(), nullable=True),
    sa.Column('type', sa.Integer(), nullable=True),
    sa.Column('sent', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('events')
    # ### end Alembic commands ###
