from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, desc, func
from sqlalchemy.orm import relationship
from .base import Base
from .book import Book
from flask import current_app
from app.libs.db_utils import db


# 模型类必须创建,继承时不创建该表
class Wish(Base):
    """
    心愿清单
    """
    id = Column(Integer, primary_key=True)
    # 表示礼物是否已送出
    launched = Column(Boolean, default=False)
    # 用于记录这个礼物是由谁送出的
    # user = relationship("User")
    # uid = Column(Integer, ForeignKey('user.id'))
    uid = Column(Integer)
    # book = relationship("Book")
    # bid = Column(Integer, ForeignKey('book.id'))
    # 根据业务逻辑,在gift中的isbn可以重复
    isbn = Column(String(15), nullable=False)

    @property
    def book(self):
        """
        通过礼物查书,再转换成view_models
        :return:
        """
        return Book.query.filter_by(isbn=self.isbn).first().to_dict()

    @classmethod
    def recent(cls):
        """
        将gift表中前30条数据输出到首页
        去重
        排序
        :return:
        """
        # 关闭ONLY_FULL_GROUP_BY
        # mysql > set global sql_mode='STRICT_TRANS_TABLES,
        # NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION';
        # mysql > set session sql_mode = 'STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,
        # NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION';
        recent_gift = Wish.query.filter_by(launched=False).group_by(
            Wish.isbn).order_by(desc(Wish.create_time)).limit(
            current_app.config["RECENT_BOOK_COUNT"]).distinct().all()
        return recent_gift

    @classmethod
    def get_user_wishes(cls, uid):
        """
        获取这个用户的所有心愿
        :param uid:
        :return:
        """
        wishes = Wish.query.filter_by(uid=uid, launched=False).order_by(desc(Wish.create_time)).all()
        return wishes

    @classmethod
    def get_wish_counts(cls, isbn_list):
        """
        根据传入的isbn_list判断gift表中礼物数量
        通过isbn分组
        对分组的wish计数
        :param isbn_list:
        :return:
        """
        # 解决循环导入问题
        from .gift import Gift
        count_list = db.session.query(func.count(Gift.id), Gift.isbn).filter(
            Gift.launched == False, Gift.isbn.in_(isbn_list), Gift.status == 1).group_by(Gift.isbn).all()
        # 尽量以字典形式向外返回数据
        count_list = [{"count": w[0], "isbn": w[1]} for w in count_list]
        return count_list
