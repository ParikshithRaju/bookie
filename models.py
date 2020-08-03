import sys
from datetime import datetime

sys.path.append('..')

from sqlalchemy import desc
from flask_login import UserMixin

from bookie import db


class bookmarkDB(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.String(300))
    user_id = db.Column(db.Integer, db.ForeignKey('userDB.id'), nullable=False)

    @staticmethod
    def newest(num):
        return bookmarkDB.query.order_by(desc(bookmarkDB.date)).limit(num)

    def __repr__(self):
        return f"<Bookmark '{self.description}':'{self.url}'>"


class userDB(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, nullable=False)
    bookmarks = db.relationship('bookmarkDB', backref='user', lazy='dynamic')

    def __repr__(self):
        return f'Username: {self.name}'
