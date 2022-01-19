from .blueprint import web
from app.libs.helper import check_can_save_to_list
from flask_login import current_user, login_required
from app.libs.db_utils import db
from app.models.wish import Wish
from flask import flash, redirect, url_for, render_template, request
from app.view_models.trade_view_models import MyGiftWishInfo
from app.models.gift import Gift
from app.libs.email_utils import handle_send_mail
from app.models.user import User
from app.models.book import Book


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
    """
    向他赠送书籍
    :param wid:
    :return:
    """
    # 1、确认心愿表中有该图书数据
    # 2、确认自己能够送出这本书(上传了这本书)
    # 3、向对方发送邮件,对方点击邮件后会向web.send_drift发送请求,创建一个鱼漂
    wish = Wish.query.get_or_404(wid)
    isbn = request.args.get("isbn")
    if isbn != wish.isbn:
        flash("ISBN号码不符")
    else:
        gift = Gift.query.filter_by(uid=current_user.id, isbn=wish.isbn).first_or_404()
        if not gift:
            flash("你还没有上传此书,请点击加入到赠送清单添加此书,添加前请确认自己可以赠送此书")
        else:
            # 有书发送邮件
            user = User.query.get_or_404(wish.uid)
            if user:
                email = user.email
                wish.nickname = user.nickname
                gift.nickname = current_user.nickname
                wish.book_title = Book.query.filter_by(isbn=isbn).first_or_404().title
                handle_send_mail(to=email, subject="有人想送你一本书", template="email/satisify_wish.html", wish=wish,
                                 gift=gift)
                flash("已向{nickname}发送了一封电子邮件,如果{nickname}愿意接受你的赠送，你将收到一个鱼漂".format(nickname=user.nickname))
    return redirect(url_for("web.book_detail", isbn=isbn))


@web.route('/wish/book/<isbn>/redraw')
@login_required
def redraw_from_wish(isbn):
    wish = Wish.query.filter_by(isbn=isbn, launched=False, uid=current_user.id).first_or_404()
    with db.auto_commit():
        wish.delete()
    return redirect(url_for("web.my_wish"))
