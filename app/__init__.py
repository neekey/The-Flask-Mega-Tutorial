from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import config

lm = LoginManager()
app = Flask(__name__)
lm.init_app(app)
lm.login_view = 'login'
app.config.from_object(config)
db = SQLAlchemy(app)

from app import views, models
