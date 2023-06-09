"""empty message

Revision ID: c13ebff38576
Revises: 97c043deae54
Create Date: 2023-06-05 19:58:15.800506

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c13ebff38576'
down_revision = '97c043deae54'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('pricing_plan', sa.String(length=10), nullable=True))
        batch_op.add_column(sa.Column('api_key', sa.String(), nullable=True))
        batch_op.create_unique_constraint("unique_user_api_key", ['api_key'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint("unique_user_api_key", type_='unique')
        batch_op.drop_column('api_key')
        batch_op.drop_column('pricing_plan')

    # ### end Alembic commands ###
