import redis
# rdb = redis.ConnectionPool(connection_class=redis.UnixDomainSocketConnection, path="/var/run/redis/redis.sock")
r = redis.Redis(unix_socket_path='/tmp/redis.sock')