from app.libs.http_helper import HTTP
from flask import current_app
from app.models.book import Book
from app.libs.db_utils import db


class YuShuBook(object):
    def __init__(self):
        self.total = 0
        self.books = []

    def __fill_single(self, data):
        """
        裁剪一本原始数据
        :param data:
        :return:
        """
        if data:
            self.total = 1
            self.books.append(data)

    def __fill_collection(self, data):
        """
        裁剪多本原始数据
        :param data:
        :return:
        """
        self.total = data.get("total")
        self.books = data.get("books")

    def search_by_isbn(self, isbn):
        # 先查库
        one_book = db.session.query(Book).filter(Book.isbn == isbn).first()
        if not one_book:
            url = current_app.config.get("YUSHU_ISBN_API").format(isbn)
            response = HTTP.get(url)
            self.__fill_single(data=response)
        else:
            self.__fill_single(data=one_book.to_dict())

    def __save_book_data_from_search_keyword(self, books):
        """
        存储通过关键字查询的数据,存储前先通过isbn查询
        :param books:
        :return:
        """
        with db.auto_commit():
            for i in books:
                save_book = Book()
                book = db.session.query(Book).filter(Book.isbn == i.get("isbn")).first()
                if not book:
                    save_book.set_attrs(i)
                    db.session.add(save_book)

    def search_by_keyword(self, keyword, page=1):
        url = current_app.config.get("YUSHU_KEYWORD_API").format(keyword, current_app.config.get("PER_PAGE_DATA_COUNT"),
                                                                 self.calculator_start(page))
        response = HTTP.get(url)
        if response:
            self.__save_book_data_from_search_keyword(books=response.get("books"))
            self.__fill_collection(data=response)

    @staticmethod
    def calculator_start(page):
        # 计算数据起始
        return (page - 1) * current_app.config.get("PER_PAGE_DATA_COUNT")

    # 精妙代码
    @property
    def first(self):
        return self.books[0] if self.total >= 1 else None


if __name__ == '__main__':
    from app import create_app
    app = create_app()
    with app.app_context():
        test_yushu = YuShuBook()
        test_yushu.search_by_keyword(keyword="西游记")
        # test_yushu.search_by_isbn(isbn="9787805200552")
        print(test_yushu.books)
