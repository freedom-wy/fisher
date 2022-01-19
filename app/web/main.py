from flask import render_template, abort
from .blueprint import web
from app.models.gift import Gift
from app.view_models.book_view_models import SingleBookViewModel
from flask_login import login_required, current_user
from app.models.user import User
from app.view_models.drift_view_models import DriftInfo


@web.route('/')
def index():
    """
    # 通过礼物转换成图书数据
    :return:
    """
    # 获取符合要求的礼物数据
    recent_gifts = Gift.recent()
    books = [SingleBookViewModel(gift.book) for gift in recent_gifts]
    return render_template("index.html", recent=books)


@web.route('/personal')
@login_required
def personal_center():
    user = User.query.get_or_404(current_user.id)
    userinfo = DriftInfo(user=user)
    return render_template("personal.html", user=userinfo)
