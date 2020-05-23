from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .. import config
from gino_starlette import Gino

db = Gino(dsn=config.DB_DSN)

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
