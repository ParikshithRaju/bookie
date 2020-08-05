import sys
from datetime import datetime

sys.path.append('..')
sys.path.append('.')

from sqlalchemy import desc
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, login_required, current_user, logout_user

from bookie import app, db, bcrypt, login_manager
from models import bookmarkDB, userDB, tagDB
from forms import BookmarkForm, SignupForm, LoginForm


@login_manager.user_loader
def load_user(userid):
    return userDB.query.get(int(userid))


@app.route('/index')
@app.route('/')
def home():
    if current_user.is_authenticated:
        tagDict = current_user.getTagDict()
        sorted_dict = sorted(
            tagDict.items(),
            key=lambda x: x[1],
            reverse=True
        )
        most_used_tags_names=sorted_dict[:5]
        most_used_tags_objects=[tagDB.getTagByName(name[0]) for name in most_used_tags_names]
        return render_template('index.html', bookmarks=current_user.bookmarks.order_by(desc(bookmarkDB.date)).limit(3),
                               most_used_tags=most_used_tags_objects,
                               user=current_user)
    else:
        return render_template('index.html', user=current_user)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode()
        db.session.add(
            userDB(name=form.name.data, email=form.email.data, password=hashed_password)
        )
        db.session.commit()
        flash(f"{form.name.data} you are successfully signed up")
        return redirect(url_for('login'))
    return render_template("signup.html", form=form, user=current_user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = userDB.query.filter_by(email=form.email.data).first()
        login_user(user, form.remember_me.data)
        flash(f"{user.name} you are logged in successfully")
        return redirect(request.args.get('next') or url_for('home'))
    return render_template("login.html", form=form, user=current_user)


@app.route('/add', methods=['GET', 'POST'])
@login_required
def addUrl():
    form = BookmarkForm()
    if form.validate_on_submit():
        db.session.add(
            bookmarkDB(url=form['url'].data, date=datetime.utcnow(), description=form['description'].data
                       , tags=form['tags'].data, user=current_user)
        )
        db.session.commit()
        flash('Successfully Added bookmark ' + form.description.data)
        print(request.args)
        return redirect(url_for('home'))
    return render_template('addUrlForm.html', form=form, user=current_user, title="Add Bookmark")


@app.route('/edit/<int:bookmarkid>', methods=["GET", "POST"])
@login_required
def editUrl(bookmarkid):
    bookmark = bookmarkDB.query.get(bookmarkid)
    form = BookmarkForm(obj=bookmark)
    if form.validate_on_submit():
        form.populate_obj(bookmark)
        db.session.commit()
        flash("Successfully edited the bookmark")
        return redirect(url_for("user", userid=current_user.id))
    return render_template('addUrlForm.html', form=form, user=current_user, title="Edit bookmark")


@app.route('/user/<userid>')
@login_required
def user(userid):
    return render_template('userPage.html', user=userDB.query.get(userid))


@app.route('/tag/<int:tagid>')
@login_required
def tagView(tagid):
    return render_template('tagPage.html', user=current_user, tag=tagDB.query.get(tagid))
