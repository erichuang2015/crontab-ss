import datetime
import operator

from celery import Celery

from common import craw_data, sorted_ss, set_route_ss
from redis_helper import helper

celery = Celery()
celery.config_from_object('config')


@celery.task
def refresh_ss():
    data = craw_data()
    data = sorted_ss(data)
    set_route_ss(data)
    ss = eval(helper.get('ss'))
    if not operator.eq(ss, data[0]):
        helper.set('ss', data[0])
    helper.set('last_refresh_time', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
