"""Remove depth column from soil_properties table

Revision ID: 2f53bc73f0c1
Revises: 42d06176751c
Create Date: 2024-09-21 07:33:58.299328

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2f53bc73f0c1'
down_revision = '42d06176751c'
branch_labels = None
depends_on = None


def upgrade():
    # Remove the depth column from the soil_properties table
    with op.batch_alter_table('soil_properties') as batch_op:
        batch_op.drop_column('depths')


def downgrade():
    # Add the depth column back to the soil_properties table with a default value
    with op.batch_alter_table('soil_properties') as batch_op:
        batch_op.add_column(sa.Column('depths', sa.String(
            10), nullable=False, server_default='0-20'))
    # ### end Alembic commands ###
