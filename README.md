# crontab-ss
### 本项目的用途

屌丝程序猿用于抓取免费ss账号并直接更新路由器配置

### 本项目的基本架构如下：

![项目架构](http://p9bxq42du.bkt.clouddn.com/crontab-ss.png)

### 本项目用到的第三方库

* [frp](https://github.com/fatedier/frp)，一个用于内网穿透的工具
* [flask](https://github.com/pallets/flask)，搭建web服务
* [celery](https://github.com/celery/celery)，实现定时任务和异步任务

### 运行方式
* git clone https://github.com/long2ice/crontab-ss.git
* 安装依赖，pip install -r requirements.txt
* 设置好配置文件，详见[config.py](https://github.com/long2ice/crontab-ss/blob/master/config.py)
* celery -A celery_task.celery worker -l info
* python3 app.py
