import base64
import json
import os
import sys

import requests
from bs4 import BeautifulSoup

from config import USERNAME, PASSWORD, ROUTER_SERVER, SECRET_KEY

headers = {
    'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Cookie': '_ga=GA1.2.1423561819.1527240616; _gid=GA1.2.748244877.1527240616',
    'Host': 'us.ishadowx.net',
    'Upgrade-Insecure-Requests': '1',
    'If-Modified-Since': 'Fri, 25 May 2018 07:20:14 GMT',
    'If-None-Match': '"69a5-56d02996666b3-gzip"',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
}


def crawl_ss():
    """
    获取所有的ss账号
    :return:
    """
    ss_url = 'https://us.ishadowx.net/'
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
            qr_code = 'https://us.ishadowx.net/' + h4s[4].a['href']
        except TypeError:
            break
        if ip and port and password and method and qr_code:
            yield dict(
                ip=ip,
                port=port,
                password=password,
                method=method,
                qr_code=qr_code
            )


def sorted_ss(ss_data):
    """
    根据ss延迟返回排序的数据
    :param ss_data:
    :return:
    """
    ret_data = []
    for item in ss_data:
        print(item)
        ping_result = os.popen('ping -c 3 {}'.format(item.get('ip'))).readlines()[-1]
        try:
            avg_time = float(ping_result.split(' = ')[1].split('/')[1])
            print(avg_time)
        except IndexError:
            continue
        item['avg_time'] = avg_time
        ret_data.append(item)
    return sorted(ret_data, key=lambda x: x.get('avg_time'))


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


def set_route_ss(ss_data, is_ss=True):
    """
    设置到路由器
    :param is_ss: ss or ssr
    :param ss_data:
    :return:
    """
    if is_ss:
        ss_type = '0'
    else:
        ss_type = '1'
    url = 'https://{}/start_apply.htm'.format(ROUTER_SERVER)
    payload = {
        'current_page': '/Advanced_Extensions_SS.asp', 'sid_list': 'LANHostConfig;General;',
        'action_mode': ' Apply ', 'wan_ipaddr': '192.168.1.2', 'wan_netmask': '255.255.255.0',
        'dhcp_start': '192.168.123.2', 'dhcp_end': '192.168.123.244', 'v2ray_follow_o': '0',
        'ss_run_ss_local': '0', 'ss_enable': '1', 'v2ray_follow': '0', 'ss_type': ss_type,
        'ss_mode_x': '1', 'kcptun2_enable': '0', 'kcptun2_enable2': '0',
        'ss_s1_local_address': '0.0.0.0', 'ss_s2_local_address': '0.0.0.0', 'ss_s1_local_port': '1081',
        'ss_s2_local_port': '1082',
        'ss_server': ss_data[0].get('ip'),
        'ss_server2': ss_data[1].get('ip'),
        'ss_server_port': ss_data[0].get('port'),
        'ss_s2_port': ss_data[1].get('port'),
        'ss_key': ss_data[0].get('password'),
        'ss_s2_key': ss_data[1].get('password'),
        'ss_method': ss_data[0].get('method'),
        'ss_s2_method': ss_data[1].get('method'), 'ssr_type_protocol_write': 'null',
        'ssr2_type_protocol_write': 'null', 'ssr_type_obfs_write': 'null', 'ssr2_type_obfs_write': 'null',
        'ss_multiport': '22,80,443', 'ss_tochina_enable': '0', 'ss_udp_enable': '1',
        'ss_DNS_Redirect': '0', 'ss_dnsproxy_x': '0', 'ss_pdnsd_wo_redir': '1', 'ss_pdnsd_all': '0',
        'ss_3p_enable': '1', 'ss_3p_gfwlist': '1', 'ss_3p_kool': '1', 'ss_sub1': '1', 'ss_sub3': '1',
        'ss_check': '1', 'ss_keep_check': '1', 'ss_link_1': 'www.163.com',
        'ss_link_2': 'www.google.com.hk', 'ss_updatess': '0', 'ss_update': '0', 'ss_update_hour': '23',
        'ss_update_min': '59',
        'scripts.shadowsocks_mydomain_script.sh': 'www.91ribiw.site\r\nwww.taofulile.com\r\n',
        'LAN_AC_IP': '0', 'scripts.shadowsocks_ss_spec_lan.sh':
            '#b,192.168.123.115\r\n#g,192.168.123.116\r\n#n,192.168.123.117\r\n#1,192.168.123.118\r\n#2,192.168.123.119\r\n#b,099B9A909FD9\r\n#1,099B9A909FD9\r\n#2,A9:CB:3A:5F:1F:C7\r\n\r\n\r\n',
        'scripts.shadowsocks_ss_spec_wan.sh':
            'WAN@raw.githubusercontent.com\r\n#WAN+8.8.8.8\r\n#WAN@www.google.com\r\n#WAN!www.baidu.com\r\n#WAN-223.5.5.5\r\n#WAN-114.114.114.114\r\nWAN!members.3322.org\r\nWAN!www.cloudxns.net\r\nWAN!dnsapi.cn\r\nWAN!api.dnspod.com\r\nWAN!www.ipip.net\r\nWAN!alidns.aliyuncs.com\r\n\r\n\r\n#以下样板是四个网段分别对应BLZ的美/欧/韩/台服\r\n#WAN+24.105.0.0/18\r\n#WAN+80.239.208.0/20\r\n#WAN+182.162.0.0/16\r\n#WAN+210.242.235.0/24\r\n#以下样板是telegram\r\n#WAN+149.154.160.1/32\r\n#WAN+149.154.160.2/31\r\n#WAN+149.154.160.4/30\r\n#WAN+149.154.160.8/29\r\n#WAN+149.154.160.16/28\r\n#WAN+149.154.160.32/27\r\n#WAN+149.154.160.64/26\r\n#WAN+149.154.160.128/25\r\n#WAN+149.154.161.0/24\r\n#WAN+149.154.162.0/23\r\n#WAN+149.154.164.0/22\r\n#WAN+149.154.168.0/21\r\n#WAN+91.108.4.0/22\r\n#WAN+91.108.56.0/24\r\n#WAN+109.239.140.0/24\r\n#WAN+67.198.55.0/24\r\n#WAN+91.108.56.172\r\n#WAN+149.154.175.50\r\n\r\n\r\nWAN!opt.cn2qq.com\r\n'
    }
    if not is_ss:
        payload['ss_usage'] = '-O origin -o plain'
        payload['ss_s2_usage'] = '-O origin -o plain'
        payload['ssr2_type_obfs'] = 'plain'
        payload['ssr2_type_obfs_write'] = 'plain'
        payload['ssr_type_obfs'] = 'plain'
        payload['ssr_type_obfs_write'] = 'plain'
        payload['ssr2_type_protocol'] = 'origin'
        payload['ssr2_type_protocol_write'] = 'origin'
        payload['ssr_type_protocol'] = 'origin'
        payload['ssr_type_protocol_write'] = 'origin'
    ret = requests.post(url, data=payload, auth=(USERNAME, PASSWORD))
    print(ret)


def notify_message(title, message):
    """
    通过server酱发送通知
    :return:
    """
    url = 'https://sc.ftqq.com/{}.send'.format(SECRET_KEY)
    data = {
        'text': title,
        'desp': message
    }
    requests.post(url, data=data)


def ss_to_str(ss):
    """
    ss账号转字符串
    :param ss:
    :return:
    """
    return 'ip:{}\nport:{}\npassword:{}\nmethod:{}'.format(ss.get('ip'), ss.get('port'), ss.get('password'),
                                                           ss.get('method'))


def crawl_ssr():
    ret = requests.get('https://tool.ssrshare.xyz/tool/api/free_ssr?key=1529510400_9_lpk&page=1&limit=90').json()
    ss_list = ret.get('data')
    ss_data = []
    for ss in ss_list:
        if ss.get('m_station_cn_status') == 'true':
            ss_data.append(dict(
                ip=ss.get('server'),
                port=ss.get('server_port'),
                password=ss.get('password'),
                method=ss.get('server'),
                qrcode=None,
                avg_time=ss.get('m_station_cn_ms')
            ))
    return sorted(ss_data, key=lambda x: x.get('avg_time'))


def b64decode(s):
    s += '=' * (-len(s) % 4)
    return base64.b64decode(s).decode()
