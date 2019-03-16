from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog', __name__)


@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/index.html', posts=posts)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')


@bp.route('/<int:id>/view', methods=('GET', 'POST'))
def view(id, choose_like=None, choose_unlike=None, comment=None):
    post = get_post(id, check_author=False)
    return render_template('blog/view.html', post=post)


@bp.route('/<int:id>/like', methods=('POST',))
@login_required
def user_like(id):
    post = get_post(id, check_author=False)
    feedback = get_feedback(id, g.user['id'])
    db = get_db()

    if feedback is None:
        db.execute(
            'INSERT INTO feedback (post_id, author_id, like)'
            ' VALUES (?, ?, ?)',
            (id, g.user['id'], 1)
        )
        thumbsup = post['thumbsup'] + 1
        db.execute(
            'UPDATE post SET thumbsup = ? WHERE id = ?', (thumbsup, id)
        )
        db.commit()
        post = get_post(id, check_author=False)
    else:
        like, unlike, thumbsup, thumbsdown = feedback['like'], feedback['unlike'], post['thumbsup'], post['thumbsdown']
        if like:  # `if like is True` will cause error behavior
            like = 0
            thumbsup -= 1
        else:
            like = 1
            thumbsup += 1
            if unlike:
                unlike = 0
                thumbsdown -= 1
        db.execute(
            'UPDATE feedback SET like = ?, unlike = ?'
            ' WHERE post_id = ? AND author_id = ?',
            (like, unlike, id, g.user['id'])
        )
        db.execute(
            'UPDATE post SET thumbsup = ?, thumbsdown = ?'
            ' WHERE id = ?',
            (thumbsup, thumbsdown, id)
        )
        db.commit()

    post = get_post(id, check_author=False)
    return render_template('blog/view.html', post=post)


@bp.route('/<int:id>/unlike', methods=('POST',))
@login_required
def user_unlike(id):
    post = get_post(id, check_author=False)
    feedback = get_feedback(id, g.user['id'])
    db = get_db()

    if feedback is None:
        db.execute(
            'INSERT INTO feedback (post_id, author_id, unlike)'
            ' VALUES (?, ?, ?)',
            (id, g.user['id'], 1)
        )
        thumbsdown = post['thumbsdown'] + 1
        db.execute(
            'UPDATE post SET thumbsdown = ? WHERE id = ?', (thumbsdown, id)
        )
        db.commit()
        post = get_post(id, check_author=False)
    else:
        like, unlike, thumbsup, thumbsdown = feedback['like'], feedback['unlike'], post['thumbsup'], post['thumbsdown']
        print (like, unlike, thumbsup, thumbsdown)
        if unlike:
            unlike = 0
            thumbsdown -= 1
        else:
            unlike = 1
            thumbsdown += 1
            if like:
                like = 0
                thumbsup -= 1
        db.execute(
            'UPDATE feedback SET like = ?, unlike = ?'
            ' WHERE post_id = ? AND author_id = ?',
            (like, unlike, id, g.user['id'])
        )
        db.execute(
            'UPDATE post SET thumbsup = ?, thumbsdown = ?'
            ' WHERE id = ?',
            (thumbsup, thumbsdown, id)
        )
        db.commit()

    post = get_post(id, check_author=False)
    return render_template('blog/view.html', post=post)


def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username, thumbsup, thumbsdown'
        ' FROM post p JOIN user u on p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post


def get_feedback(post_id, user_id):
    feedback = get_db().execute(
        'SELECT like, unlike, comment'
        ' FROM feedback WHERE post_id = ? AND author_id = ?',
        (post_id, user_id)
    ).fetchone()

    return feedback


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.execute('DELETE FROM feedback WHERE post_id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))
