from flask import Flask

app = Flask(__name__)


@app.route("/book/search/<q>/<page>")
def search(q, page):
    """
    搜索图书
    :param q: 搜索关键字或搜索的ISBN号码, ISBN10为10位数字,可能包含-,ISBN13为13位数字
    :param page: 页码
    :return:
    """
    key_or_isbn = "key"
    if len(q) == 13 and q.isdigit():
        key_or_isbn = "isbn"
    short_q = q.replace('-', "")
    if len(q) == 10 and len(short_q) and short_q.isdigit():
        key_or_isbn = "isbn"
    return key_or_isbn


@app.route("/")
def hello_world():
    return "Hello World!"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
