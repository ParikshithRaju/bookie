import storing
from datetime import datetime

db = storing.db


class BookmarkDB(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.String(300))

    def __repr__(self):
        return f"<Bookmark '{self.description}':'{self.url}'"
