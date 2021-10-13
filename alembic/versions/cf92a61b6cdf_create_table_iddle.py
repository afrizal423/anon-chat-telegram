"""create table iddle

Revision ID: cf92a61b6cdf
Revises: bec1d011dccb
Create Date: 2021-10-11 19:40:11.306422

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import func


# revision identifiers, used by Alembic.
revision = 'cf92a61b6cdf'
down_revision = 'bec1d011dccb'
branch_labels = None
depends_on = None


def upgrade():
    prt = op.create_table(
        'tbl_iddle',
        sa.Column('iddle_uuid', sa.String(255), primary_key=True),
        sa.Column('id_user', sa.String(255), nullable=False),
        sa.Column('status', sa.Boolean(), default="false"),
        sa.Column('updated_at', sa.TIMESTAMP(True),server_default=func.now()),
        sa.ForeignKeyConstraint(('id_user',), ['tbl_pengguna.id_user']),
    )


def downgrade():
    op.drop_table('tbl_iddle')
