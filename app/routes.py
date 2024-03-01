from flask_basicauth import BasicAuth
from app import app
from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user
import sqlalchemy as sa
from app import db
from app.models import User
from app.forms import LoginForm
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView, Admin
from werkzeug.exceptions import HTTPException
from werkzeug import Response
from flask import request
from urllib.parse import urlsplit

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    query = sa.select(User)
    users = db.session.scalars(query).all()
    headers = ['First Name', 'Last Name', 'Rating', 'Wins', 'Losses']
    return render_template('index.html', users=users, headers=headers)

# Basic login page. Not necessary to view basic /index content but we could use this to
# add more user-specific features later.
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

# This class supercedes ModelView to restrict access to authenticated users only
class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))

# Use the built-in flask-admin to create the /admin domain
# This is currently only accessible to kclements user
# If more users need to use it in the future, this can be easily changed
admin = Admin(app, name="Admin")
admin.add_view(MyModelView(User, db.session))