import datetime
import operator

import requests
import xmltodict
from flask_mail import Message

from app import celery, mail, app
from common import crawl_ss, sorted_ss, set_route_ss, crawl_ssr
from config import ROUTER_SERVER
from redis_helper import helper


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
    url = f'https://{ROUTER_SERVER}/wol_action.asp'
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


@celery.task
def touch_web_driver():
    url = 'https://gfe.nvidia.com/mac-update'
    ret = requests.get(url)
    ret_dict = xmltodict.parse(ret.text)
    latest = ret_dict.get('plist').get('dict').get('array').get('dict')[0]
    version = latest.get('string')[5]
    url = latest.get('string')[0]
    if version != '387.10.10.10.40.10':
        with app.app_context():
            msg = Message(subject='webdriver更新了！', recipients=['long2ice@qq.com'], body=url)
            mail.send(msg)
