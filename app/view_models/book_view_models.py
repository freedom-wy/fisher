class SingleBookViewModel(object):
    def __init__(self, book):
        self.title = book.get("title")
        self.publisher = book.get("publisher")
        self.author = "、".join(book.get("author"))
        self.image = book.get("image")
        self.price = book.get("price")
        self.summary = book.get("summary")
        self.pages = book.get("pages")
        self.isbn = book.get("isbn")


class CollectionBookViewModel(object):
    def __init__(self):
        self.total = 0
        self.books = []
        self.keyword = None

    def fill(self, yushu_book, keyword):
        self.total = yushu_book.total
        self.keyword = keyword
        self.books = [SingleBookViewModel(book) for book in yushu_book.books]
