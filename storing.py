from website import app
import os
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

baseDir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(baseDir, "myDatabase.db")
db = SQLAlchemy(app)

import models

def storeBookMark(form):
    db.session.add(
        models.BookmarkDB(url=form['url'].data, date=datetime.utcnow(), description=form['description'].data)
    )
    db.session.commit()
