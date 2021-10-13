"""create table pengguna

Revision ID: d1a62627db03
Revises: 
Create Date: 2021-10-11 17:51:16.821628

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd1a62627db03'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    pgn = op.create_table(
        'tbl_pengguna',
        sa.Column('user_uuid', sa.String(255), primary_key=True),
        sa.Column('id_user', sa.String(255), nullable=False, unique=True),
        sa.Column('username_user', sa.String(255)),
        sa.Column('firstname_user', sa.String(255)),
        sa.Column('lastname_user', sa.String(255)),
        sa.Column('jeniskelamin_user', sa.String(2)),
        sa.Column('ketertarikan_user', sa.String(2)),
        sa.Column('umur_user', sa.Integer()),
        sa.Column('joined_at', sa.DateTime()),
    )


def downgrade():
    op.drop_table('tbl_pengguna')
