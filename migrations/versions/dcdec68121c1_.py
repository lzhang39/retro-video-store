"""empty message

Revision ID: dcdec68121c1
Revises: b4a06c1d948a
Create Date: 2021-05-20 01:23:00.618784

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'dcdec68121c1'
down_revision = 'b4a06c1d948a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('customers',
    sa.Column('customer_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('postal_code', sa.String(), nullable=True),
    sa.Column('phone', sa.String(), nullable=True),
    sa.Column('registered_at', sa.DateTime(), nullable=True),
    sa.Column('videos_checked_out_count', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('customer_id')
    )
    op.create_table('videos',
    sa.Column('video_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('release_date', sa.DateTime(), nullable=True),
    sa.Column('total_inventory', sa.Integer(), nullable=True),
    sa.Column('available_inventory', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('video_id')
    )
    op.create_table('rentals',
    sa.Column('rental_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('customer_id', sa.Integer(), nullable=False),
    sa.Column('video_id', sa.Integer(), nullable=False),
    sa.Column('due_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['customer_id'], ['customers.customer_id'], ),
    sa.ForeignKeyConstraint(['video_id'], ['videos.video_id'], ),
    sa.PrimaryKeyConstraint('rental_id', 'customer_id', 'video_id')
    )
    op.drop_table('rental')
    op.drop_table('video')
    op.drop_table('customer')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('customer',
    sa.Column('customer_id', sa.INTEGER(), server_default=sa.text("nextval('customer_customer_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('postal_code', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('phone', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('registered_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('videos_checked_out_count', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('customer_id', name='customer_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('video',
    sa.Column('video_id', sa.INTEGER(), server_default=sa.text("nextval('video_video_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('title', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('release_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('total_inventory', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('available_inventory', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('video_id', name='video_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('rental',
    sa.Column('rental_id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('customer_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('video_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('due_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['customer_id'], ['customer.customer_id'], name='rental_customer_id_fkey'),
    sa.ForeignKeyConstraint(['video_id'], ['video.video_id'], name='rental_video_id_fkey'),
    sa.PrimaryKeyConstraint('rental_id', 'customer_id', 'video_id', name='rental_pkey')
    )
    op.drop_table('rentals')
    op.drop_table('videos')
    op.drop_table('customers')
    # ### end Alembic commands ###
