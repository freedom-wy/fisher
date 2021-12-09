from http_helper import HTTP
from flask import current_app


class YuShuBook(object):
    isbn_url = current_app.config.get("YUSHU_ISBN_API")
    keyword_url = current_app.config.get("YUSHU_KEYWORD_API")

    @classmethod
    def search_by_isbn(cls, isbn):
        url = cls.isbn_url.format(isbn)
        response = HTTP.get(url)
        return response

    @classmethod
    def search_by_keyword(cls, keyword, count=15, start=0):
        url = cls.keyword_url.format(keyword, count, start)
        response = HTTP.get(url)
        return response
