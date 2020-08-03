import sys
from datetime import datetime

sys.path.append('..')
sys.path.append('.')

from flask import render_template, flash, redirect, url_for

from bookie import app, db
from models import BookmarkDB
from forms import BookmarkForm


@app.route('/index')
@app.route('/')
def home():
    return render_template('index.html', newest=BookmarkDB.newest(3).all())


@app.route('/add', methods=['GET', 'POST'])
def addUrl():
    form = BookmarkForm()
    if form.validate_on_submit():
        db.session.add(
            BookmarkDB(url=form['url'].data, date=datetime.utcnow(), description=form['description'].data)
        )
        db.session.commit()
        flash('Successfully Added bookmark ' + form.description.data)
        return redirect(url_for('home'))
    return render_template('addUrlForm.html', form=form)
