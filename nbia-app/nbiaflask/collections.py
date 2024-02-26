from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort


from nbiaflask.db import get_db

bp = Blueprint('collections', __name__)

@bp.route('/')
def index():
    db = get_db()
    collections = db.execute(
        'SELECT Collection'
        ' FROM collections'
        ' ORDER BY Collection'
    ).fetchall()
    return render_template('collections/index.html', collections=collections)