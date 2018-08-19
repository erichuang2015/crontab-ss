import redis

from config import REDIS_PASSWORD,REDIS_HOST

pool = redis.ConnectionPool(host=REDIS_HOST, decode_responses=True, password=REDIS_PASSWORD)
helper = redis.Redis(connection_pool=pool)
