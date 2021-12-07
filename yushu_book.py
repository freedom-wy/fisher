from http import HTTP


class YuShuBook(object):
    isbn_url = ""
    keyword_url = ""

    @classmethod
    def search_by_isbn(cls, isbn):
        url = cls.isbn_url
        response = HTTP.get(url)
        return response

    @classmethod
    def search_by_keyword(cls, keyword, count=15, start=0):
        url = cls.keyword_url
        response = HTTP.get(url)
        return response
