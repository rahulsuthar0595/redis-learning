from redis.sentinel import Sentinel


sentinel = Sentinel([('localhost', 26379)], socket_timeout=0.1)

sentinel.discover_master('redis-test')

