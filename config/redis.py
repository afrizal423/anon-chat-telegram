import redis
from config.db import config

config.read('konfig.ini')

# rdb = redis.ConnectionPool(connection_class=redis.UnixDomainSocketConnection, path="/var/run/redis/redis.sock")
r = redis.Redis(unix_socket_path=config.get('BotKu', 'REDIS_SOCK'))