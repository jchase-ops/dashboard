import calendar
from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort
from .auth import *
from .db import get_db
from .models import *
from sqlalchemy import select
from sqlalchemy.orm import Session
from datetime import datetime

__all__ = ['home']

bp = Blueprint('calendar', __name__, url_prefix='/calendar')

@bp.route('/month')
@login_required
def month():
    error = None

    today = datetime(datetime.now().year, datetime.now().month, datetime.now().day)
    month_calendar_iter = calendar.Calendar(firstweekday=6).itermonthdates(today.year, today.month)
    month_calendar = []
    for x in month_calendar_iter:
        month_calendar.append(x)

    if error is not None:
        flash(error)

    return render_template('calendar/month.html', today=today, month_calendar=month_calendar)

