from flask import jsonify
from helper import is_isbn_or_key
from yushu_book import YuShuBook
from .book_blueprint import book_bp


@book_bp.route("/book/search/<q>/<page>")
def search(q, page):
    """
    搜索图书
    :param q: 搜索关键字或搜索的ISBN号码, ISBN10为10位数字,可能包含-,ISBN13为13位数字
    :param page: 页码
    :return:
    """
    isbn_or_key = is_isbn_or_key(q)
    if isbn_or_key == "isbn":
        result = YuShuBook.search_by_isbn(q)
    else:
        result = YuShuBook.search_by_keyword(q)
    return jsonify(result)
