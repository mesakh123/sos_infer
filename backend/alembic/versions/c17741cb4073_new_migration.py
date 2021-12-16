"""New Migration

Revision ID: c17741cb4073
Revises: a69860e0ce6d
Create Date: 2021-12-16 03:43:47.702465

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c17741cb4073'
down_revision = 'a69860e0ce6d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('events',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('payload_length', sa.String(), nullable=True),
    sa.Column('timestamps', sa.DateTime(timezone=True), nullable=True),
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