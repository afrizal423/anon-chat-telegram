from databases import Database
import configparser
from sqlalchemy import (
    create_engine,
    MetaData
)

config = configparser.ConfigParser()
config.read('alembic.ini')

DATABASE_URL = config.get('alembic', 'sqlalchemy.url')

# SQLAlchemy
engine = create_engine(DATABASE_URL)
conn = engine.connect()

# databases query builder
database = Database(DATABASE_URL)

metadata = MetaData()