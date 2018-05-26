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
    helper.set('qr_code', data[0].get('qr_code'))
