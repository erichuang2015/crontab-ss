import datetime
import operator

import requests
from celery import Celery

from common import crawl_ss, sorted_ss, set_route_ss, crawl_ssr
from config import ROUTER_SERVER
from redis_helper import helper

celery = Celery()
celery.config_from_object('config')
celery.conf.broker_url = 'redis://:456d1adsnkasnn^&*^*146312d1a@long2ice.cn:6379/0'


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


@celery.task
def start_up_pc():
    url = 'https://{}/wol_action.asp'.format(ROUTER_SERVER)
    params = dict(dstmac='60:45:CB:7F:F4:AB')
    ret = requests.get(url, params)
    return ret.json()


@celery.task
def sign_ss():
    """
    ss签到
    :return:
    """
    login_url = 'https://www.baacloud.info/modules/_login.php'
    login_data = {
        'email': 'long2ice@gmail.com',
        'passwd': 'CatLiewpyifan8U',
        'remember_me': 'week'
    }
    login_data_2 = {
        'email': '343178315@qq.com',
        'passwd': 'MoveQuiWrujwu1O',
        'remember_me': 'week'
    }
    session = requests.Session()
    session.post(login_url, data=login_data)
    sign_url = 'https://www.baacloud.info/modules/_checkin.php'
    ret = session.get(sign_url)
    session = requests.Session()
    session.post(login_url, data=login_data_2)
    sign_url = 'https://www.baacloud.info/modules/_checkin.php'
    ret = session.get(sign_url)
    return ret.text
