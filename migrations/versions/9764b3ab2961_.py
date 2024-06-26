"""empty message

Revision ID: 9764b3ab2961
Revises: 
Create Date: 2024-04-22 12:27:13.465823

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9764b3ab2961'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('student',
    sa.Column('student_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('dob', sa.Date(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('student_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('student')
    # ### end Alembic commands ###
