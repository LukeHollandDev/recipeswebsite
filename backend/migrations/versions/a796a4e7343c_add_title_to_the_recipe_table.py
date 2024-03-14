"""add title to the recipe table

Revision ID: a796a4e7343c
Revises: 3223d70edaa8
Create Date: 2024-03-14 20:02:08.493847

"""
from typing import Sequence, Union
import sqlmodel

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a796a4e7343c'
down_revision: Union[str, None] = '3223d70edaa8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('recipe', sa.Column('title', sqlmodel.sql.sqltypes.AutoString(), nullable=False))
    op.create_index(op.f('ix_recipe_title'), 'recipe', ['title'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_recipe_title'), table_name='recipe')
    op.drop_column('recipe', 'title')
    # ### end Alembic commands ###
