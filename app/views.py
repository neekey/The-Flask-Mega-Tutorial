from app import app, lm, db
from flask import render_template, flash, redirect, url_for, request, g
from flask_login import login_user, current_user, login_required
from .models import User
from .OAuth import OAuthSignIn


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/')
@app.route('/index')
@login_required
def index():
    user = g.user
    posts = [
        {
            'author': 'Neekey',
            'body': 'A Python newbie from Fed world.'
        },
        {
            'author': 'Mason',
            'body': 'A good Chef who can cook delicious chicken.'
        },
    ]
    return render_template('index.html',
                           title='Home',
                           user=user,
                           posts=posts)


@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@app.route('/callback/<provider>')
def oauth_callback(provider):
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    social_id, username, email = oauth.callback()
    if social_id is None:
        flash('Authentication failed.')
        return redirect(url_for('login'))
    user = User.query.filter_by(email=email).first()
    if user is None:
        nickname = username
        if nickname is None or nickname == '':
            nickname = email.split('@')[0]
        user = User(nickname=nickname, email=email, social_id=social_id)
        db.session.add(user)
        db.session.commit()
    login_user(user)
    return redirect(request.args.get('next') or url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    return render_template('login.html',
                           title='Sign In')


@app.before_request
def before_request():
    g.user = current_user
