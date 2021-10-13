from config.db import metadata, database as db
import sqlalchemy
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID


pgn = sqlalchemy.Table(
    "tbl_pengguna",
    metadata,
    sqlalchemy.Column("user_uuid", UUID(as_uuid=True), primary_key=True),
    sqlalchemy.Column("id_user", sqlalchemy.String),
    sqlalchemy.Column("username_user", sqlalchemy.String),
    sqlalchemy.Column("firstname_user", sqlalchemy.String),
    sqlalchemy.Column("lastname_user", sqlalchemy.String),
    sqlalchemy.Column("jeniskelamin_user", sqlalchemy.String),
    sqlalchemy.Column("ketertarikan_user", sqlalchemy.String),
    sqlalchemy.Column("umur_user", sqlalchemy.String),
    sqlalchemy.Column("joined_at", sqlalchemy.DateTime),
)

idle = sqlalchemy.Table(
    "tbl_iddle",
    metadata,
    sqlalchemy.Column("iddle_uuid", UUID(as_uuid=True), primary_key=True),
    sqlalchemy.Column("id_user", sqlalchemy.String),
    sqlalchemy.Column("status", sqlalchemy.String),
    sqlalchemy.Column("mssg_id", sqlalchemy.String),
)