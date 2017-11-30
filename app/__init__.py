from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
# from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__, instance_relative_config=True)


# config
from util import filter

app.config.from_object('config.DevelopConfig')
app.config.from_pyfile('config.py')


# tools
# db = SQLAlchemy(app)
mail = Mail(app)
bcrypt = Bcrypt(app)
csrf = CSRFProtect(app)
login_manager = LoginManager(app)

login_manager.login_view = 'home.login'
login_manager.session_protection = 'strong'


# from app.view.home import home
# from app.view.register import register
# from app.view.mypage import mypage
#
# app.register_blueprint(home)
# app.register_blueprint(register)
# app.register_blueprint(mypage)

# service
from app.view.service.bank import bank_service

app.register_blueprint(bank_service, url_prefix='/service/bank')

# TODO api
# from app.view.api.db import data
#
# app.register_blueprint(data)
