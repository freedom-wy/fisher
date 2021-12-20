from flask import jsonify, request
from app.libs.helper import is_isbn_or_key
from app.spider.yushu_book import YuShuBook
from .blueprint import book_bp
from app.forms.args_verification import searchArgsVerification
from app.view_models.book_view_models import BookViewModel


@book_bp.route("/book/search")
def search():
    """
    搜索图书
    :param q: 搜索关键字或搜索的ISBN号码, ISBN10为10位数字,可能包含-,ISBN13为13位数字
    :param page: 页码
    :return:
    """
    search_args_verification = searchArgsVerification(request.args)
    if search_args_verification.validate():
        q = search_args_verification.q.data.strip()
        page = search_args_verification.page.data
        isbn_or_key = is_isbn_or_key(q)
        if isbn_or_key == "isbn":
            # 此处可以判断数据库中是否包含图书数据,如包含图书数据直接返回,如不包含则通过API获取并保存入库
            result = YuShuBook.search_by_isbn(q)
            result = BookViewModel.package_single(data=result, keyword=q)
        else:
            result = YuShuBook.search_by_keyword(q, page=page)
            result = BookViewModel.package_collection(data=result, keyword=q)
        return jsonify(result)
    else:
        return jsonify({"message": "搜索参数校验失败"})
