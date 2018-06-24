import datetime
import operator

from celery import Celery

from common import crawl_ss, sorted_ss, set_route_ss, crawl_ssr
from redis_helper import helper

celery = Celery()
celery.config_from_object('config')


@celery.task
def refresh_ss(is_ss=True):
    if is_ss:
        data = crawl_ss()
        data = sorted_ss(data)
    else:
        data = crawl_ssr()
    ss = helper.get('ss')
    if ss:
        ss = eval(ss)
    if not operator.eq(ss, data[0]):
        helper.set('ss', data[0])
        set_route_ss(data, is_ss)
    helper.set('last_refresh_time', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
