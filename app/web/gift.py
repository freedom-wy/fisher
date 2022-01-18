from .blueprint import web
from flask_login import login_required, current_user
from app.models.gift import Gift
from app.libs.db_utils import db
from flask import current_app, flash, redirect, url_for, render_template
from app.libs.helper import check_can_save_to_list
from app.models.drift import Drift
from app.view_models.trade_view_models import MyGiftWishInfo
from app.libs.enums import PendingStatus


@web.route('/my/gifts')
@login_required
def my_gifts():
    """
    1、查询当前用户所有礼物数据
    2、根据礼物数据获得所有心愿数据的数量
    :return:
    """
    mygifts_source_data = Gift.get_user_gifts(uid=current_user.id)
    isbn_list = [gift.isbn for gift in mygifts_source_data]
    wish_count_list = Gift.get_wish_counts(isbn_list)
    # 原始数据转换为view_model,便于模板渲染
    view_model = MyGiftWishInfo(mygifts_source_data, wish_count_list)
    return render_template("my_gifts.html", gifts=view_model.trades)


@web.route('/gifts/book/<isbn>')
# 用户必须登录后才能对图书进行赠送或索取
@login_required
def save_to_gifts(isbn):
    """
    赠送图书
    :param isbn:
    :return:
    """
    # 通过事物保持一致性
    if check_can_save_to_list(isbn, current_user.id):
        with db.auto_commit():
            gift = Gift()
            gift.isbn = isbn
            # 哪一个用户赠送的图书,current_user.id为当前访问页面的用户
            gift.uid = current_user.id
            current_user.beans += current_app.config.get("BEANS_UPLOAD_ONE_BOOK")
            db.session.add(gift)
    else:
        flash("这本书已添加到你的赠送清单或已存在于你的心愿清单,请不要重复添加")
    return redirect(url_for("web.book_detail", isbn=isbn))


@web.route('/gifts/<gid>/redraw')
@login_required
def redraw_from_gifts(gid):
    """
    撤销礼物
    :param gid:
    :return:
    """
    # 1、该礼物不能存在于鱼漂中
    # 2、扣除鱼豆,并删除该书籍
    drift = Drift.query.filter_by(gift_id=gid, pending=PendingStatus.Waiting).first_or_404()
    if drift:
        flash("该书籍正处于交易状态,请先前往鱼漂页面完成处理")
    else:
        gift = Gift.query.filter_by(id=gid, launched=False).first_or_404()
        with db.auto_commit():
            current_user.beans -= current_app.config.get("BEANS_UPLOAD_ONE_BOOK")
            gift.delete()
    return redirect(url_for("web.my_gifts"))




