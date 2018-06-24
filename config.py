from celery.schedules import crontab

# flask
DEBUG = True
# 路由器账号密码
USERNAME = ''
PASSWORD = ''
# 路由器ip
ROUTER_SERVER = ''
# 微信公众号
TOKEN = ''
APP_ID = ''
ENCODING_AES_KEY = ''
# redis
REDIS_PASSWORD = ''
# celery
broker_url = 'redis://:{}@localhost:6379/0'.format(REDIS_PASSWORD)
result_backend = broker_url
beat_schedule = {
    'refresh-ss-every-hour': {
        'task': 'celery_task.refresh_ss',
        'schedule': crontab(minute='*/10'),
        'args': [True]
    },
}
# email
MAIL_SERVER = ''
MAIL_USERNAME = ''
MAIL_PASSWORD = ''
MAIL_DEFAULT_SENDER = ''
# server酱
SECRET_KEY = ''
