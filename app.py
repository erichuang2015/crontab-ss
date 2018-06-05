from flask import Flask
from flask_mail import Mail
from werobot.contrib.flask import make_view
import views

app = Flask(__name__)
mail = Mail(app)
app.config.from_object('config')
app.add_url_rule('/', view_func=views.index)
app.add_url_rule('/robot', view_func=make_view(views.robot), methods=['GET', 'POST'])

if __name__ == '__main__':
    app.run()
