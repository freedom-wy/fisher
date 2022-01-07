from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


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
