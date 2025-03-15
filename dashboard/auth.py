import functools
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from .forms import *
from .models import *
from .db import *
from sqlalchemy import select
from sqlalchemy.orm import Session

__all__ = ['register', 'login', 'load_logged_in_user', 'logout', 'login_required']

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    form = AddUserForm()
    error = None

    if request.method == 'POST':

        if not form.username.data:
            error = 'Username is required.'
        elif not form.password.data:
            error = 'Password is required.'

        if error is None:
            with Session(get_db()) as db:
                try:
                    db.add(User(form.username.data, generate_password_hash(form.password.data), None, form.first_name.data, form.last_name.data, form.email_address.data))
                    db.commit()
                except:
                    error = f'User {form.username.data} is already registered.'
        
        return redirect(url_for('auth.login'))
        
        flash(error)

    return render_template('auth/register.html', form=form, error=error)


@bp.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    error = None

    if request.method == 'POST':
        
        if not form.username.data:
            error = 'Username is required.'
        elif not form.password.data:
            error = 'Password is required.'

        with Session(get_db()) as db:
            user = db.scalar(select(User).where(User.username == form.username.data))

            if user is None:
                error = 'Incorrect username.'
            elif not check_password_hash(user.password, form.password.data):
                error = 'Incorrect password.'

            if error is None:
                session.clear()
                session['user_id'] = user.id
                return redirect(url_for('blog.index'))
        
        flash(error)

    return render_template('auth/login.html', form=form, error=error)


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        with Session(get_db()) as db:
            g.user = db.scalar(select(User).where(User.id == user_id))


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        
        return view(**kwargs)
    
    return wrapped_view