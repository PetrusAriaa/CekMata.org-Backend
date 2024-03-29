"""Generate table

Revision ID: 6d93fa51d31d
Revises: 
Create Date: 2024-03-02 15:29:44.701582+07:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6d93fa51d31d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('patients',
    sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False, unique=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('code', sa.String(length=9), nullable=True, unique=True),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('birth', sa.Date(), nullable=True),
    sa.Column('phone', sa.String(length=20), nullable=True),
    sa.Column('classification', sa.String(length=255), nullable=True),
    sa.Column('recommendation', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False, unique=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('username', sa.String(length=32), nullable=True),
    sa.Column('password', sa.String(length=255), nullable=True),
    sa.Column('last_login', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('controls',
    sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False, unique=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('fk_patient_id', sa.UUID(), nullable=True),
    sa.Column('fk_patient_code', sa.String(length=9), nullable=True),
    sa.Column('patient_name', sa.String(length=255), nullable=True),
    sa.Column('last_control', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['fk_patient_code'], ['patients.code'], ),
    sa.ForeignKeyConstraint(['fk_patient_id'], ['patients.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('controls')
    op.drop_table('users')
    op.drop_table('patients')
    # ### end Alembic commands ###
