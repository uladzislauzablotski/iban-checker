"""auto

Revision ID: 6152d332ffe3
Revises: 
Create Date: 2023-09-20 23:04:15.359001

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '6152d332ffe3'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('iban',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('iban', sa.String(), nullable=True),
    sa.Column('status', sa.Enum('VALID', 'NOT_VALID', name='validationstatus'), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_iban_id'), 'iban', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_iban_id'), table_name='iban')
    op.drop_table('iban')
    # ### end Alembic commands ###
