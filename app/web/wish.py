from .blueprint import web
from app.libs.helper import check_can_save_to_list
from flask_login import current_user, login_required
from app.libs.db_utils import db
from app.models.wish import Wish
from flask import flash, redirect, url_for, render_template
from app.view_models.trade_view_models import MyGiftWishInfo


@web.route('/my/wish')
@login_required
def my_wish():
    mywishes_source_data = Wish.get_user_wishes(uid=current_user.id)
    isbn_list = [wish.isbn for wish in mywishes_source_data]
    gift_count_list = Wish.get_wish_counts(isbn_list)
    # 原始数据转换为view_model,便于模板渲染
    view_model = MyGiftWishInfo(mywishes_source_data, gift_count_list)
    return render_template("my_wish.html", wishes=view_model.trades)


@web.route('/wish/book/<isbn>')
@login_required
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
