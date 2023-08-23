"""init

Revision ID: 38e09e494a2f
Revises: 
Create Date: 2023-08-21 16:26:53.976111

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '38e09e494a2f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('category', sa.Column('test_field', sa.String(length=255), nullable=True))
    op.drop_index('fulltext_name', table_name='dish', mysql_prefix='FULLTEXT')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('fulltext_name', 'dish', ['name'], unique=False, mysql_prefix='FULLTEXT')
    op.drop_column('category', 'test_field')
    # ### end Alembic commands ###