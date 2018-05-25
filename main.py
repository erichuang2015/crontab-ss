"""
定时向https://my.ishadowx.net/ 抓取免费ss账号并生成配置文件
"""
import json
import os
import sys

import requests
from bs4 import BeautifulSoup


def craw_data():
    """
    获取所有的ss账号
    :return:
    """
    ss_url = 'https://my.ishadowx.net/'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': '_ga=GA1.2.1423561819.1527240616; _gid=GA1.2.748244877.1527240616',
        'Host': 'my.ishadowx.net',
        'Upgrade-Insecure-Requests': '1',
        'If-Modified-Since': 'Fri, 25 May 2018 07:20:14 GMT',
        'If-None-Match': '"69a5-56d02996666b3-gzip"',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
    }

    ret = requests.get(ss_url, headers=headers)

    bs4 = BeautifulSoup(ret.text, 'lxml')

    items = bs4.find_all(class_='portfolio-item')
    for item in items:
        h4s = item.find_all('h4')
        ip = h4s[0].span.string.strip()
        port = h4s[1].span.string.strip()
        password = h4s[2].span.string.strip()
        method = h4s[3].string.strip().split(':')[1]
        try:
            qr_code = 'https://my.ishadowx.net/' + h4s[4].a['href']
        except TypeError:
            break
        yield dict(
            ip=ip,
            port=port,
            password=password,
            method=method,
            qr_code=qr_code
        )


def get_best_ss(ss_data):
    """
    返回延迟最小的ss
    :param ss_data:
    :return:
    """
    min_time = 100
    best_server = None
    for item in ss_data:
        print(item)
        ping_result = os.popen('ping -c 3 -t 5 {}'.format(item.get('ip'))).readlines()[-1]
        avg_time = float(ping_result.split(' = ')[1].split('/')[1])
        if avg_time < min_time:
            min_time = avg_time
            best_server = item
    return best_server


def write_ss_config(ss):
    """
    写入ss配置文件
    :param ss:
    :return:
    """
    config_file = sys.path[0] + '/gui-config.json'
    f = open(config_file)
    config = json.load(f)
    config['configs'] = [{
        "remarks": ss.get('ip'),
        "server": ss.get('ip'),
        "server_port": ss.get('port'),
        "method": ss.get('method'),
        "password": ss.get('password'),
        "tcp_over_udp": False,
        "udp_over_tcp": False,
        "enable": True

    }]
    f.close()
    f = open(config_file, 'w')
    json.dump(config, f)
    f.close()


if __name__ == '__main__':
    data = craw_data()
    best_ss = get_best_ss(data)
    write_ss_config(best_ss)
