from flask import url_for
from app import app
from flask import render_template, flash, redirect
from flask_login import current_user, login_user
import sqlalchemy as sa
from app import db
from app.models import User
# from flask_login import logout_user, login_required
from flask import request
from urllib.parse import urlsplit

@app.route('/')
@app.route('/index')
def index():
    query = sa.select(User)
    users = db.session.scalars(query).all()
    headers = ['First Name', 'Last Name', 'Rating']
    return render_template('index.html', users=users, headers=headers)