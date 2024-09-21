"""second migration - updating the soil_measurements table to include location and soil property foreign keys.

Revision ID: be11a6fcf11d
Revises: a0f541a8cb1c
Create Date: 2024-09-21 07:00:01.582163

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'be11a6fcf11d'
down_revision = 'a0f541a8cb1c'
branch_labels = None
depends_on = None


def upgrade():
    # Create a new table with the desired schema
    op.create_table(
        'new_soil_measurements',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('value', sa.Float, nullable=False),
        sa.Column('depth', sa.String(10), nullable=False),
        sa.Column('uncertainty_50', sa.String(255), nullable=True),
        sa.Column('uncertainty_68', sa.String(255), nullable=True),
        sa.Column('uncertainty_90', sa.String(255), nullable=True),
        sa.Column('property_id', sa.Integer,
                  sa.ForeignKey('soil_properties.id')),
        sa.Column('location_id', sa.Integer, sa.ForeignKey('locations.id'))
    )

    # Copy data from the old table to the new table
    op.execute('''
        INSERT INTO new_soil_measurements (id, value, depth, uncertainty_50, uncertainty_68, uncertainty_90, property_id, location_id)
        SELECT id, value, depth, uncertainty_50, uncertainty_68, uncertainty_90, property_id, location_id
        FROM soil_measurements
    ''')

    # Drop the old table
    op.drop_table('soil_measurements')

    # Rename the new table to the old table name
    op.rename_table('new_soil_measurements', 'soil_measurements')


def downgrade():
    # Create the old table with the original schema
    op.create_table(
        'old_soil_measurements',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('value', sa.Float, nullable=False),
        sa.Column('depth', sa.String(10), nullable=False),
        sa.Column('uncertainty_50', sa.String(255), nullable=True),
        sa.Column('uncertainty_68', sa.String(255), nullable=True),
        sa.Column('uncertainty_90', sa.String(255), nullable=True),
        sa.Column('property_id', sa.Integer,
                  sa.ForeignKey('soil_properties.id'))
        # Note: location_id is not included in the old schema
    )

    # Copy data from the new table to the old table
    op.execute('''
        INSERT INTO old_soil_measurements (id, value, depth, uncertainty_50, uncertainty_68, uncertainty_90, property_id)
        SELECT id, value, depth, uncertainty_50, uncertainty_68, uncertainty_90, property_id
        FROM soil_measurements
    ''')

    # Drop the new table
    op.drop_table('soil_measurements')

    # Rename the old table to the original table name
    op.rename_table('old_soil_measurements', 'soil_measurements')
