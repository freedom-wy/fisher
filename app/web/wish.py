from .blueprint import web
from app.libs.helper import check_can_save_to_list
from flask_login import current_user
from app.libs.db_utils import db
from app.models.wish import Wish
from flask import flash, redirect, url_for


@web.route('/my/wish')
def my_wish():
    pass


@web.route('/wish/book/<isbn>')
def save_to_wish(isbn):
    # 通过事物保持一致性
    if check_can_save_to_list(isbn, current_user.id):
        with db.auto_commit():
            wish = Wish()
            wish.isbn = isbn
            # 哪一个用户赠送的图书,current_user.id为当前访问页面的用户
            wish.uid = current_user.id
            db.session.add(wish)
    else:
        flash("这本书已添加到你的赠送清单或已存在于你的心愿清单,请不要重复添加")
    return redirect(url_for("web.book_detail", isbn=isbn))


@web.route('/satisfy/wish/<int:wid>')
def satisfy_wish(wid):
    pass


@web.route('/wish/book/<isbn>/redraw')
def redraw_from_wish(isbn):
    pass
