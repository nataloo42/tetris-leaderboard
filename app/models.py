from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from datetime import datetime, timezone
from flask_login import UserMixin
# from app import login
from hashlib import md5


class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    first_name: so.Mapped[int] = so.mapped_column(sa.String(30))
    last_name: so.Mapped[int] = so.mapped_column(sa.String(30))    
    rating: so.Mapped[int] = so.mapped_column(sa.Integer)

    def __repr__(self):
        return '<{} {}>'.format(self.first_name, self.last_name)