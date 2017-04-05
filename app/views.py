from app import app, lm, oid, db
from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from .models import User
from .forms import LoginForm


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


@app.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        print('try login', form.openid.data)
        return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])
    openIdError = oid.fetch_error()
    print('openId error', openIdError)
    return render_template('login.html',
                           title='Sign In',
                           form=form,
                           error=openIdError,
                           providers=app.config['OPENID_PROVIDERS'])


@oid.after_login
def after_login(resp):
    print('after login', resp.email)
    if resp.email is None or resp.email == '':
        flash('Invalid login. Please try again.')
        return redirect(url_for('login'))
    user = User.query.filter_by(email=resp.email).first()
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == '':
            nickname = resp.email.split('@')[0]
        user = User(nickname=nickname, email=resp.email)
        db.session.add(user)
        db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember=remember_me)
    return redirect(request.args.get('next') or url_for('index'))


@app.before_request
def before_request():
    g.user = current_user
