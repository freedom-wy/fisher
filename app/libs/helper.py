from app.spider.yushu_book import YuShuBook
from app.models.gift import Gift
from app.models.wish import Wish


def is_isbn_or_key(q):
    key_or_isbn = "key"
    if len(q) == 13 and q.isdigit():
        key_or_isbn = "isbn"
    short_q = q.replace('-', "")
    if len(q) == 10 and len(short_q) and short_q.isdigit():
        key_or_isbn = "isbn"
    return key_or_isbn


def check_can_save_to_list(isbn, uid):
    # 判断是否为isbn编号
    if is_isbn_or_key(q=isbn) != "isbn":
        return False
    # 判断平台中是否有该本图书
    book = YuShuBook()
    book.search_by_isbn(isbn)
    if not book.first:
        return False
    # 该本图书不能在赠送清单中，也不能在心愿清单中
    gifting = Gift.query.filter_by(uid=uid, isbn=isbn, launched=False).first()
    wishing = Wish.query.filter_by(uid=uid, isbn=isbn, launched=False).first()
    if not gifting and not wishing:
        return True
    else:
        return False
