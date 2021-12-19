from flask import jsonify, request
from app.libs.helper import is_isbn_or_key
from app.spider.yushu_book import YuShuBook
from .blueprint import book_bp
from app.forms.args_verification import searchArgsVerification


@book_bp.route("/book/search")
def search():
    """
    搜索图书
    :param q: 搜索关键字或搜索的ISBN号码, ISBN10为10位数字,可能包含-,ISBN13为13位数字
    :param page: 页码
    :return:
    """
    search_args_verification = searchArgsVerification(request.args)
    if search_args_verification.validate():
        q = search_args_verification.q.data.strip()
        page = search_args_verification.page.data
        isbn_or_key = is_isbn_or_key(q)
        if isbn_or_key == "isbn":
            result = YuShuBook.search_by_isbn(q)
        else:
            result = YuShuBook.search_by_keyword(q, page=page)
        return jsonify(result)
    else:
        return jsonify({"message": "搜索参数校验失败"})