from .. import config
from gino_starlette import Gino

db = Gino(dsn=config.DB_DSN,
          pool_min_size=config.DB_POOL_MIN_SIZE,
          pool_max_size=config.DB_POOL_MAX_SIZE,
          echo=config.DB_ECHO,
          ssl=config.DB_SSL,
          use_connection_for_request=config.DB_USE_CONNECTION_FOR_REQUEST,
          retry_limit=config.DB_RETRY_LIMIT,
          retry_interval=config.DB_RETRY_INTERVAL, )

# Import your models here so Alembic will pick them up
from backend.users.models import *

