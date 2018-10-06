from celery import Celery
from flask import Flask
from flask_mail import Mail

app = Flask(__name__)
app.config.from_object('config')

mail = Mail(app)

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

if __name__ == '__main__':
    app.run()
