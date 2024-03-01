from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db, login
from datetime import datetime, timezone
from flask_login import UserMixin
from hashlib import md5


class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[Optional[str]] = so.mapped_column(sa.String(30), index=True,
                                                unique=True)
    first_name: so.Mapped[Optional[str]] = so.mapped_column(sa.String(30))
    last_name: so.Mapped[Optional[str]] = so.mapped_column(sa.String(30))
    rating: so.Mapped[int] = so.mapped_column(sa.Integer)
    wins: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer)
    losses: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer)
    password: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    def __repr__(self):
        return '<{} {}>'.format(self.first_name, self.last_name)

    def check_password(self, password):
        return password == self.password

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))
