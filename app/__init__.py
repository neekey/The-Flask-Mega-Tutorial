from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import ADMINS, MAIL_PASSWORD, MAIL_PORT, MAIL_SERVER, MAIL_USERNAME

lm = LoginManager()
app = Flask(__name__)
lm.init_app(app)
lm.login_view = 'login'
app.config.from_object('config')
db = SQLAlchemy(app)

# `python -m smtpd -n -c DebuggingServer localhost:25` start a testing server
if not app.debug:
    import logging
    from logging.handlers import SMTPHandler
    credentials = None
    if MAIL_USERNAME or MAIL_PASSWORD:
        credentials = (MAIL_USERNAME, MAIL_PASSWORD)
    mail_handler = SMTPHandler((MAIL_SERVER, MAIL_PORT), 'no-relay@' + MAIL_SERVER, ADMINS, 'microblog failure', credentials)
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)

if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('tmp/microblog.log', 'a', 1 * 1024 * 1024, 10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('microblog startup')


from app import views, models
