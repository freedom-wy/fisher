class BookViewModel(object):

    @classmethod
    def package_single(cls, data, keyword):
        """
        通过ISBN搜索的图书数据, 只有一本图书数据
        :param data: 原始数据
        :param keyword: 关键字
        :return: 统一的数据返回格式
        """
        return_data = {
            "books": [],
            "total": 0,
            "keyword": keyword
        }
        if data:
            return_data["total"] = 1
            return_data["books"] = [cls.__cut_boo_data(data)]
        return return_data

    @classmethod
    def package_collection(cls, data, keyword):
        """
        通过关键字搜索的图书数据, 返回多条图书数据
        :param data:
        :param keyword:
        :return:
        """
        return_data = {
            "books": [],
            "total": 0,
            "keyword": keyword
        }
        if data:
            return_data["total"] = data.get("total")
            return_data["books"] = [cls.__cut_boo_data(book) for book in data.get("books")]
        return return_data

    @classmethod
    def __cut_boo_data(cls, data):
        """
        裁剪图书数据
        :param data:
        :return:
        """
        book = {
            "title": data.get("title"),
            "publisher": data.get("publisher"),
            "pages": data.get("pages") or "",
            "author": "、".join(data.get("author")),
            "price": data.get("price"),
            "summary": data.get("summary") or "",
            "image": data.get("image")
        }
        return book
