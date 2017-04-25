import os
basedir = os.path.abspath(os.path.dirname(__file__))

WTF_CSRF_ENABLED = True
SECRET_KEY = 'YOU WILL NEVER GUESS'

OPENID_PROVIDERS = [
    {'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id'},
    {'name': 'Yahoo', 'url': 'https://me.yahoo.com'},
    {'name': 'AOL', 'url': 'http://openid.aol.com/<username>'},
    {'name': 'Flickr', 'url': 'http://www.flickr.com/<username>'},
    {'name': 'MyOpenID', 'url': 'https://www.myopenid.com'}
]

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = False

OAUTH_CREDENTIALS = {
    'facebook': {
        'id': '1867530783461665',
        'secret': '185275a5e4b189218d55ac8e56b9a129',
        'authorize_url': 'https://graph.facebook.com/oauth/authorize',
        'access_token_url': 'https://graph.facebook.com/oauth/access_token',
        'base_url': 'https://graph.facebook.com/'
    }
}

# mail server settings
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = 'name'
MAIL_PASSWORD = 'password'

# administrator list
ADMINS = ['ni184775761@gmail.com']

# pagination
POSTS_PER_PAGE = 3
