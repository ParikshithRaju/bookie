import os
from forms import BookmarkForm
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import models
from datetime import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = "parikshithcr"

baseDir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(baseDir, "myDatabase.db")
db = SQLAlchemy(app)


@app.route('/index')
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/add', methods=['GET', 'POST'])
def addUrl():
    form = BookmarkForm()
    if form.validate_on_submit():
        db.session.add(
            models.BookmarkDB(url=form['url'].data,date=datetime.utcnow(),description=form['description'].data)
        )
        db.session.commit()
        flash('Successfully Added bookmark ' + form.description.data)
        return redirect(url_for('home'))
    return render_template('addUrlForm.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
