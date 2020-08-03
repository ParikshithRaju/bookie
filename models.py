import sys
from datetime import datetime
sys.path.append('..')

from sqlalchemy import desc

from bookie import db


class BookmarkDB(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.String(300))

    @staticmethod
    def newest(num):
        return BookmarkDB.query.order_by(desc(BookmarkDB.date)).limit(num)

    def __repr__(self):
        return f"<Bookmark '{self.description}':'{self.url}'>"


class UserDB(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'Username: {self.name}'
