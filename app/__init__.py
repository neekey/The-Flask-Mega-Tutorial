import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_openid import OpenID
from config import basedir

lm = LoginManager()
app = Flask(__name__)
lm.init_app(app)
lm.login_view = 'login'
oid = OpenID(app, os.path.join(basedir, 'tmp'))
app.config.from_object('config')
db = SQLAlchemy(app)

from app import views, models
