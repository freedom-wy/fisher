from .blueprint import web
from flask_login import login_required, current_user
from app.models.gift import Gift
from flask import flash, redirect, url_for, render_template, request
from app.view_models.drift_view_models import DriftInfo
from app.models.user import User
from app.forms.drift_auth import DriftForm
from app.libs.db_utils import db
from app.models.drift import Drift
from app.models.book import Book
from app.libs.email_utils import handle_send_mail
from sqlalchemy import desc, or_
from app.view_models.drift_view_models import DriftCollection
from app.libs.enums import PendingStatus
from app.models.wish import Wish


@web.route('/drift/<int:gid>', methods=['GET', 'POST'])
@login_required
def send_drift(gid):
    """
    向他人索要图书
    1、自己不能向自己请求书籍
    2、索要者的鱼豆必须大于或等于1
    3、每索取两本书，自己必须送出一本书
    :param gid: 礼物id,在templates文件中传递过来的
    :return:
    """
    drift_form = DriftForm(request.form)
    # 图书关联的赠送者信息和索要者信息
    current_gift = Gift.query.get_or_404(gid)
    # 自己不能向自己请求书籍
    if current_gift.is_yourself_gift(current_user.id):
        flash("不能向自己索要书籍")
        return redirect(url_for("web.book_detail", isbn=current_gift.isbn))
    can_send = current_user.can_send_drift()
    if not can_send:
        return render_template("not_enough_beans.html", beans=current_user.beans)

    gifter = User.query.get_or_404(current_gift.uid)
    book = Book.query.filter_by(isbn=current_gift.isbn).first()
    current_gift.nickname = gifter.nickname
    current_gift.book_title = book.title

    # 邮寄信息
    if request.method == "POST" and drift_form.validate():
        # 将页面数据保存到drift表中
        save_drift(drift_form, current_gift)
        # 向赠送者发送消息
        handle_send_mail(to=gifter.email, subject="有人想要一本书",
                         template="email/get_gift.html", wisher=current_user, gift=current_gift)
        # 跳转到鱼漂页面
        return redirect(url_for("web.pending"))
    # 可以通过view_model也可以通过字典组装数据
    gifterinfo = DriftInfo(user=gifter)
    return render_template("drift.html", gifter=gifterinfo, user_beans=current_user.beans, form=drift_form)


@web.route('/pending')
@login_required
def pending():
    """
    鱼漂页面
    :return:
    """
    # 查询drift表中数据并根据要求展示
    drifts = Drift.query.filter(
        or_(Drift.requester_id == current_user.id, Drift.gifter_id == current_user.id)).order_by(
        desc(Drift.create_time)).all()
    views = DriftCollection(drifts, current_user.id)
    return render_template("pending.html", drifts=views.data)


@web.route('/drift/<int:did>/reject')
@login_required
def reject_drift(did):
    """
    赠送者拒绝
    :param did:
    :return:
    """
    with db.auto_commit():
        drift = Drift.query.filter_by(id=did, gifter_id=current_user.id).first_or_404()
        drift.pending = PendingStatus.Reject
        # 将鱼豆返还给请求者
        requester = User.query.get_or_404(drift.requester_id)
        requester.beans += 1
    return redirect(url_for("web.pending"))


@web.route('/drift/<int:did>/redraw')
@login_required
def redraw_drift(did):
    """
    鱼漂撤销
    :param did:
    :return:
    """
    # 修改鱼漂中条目状态
    with db.auto_commit():
        # 撤销只有请求者中存在
        drift = Drift.query.filter_by(id=did, requester_id=current_user.id).first_or_404()
        drift.pending = PendingStatus.Redraw
        # 由于撤销,归还鱼豆
        current_user.beans += 1
    return redirect(url_for("web.pending"))


@web.route('/drift/<int:did>/mailed')
@login_required
def mailed_drift(did):
    """
    赠送者邮寄
    :param did:
    :return:
    """
    with db.auto_commit():
        # 1、修改drift表中pending状态
        drift = Drift.query.filter_by(id=did, gifter_id=current_user.id).first_or_404()
        drift.pending = PendingStatus.Success
        # 2、向赠送者发放1个鱼豆
        current_user.beans += 1
        # 3、修改心愿清单和赠送清单中launched状态
        gift = Gift.query.filter_by(id=drift.gift_id).first_or_404()
        gift.launched = True
        wish = Wish.query.filter_by(isbn=drift.isbn, uid=drift.requester_id).first_or_404()
        wish.launched = True
    return redirect(url_for("web.pending"))


def save_drift(drift_form, current_gift):
    """
    # 邮寄信息,索要者提交的相关信息
    recipient_name, address, message, mobile
    # 书籍信息
    isbn, book_title, book_author, book_img
    # 赠送者相关信息
    gifter_id, gift_id, gifter_nickname
    # 索要者相关信息
    requester_id, requester_nickname
    # 交易
    pending
    :return:
    """
    with db.auto_commit():
        drift = Drift()
        # 保存索要者提交的信息
        drift.set_attrs(drift_form.data)
        # 保存书籍信息
        book = Book.query.filter_by(isbn=current_gift.isbn).first().to_dict()
        drift.isbn = book.get("isbn")
        drift.book_title = book.get("title")
        drift.book_author = book.get("author")
        drift.book_img = book.get("image")
        # 保存赠送者相关信息
        user = User.query.get_or_404(current_gift.uid).to_dict()
        drift.gifter_id = current_gift.uid
        drift.gift_id = current_gift.id
        drift.gifter_nickname = user.get("nickname")
        # 保存索要者信息
        drift.requester_id = current_user.id
        drift.requester_nickname = current_user.nickname
        # 扣除鱼豆
        current_user.beans -= 1
        db.session.add(drift)
