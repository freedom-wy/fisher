from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, desc
from sqlalchemy.orm import relationship
from .base import Base
from .book import Book
from flask import current_app


class Gift(Base):
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
        recent_gift = Gift.query.filter_by(launched=False).group_by(
            Gift.isbn).order_by(desc(Gift.create_time)).limit(
            current_app.config["RECENT_BOOK_COUNT"]).distinct().all()
        return recent_gift
