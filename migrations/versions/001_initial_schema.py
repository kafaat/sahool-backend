"""initial schema

Revision ID: 001
Revises: 
Create Date: 2025-11-21 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
import geoalchemy2
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Enable PostGIS extension
    op.execute('CREATE EXTENSION IF NOT EXISTS postgis')
    
    # Create farms table
    op.create_table('farms',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('owner_name', sa.String(), nullable=True),
        sa.Column('location', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create fields table
    op.create_table('fields',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('farm_id', sa.Integer(), nullable=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('boundary', geoalchemy2.types.Geometry(geometry_type='POLYGON', srid=4326), nullable=False),
        sa.Column('area_ha', sa.Float(), nullable=True),
        sa.ForeignKeyConstraint(['farm_id'], ['farms.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_fields_farm_id'), 'fields', ['farm_id'], unique=False)
    
    # Create satellite_images table
    op.create_table('satellite_images',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('field_id', sa.Integer(), nullable=False),
        sa.Column('source', sa.String(), nullable=True),
        sa.Column('captured_at', sa.DateTime(), nullable=True),
        sa.Column('red_path', sa.String(), nullable=False),
        sa.Column('nir_path', sa.String(), nullable=False),
        sa.Column('cloud_percent', sa.Float(), nullable=True),
        sa.Column('meta', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.ForeignKeyConstraint(['field_id'], ['fields.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_satellite_images_field_id'), 'satellite_images', ['field_id'], unique=False)
    op.create_index(op.f('ix_satellite_images_captured_at'), 'satellite_images', ['captured_at'], unique=False)
    
    # Create ndvi_results table
    op.create_table('ndvi_results',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('image_id', sa.Integer(), nullable=True),
        sa.Column('field_id', sa.Integer(), nullable=True),
        sa.Column('processed_at', sa.DateTime(), nullable=True),
        sa.Column('mean_ndvi', sa.Float(), nullable=True),
        sa.Column('min_ndvi', sa.Float(), nullable=True),
        sa.Column('max_ndvi', sa.Float(), nullable=True),
        sa.Column('ndvi_tif_path', sa.String(), nullable=True),
        sa.Column('ndvi_png_path', sa.String(), nullable=True),
        sa.Column('stats', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.ForeignKeyConstraint(['field_id'], ['fields.id'], ),
        sa.ForeignKeyConstraint(['image_id'], ['satellite_images.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ndvi_results_field_id'), 'ndvi_results', ['field_id'], unique=False)
    op.create_index(op.f('ix_ndvi_results_image_id'), 'ndvi_results', ['image_id'], unique=False)
    
    # Create change_detection_results table
    op.create_table('change_detection_results',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('field_id', sa.Integer(), nullable=True),
        sa.Column('old_ndvi_id', sa.Integer(), nullable=True),
        sa.Column('new_ndvi_id', sa.Integer(), nullable=True),
        sa.Column('processed_at', sa.DateTime(), nullable=True),
        sa.Column('delta_tif_path', sa.String(), nullable=True),
        sa.Column('stats', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.ForeignKeyConstraint(['field_id'], ['fields.id'], ),
        sa.ForeignKeyConstraint(['old_ndvi_id'], ['ndvi_results.id'], ),
        sa.ForeignKeyConstraint(['new_ndvi_id'], ['ndvi_results.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_change_detection_results_field_id'), 'change_detection_results', ['field_id'], unique=False)
    
    # Create alerts table
    op.create_table('alerts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('field_id', sa.Integer(), nullable=True),
        sa.Column('result_id', sa.Integer(), nullable=True),
        sa.Column('type', sa.String(), nullable=True),
        sa.Column('message', sa.String(), nullable=True),
        sa.Column('severity', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['field_id'], ['fields.id'], ),
        sa.ForeignKeyConstraint(['result_id'], ['ndvi_results.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_alerts_field_id'), 'alerts', ['field_id'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_alerts_field_id'), table_name='alerts')
    op.drop_table('alerts')
    op.drop_index(op.f('ix_change_detection_results_field_id'), table_name='change_detection_results')
    op.drop_table('change_detection_results')
    op.drop_index(op.f('ix_ndvi_results_image_id'), table_name='ndvi_results')
    op.drop_index(op.f('ix_ndvi_results_field_id'), table_name='ndvi_results')
    op.drop_table('ndvi_results')
    op.drop_index(op.f('ix_satellite_images_captured_at'), table_name='satellite_images')
    op.drop_index(op.f('ix_satellite_images_field_id'), table_name='satellite_images')
    op.drop_table('satellite_images')
    op.drop_index(op.f('ix_fields_farm_id'), table_name='fields')
    op.drop_table('fields')
    op.drop_table('farms')
    op.execute('DROP EXTENSION IF EXISTS postgis')
