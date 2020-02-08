"""language: concordance text

Revision ID: 35a11e4bd66b
Revises: 14e7799c9ceb
Create Date: 2020-02-08 10:59:25.139562

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '35a11e4bd66b'
down_revision = '14e7799c9ceb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('languages', sa.Column('concordance_md', sa.Text(), nullable=True))
    op.add_column('languages', sa.Column('concordnace_html', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('languages', 'concordnace_html')
    op.drop_column('languages', 'concordance_md')
    # ### end Alembic commands ###
