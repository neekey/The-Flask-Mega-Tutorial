from app import app
from flask import render_template, flash, redirect
from .forms import LoginForm


@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Miguel'}
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
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login required for OpenId="%s", remember_me=%s' %
              (form.openid.data, str(form.remember_me.data)))
        return redirect('/index')
    return render_template('login.html',
                           title='Sign In',
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])
