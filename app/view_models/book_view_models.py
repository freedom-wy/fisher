# 精妙代码
class SingleBookViewModel(object):
    def __init__(self, book):
        self.title = book.get("title")
        self.publisher = book.get("publisher")
        self.author = "、".join(book.get("author")) if isinstance(book.get("author"), list) else book.get("author")
        # self.author = book.get("author")
        self.image = book.get("image")
        self.price = book.get("price")
        self.summary = book.get("summary")
        self.pages = book.get("pages")
        self.isbn = book.get("isbn")

    # property通过属性方式访问该方法,实例.intro
    # 精妙代码
    @property
    def intro(self):
        intros = filter(lambda x: True if x else False, [self.author, self.publisher, self.price])
        return "/".join(intros)


class CollectionBookViewModel(object):
    def __init__(self):
        self.total = 0
        self.books = []
        self.keyword = None

    def fill(self, yushu_book, keyword):
        self.total = yushu_book.total
        self.keyword = keyword
        self.books = [SingleBookViewModel(book) for book in yushu_book.books]
