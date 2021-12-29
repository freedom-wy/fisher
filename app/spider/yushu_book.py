from app.libs.http_helper import HTTP
from flask import current_app


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
        url = current_app.config.get("YUSHU_ISBN_API").format(isbn)
        response = HTTP.get(url)
        self.__fill_single(data=response)

    def search_by_keyword(self, keyword, page=1):
        url = current_app.config.get("YUSHU_KEYWORD_API").format(keyword, current_app.config.get("PER_PAGE_DATA_COUNT"),
                                                                 self.calculator_start(page))
        response = HTTP.get(url)
        self.__fill_collection(data=response)

    @staticmethod
    def calculator_start(page):
        # 计算数据起始
        return (page - 1) * current_app.config.get("PER_PAGE_DATA_COUNT")

    @property
    def first(self):
        return self.books[0] if self.total >= 1 else None
