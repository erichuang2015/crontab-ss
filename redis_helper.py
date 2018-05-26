import redis

from config import REDIS_PASSWORD

pool = redis.ConnectionPool(decode_responses=True, password=REDIS_PASSWORD)
helper = redis.Redis(connection_pool=pool)
