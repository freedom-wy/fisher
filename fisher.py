from flask import Flask, jsonify
from helper import is_isbn_or_key
from yushu_book import YuShuBook

app = Flask(__name__)


@app.route("/book/search/<q>/<page>")
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

    pass


@app.route("/")
def hello_world():
    return "Hello World!"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
