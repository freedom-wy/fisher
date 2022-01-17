from .blueprint import web
from flask_login import login_required, current_user
from ..models.gift import Gift
from flask import flash, redirect, url_for, render_template
from app.view_models.drift_view_models import DriftInfo
from app.models.user import User


@web.route('/drift/<int:gid>', methods=['GET', 'POST'])
@login_required
def send_drift(gid):
    """
    向他人索要图书
    1、自己不能向自己请求书籍
    2、索要者的鱼豆必须大于或等于1
    3、每索取两本书，自己必须送出一本书
    :param gid: 礼物id
    :return:
    """
    current_gift = Gift.query.get_or_404(gid)
    # 自己不能向自己请求书籍
    if current_gift.is_yourself_gift(current_user.id):
        flash("不能向自己索要书籍")
        return redirect(url_for("web.book_detail", isbn=current_gift.isbn))
    can_send = current_user.can_send_drift()
    if not can_send:
        return render_template("not_enough_beans.html", beans=current_user.beans)
    gifter = User.query.get_or_404(current_gift.uid)
    gifterinfo = DriftInfo(user=gifter)
    return render_template("drift.html", gifter=gifterinfo, user_beans=current_user.beans)


@web.route('/pending')
def pending():
    pass


@web.route('/drift/<int:did>/reject')
def reject_drift(did):
    pass


@web.route('/drift/<int:did>/redraw')
def redraw_drift(did):
    pass


@web.route('/drift/<int:did>/mailed')
def mailed_drift(did):
    pass
