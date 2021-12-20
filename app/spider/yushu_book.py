from app.libs.http_helper import HTTP
from flask import current_app


class YuShuBook(object):

    @classmethod
    def search_by_isbn(cls, isbn):
        # 此处可以判断数据库中是否包含图书数据,如包含图书数据直接返回,如不包含则通过API获取并保存入库
        url = current_app.config.get("YUSHU_ISBN_API").format(isbn)
        response = HTTP.get(url)
        return response

    @classmethod
    def search_by_keyword(cls, keyword, page=1):
        url = current_app.config.get("YUSHU_KEYWORD_API").format(keyword, current_app.config.get("PER_PAGE_DATA_COUNT"), cls.calculator_start(page))
        response = HTTP.get(url)
        return response

    @staticmethod
    def calculator_start(page):
        # 计算数据起始
        return (page - 1) * current_app.config.get("PER_PAGE_DATA_COUNT")
