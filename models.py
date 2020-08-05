import sys
from datetime import datetime

sys.path.append('..')

from sqlalchemy import desc
from flask_login import UserMixin

from bookie import db

tags = db.Table("bookmark_tag",
                db.Column("tag_id", db.Integer, db.ForeignKey('tagDB.id')),
                db.Column('bookmark_id', db.Integer, db.ForeignKey('bookmarkDB.id'))
                )


class bookmarkDB(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.String(300))
    user_id = db.Column(db.Integer, db.ForeignKey('userDB.id'), nullable=False)
    _tags = db.relationship('tagDB', secondary=tags, backref='bookmarks', lazy='dynamic')

    @property
    def tags(self):
        return ",".join([t.name for t in self._tags])

    @tags.setter
    def tags(self, string):
        if string:
            self._tags = [tagDB.get_or_create(name) for name in string.split(',')]

    @staticmethod
    def newest(num):
        return bookmarkDB.query.order_by(desc(bookmarkDB.date)).limit(num)

    def __repr__(self):
        return f"<Bookmark '{self.description}':'{self.url}'>"


class userDB(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, nullable=False)
    bookmarks = db.relationship('bookmarkDB', backref='user', lazy='dynamic')

    def __repr__(self):
        return f'Username: {self.name}'


class tagDB(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True, index=True)

    @staticmethod
    def get_or_create(name):
        try:
            return tagDB.query.filter_by(name=name).one()
        except:
            return tagDB(name=name)

    @staticmethod
    def all():
        return tagDB.query.all()

    def __repr__(self):
        return f"Tag:{self.name}"
