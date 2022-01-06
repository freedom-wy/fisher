from .blueprint import web
from flask_login import login_required


@web.route('/my/gifts')
@login_required
def my_gifts():
    return "ok"


@web.route('/gifts/book/<isbn>')
def save_to_gifts(isbn):
    pass


@web.route('/gifts/<gid>/redraw')
def redraw_from_gifts(gid):
    pass



