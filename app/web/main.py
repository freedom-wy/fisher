from flask import render_template
from .blueprint import web
from app.models.gift import Gift
from app.view_models.book_view_models import SingleBookViewModel


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
def personal_center():
    return 'personal'
