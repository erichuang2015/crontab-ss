import requests
import werobot
from flask import Response
from werobot.replies import ArticlesReply, Article

from celery_task import refresh_ss as refresh_ss_task
from common import headers, ss_to_str
from redis_helper import helper

robot = werobot.WeRoBot()
robot.config.from_pyfile('config.py')


def index():
    ss = eval(helper.get('ss'))
    ret = requests.get(ss.get('qr_code'), headers=headers)
    return Response(response=ret.content, mimetype='image/jpg')


@robot.filter('刷新ss')
def refresh_ss():
    refresh_ss_task.delay()
    return '刷新ss成功！上次刷新时间：{}'.format(helper.get('last_refresh_time') or '无')


@robot.filter('刷新ssr')
def refresh_ss():
    refresh_ss_task.delay(False)
    return '刷新ssr成功！上次刷新时间：{}'.format(helper.get('last_refresh_time') or '无')


@robot.filter('ss')
def get_ss(message):
    ss = eval(helper.get('ss'))
    reply = ArticlesReply(message=message)
    article = Article(
        title='ss账号',
        description=ss_to_str(ss),
        img=ss.get('qr_code'),
        url='http://wechat.long2ice.cn/'
    )
    reply.add_article(article)
    return reply
