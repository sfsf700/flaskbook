"""empty message

Revision ID: 607df83931d3
Revises: 7a00b209f784
Create Date: 2022-11-25 10:08:43.251935

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '607df83931d3'
down_revision = '7a00b209f784'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_images',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.String(), nullable=True),
    sa.Column('image_path', sa.String(), nullable=True),
    sa.Column('is_detected', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_images')
    # ### end Alembic commands ###
