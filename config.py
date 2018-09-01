from celery.schedules import crontab
import os
from dotenv import load_dotenv

load_dotenv()
# flask
DEBUG = os.getenv('DEBUG', bool)
# 路由器账号密码
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
# 路由器ip
ROUTER_SERVER = os.getenv('ROUTER_SERVER')
# 微信公众号
TOKEN = os.getenv('TOKEN')
APP_ID = os.getenv('APP_ID')
ENCODING_AES_KEY = os.getenv('ENCODING_AES_KEY')
# redis
REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')
# celery
broker_url = os.getenv('broker_url')
result_backend = broker_url
beat_schedule = {
    # 'refresh-ss-every-hour': {
    #     'task': 'celery_task.refresh_ss',
    #     'schedule': crontab(minute='*/10'),
    #     'args': [True]
    # },
    'sign-ss-every-day': {
        'task': 'celery_task.sign_ss',
        'schedule': crontab(minute='0', hour='22'),
        'args': []
    },
}
# email
MAIL_SERVER = os.getenv('MAIL_SERVER')
MAIL_USERNAME = os.getenv('MAIL_USERNAME')
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')
# server酱
SECRET_KEY = os.getenv('SECRET_KEY')
