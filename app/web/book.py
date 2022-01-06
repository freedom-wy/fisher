from flask import request, render_template, flash
from app.libs.helper import is_isbn_or_key
from app.spider.yushu_book import YuShuBook
from .blueprint import web
from app.forms.args_verification import searchArgsVerification
from app.view_models.book_view_models import CollectionBookViewModel, SingleBookViewModel
from app.models.book import Book


@web.route("/book/search")
def search():
    search_args_verification = searchArgsVerification(request.args)
    books = CollectionBookViewModel()

    if search_args_verification.validate():
        q = search_args_verification.q.data.strip()
        page = search_args_verification.page.data
        isbn_or_key = is_isbn_or_key(q)
        # 实例化请求爬虫类
        yushu_book = YuShuBook()

        if isbn_or_key == "isbn":
            # 此处可以判断数据库中是否包含图书数据,如包含图书数据直接返回,如不包含则通过API获取并保存入库
            if yushu_book.db_first(isbn=q):
                yushu_book.search_by_isbn_from_db(isbn=q)
            else:
                yushu_book.search_by_isbn(q)
        else:
            yushu_book.search_by_keyword(q, page)

        # 格式化数据
        books.fill(yushu_book, q)
        # 序列化为字典
        # return json.dumps(books, default=lambda o: o.__dict__)
    else:
        # return jsonify({"message": "搜索参数校验失败"})
        # 使用flask消息闪现时，需要配置secret_key
        flash("搜索的关键字不符合要求,请重新输入关键字")
    # 无论有没有搜索结果,都要return
    return render_template("search_result.html", books=books)


@web.route('/book/<isbn>/detail')
def book_detail(isbn):
    search_book = YuShuBook()
    # 首先查库,如库中不存在则通过接口访问
    book = Book.query.filter_by(isbn=isbn).first()
    if book:
        single_book_class = SingleBookViewModel(book=book.to_dict())
    else:
        # 取一本书可以更优雅些
        search_book.search_by_isbn(isbn=isbn)
        single_book_class = SingleBookViewModel(book=search_book.first)
    return render_template("book_detail.html", book=single_book_class, wishes=[], gifts=[])