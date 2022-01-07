from .blueprint import web
from flask_login import login_required, current_user
from app.models.gift import Gift
from app.libs.db_utils import db
from flask import current_app, flash
from app.libs.helper import check_can_save_to_list


@web.route('/my/gifts')
@login_required
def my_gifts():
    return "ok"


@web.route('/gifts/book/<isbn>')
# 用户必须登录后才能对图书进行赠送或索取
@login_required
def save_to_gifts(isbn):
    """
    赠送图书
    :param isbn:
    :return:
    """
    if check_can_save_to_list(isbn, current_user.id):
        gift = Gift()
        gift.isbn = isbn
        # 哪一个用户赠送的图书,current_user.id为当前访问页面的用户
        gift.uid = current_user.id
        current_user.beans += current_app.config.get("BEANS_UPLOAD_ONE_BOOK")
        db.session.add(gift)
        db.session.commit()
    else:
        flash("这本书已添加到你的赠送清单或已存在于你的心愿清单,请不要重复添加")
    return "OK"


@web.route('/gifts/<gid>/redraw')
def redraw_from_gifts(gid):
    pass



