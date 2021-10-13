"""create table partner

Revision ID: bec1d011dccb
Revises: d1a62627db03
Create Date: 2021-10-11 18:06:29.460929

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import func


# revision identifiers, used by Alembic.
revision = 'bec1d011dccb'
down_revision = 'd1a62627db03'
branch_labels = None
depends_on = None


def upgrade():
    prt = op.create_table(
        'tbl_partner',
        sa.Column('partner_uuid', sa.String(255), primary_key=True),
        sa.Column('id_user_pertama', sa.String(255), nullable=False),
        sa.Column('id_user_kedua', sa.String(255), nullable=True),
        sa.Column('updated_at', sa.TIMESTAMP(True),server_default=func.now()),
        sa.ForeignKeyConstraint(('id_user_pertama',), ['tbl_pengguna.id_user']),
        sa.ForeignKeyConstraint(('id_user_kedua',), ['tbl_pengguna.id_user']),
    )


def downgrade():
    op.drop_table('tbl_partner')
