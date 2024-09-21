"""Remove depth column from soil_measurements table

Revision ID: 42d06176751c
Revises: be11a6fcf11d
Create Date: 2024-09-21 07:20:19.064963

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '42d06176751c'
down_revision = 'be11a6fcf11d'
branch_labels = None
depends_on = None


def upgrade():
    # Remove the depth column from the soil_measurements table
    with op.batch_alter_table('soil_measurements') as batch_op:
        batch_op.drop_column('depth')


def downgrade():
    # Add the depth column back to the soil_measurements table with a default value
    with op.batch_alter_table('soil_measurements') as batch_op:
        batch_op.add_column(sa.Column('depth', sa.String(
            10), nullable=False, server_default='0-20'))
        # ### end Alembic commands ###
