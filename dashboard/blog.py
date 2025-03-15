from flask import Blueprint, flash, g, redirect, render_template, request, url_for, session
from werkzeug.exceptions import abort
from .auth import *
from .db import *
from .forms import *
from .models import *
from sqlalchemy import select, update
from sqlalchemy.orm import Session

__all__ = ['index', 'create', 'get_post', 'update', 'delete']

bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
    with Session(get_db()) as db:
        posts = db.scalars(select(Post).order_by(Post.created.desc()), execution_options={"prebuffer_rows": True})

    return render_template('blog/index.html', posts=posts)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    form = AddPostForm()
    error = None

    if request.method == 'POST':

        user_id = session.get('user_id')

        if not form.title.data:
            error = 'Title is required.'
        elif not form.body.data:
            error = 'Body is required.'

        if error is None:
            with Session(get_db()) as db:
                author = db.scalar(select(User).where(User.id == user_id))
                db.add(Post(form.title.data, form.body.data, author.id, author.username))
                db.commit()

        return redirect(url_for('blog.index'))
    
    flash(error)
    
    return render_template('blog/create.html')


def get_post(id, check_author=True):
    with Session(get_db()) as db:
        post = db.scalar(select(Post).join(User).where(Post.id == id), execution_options={"prebuffer_rows": True})

        if post is None:
            abort(404, f"Post id {id} doesn't exist.")

        user_id = session.get('user_id')
        if check_author and post.author_id != user_id:
            abort(403)

        return post


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    form = EditPostForm()
    error = None

    with Session(get_db()) as db:
        post = get_post(id)

        if request.method == 'POST':
            if not form.title.data:
                error = 'Title is required.'
            elif not form.body.data:
                error = 'Body is required.'

            if error is None:
                post.title = form.title.data
                post.body = form.body.data
                db.add(post)
                db.commit()

            return redirect(url_for('blog.index'))
            
        flash(error)
        
        return render_template('blog/update.html', post=post)
    

@bp.route('/<int:id>/delete', methods=('GET', 'POST'))
@login_required
def delete(id):

    with Session(get_db()) as db:
        post = get_post(id)

        if request.method == 'POST':
            db.delete(post)
            db.commit()
            
            return redirect(url_for('blog.index'))
            
    return render_template('blog/delete.html', post=post)