"""Initial migration.

Revision ID: d0e18a1ecd4e
Revises: 
Create Date: 2023-06-18 22:49:42.132614

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd0e18a1ecd4e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('database',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('repository',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('date_added', sa.DateTime(), nullable=True),
    sa.Column('url', sa.String(length=200), nullable=False),
    sa.Column('type', sa.String(length=20), nullable=False),
    sa.Column('last_polled', sa.DateTime(), nullable=True),
    sa.Column('notes', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('release',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('version', sa.String(length=20), nullable=False),
    sa.Column('notes', sa.Text(), nullable=True),
    sa.Column('url', sa.String(length=200), nullable=True),
    sa.Column('hash', sa.String(length=100), nullable=True),
    sa.Column('repository_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['repository_id'], ['repository.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('release')
    op.drop_table('repository')
    op.drop_table('database')
    # ### end Alembic commands ###
