import werobot
from flask import render_template

from celery_task import refresh_ss as refresh_ss_task
from redis_helper import helper

robot = werobot.WeRoBot()
robot.config.from_pyfile('config.py')


def index():
    qr_code = helper.get('qr_code')
    return render_template('index.html', qr_code=qr_code)


@robot.filter('刷新ss')
def refresh_ss():
    refresh_ss_task.delay()
    return '刷新成功！'
