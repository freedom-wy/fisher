from .base import Base
from sqlalchemy import Column, SmallInteger, Integer, String
from app.libs.enums import PendingStatus


class Drift(Base):
    """
    一次交易的具体信息，向赠送者索要数据
    历史信息需要记录,不能时时更新,因此Drift模型类中的字段包含nickname等字段
    优点是可以减少查询
    缺点是容易数据不一致
    """
    id = Column(Integer, primary_key=True)
    # 邮寄信息,索要者提交的相关信息
    # 收件人姓名
    recipient_name = Column(String(20), nullable=False)
    address = Column(String(100), nullable=False)
    message = Column(String(200))
    mobile = Column(String(20), nullable=False)
    # 书籍信息
    isbn = Column(String(13))
    book_title = Column(String(50))
    book_author = Column(String(30))
    book_img = Column(String(50))
    # 赠送者相关信息
    gifter_id = Column(Integer)
    gift_id = Column(Integer)
    gifter_nickname = Column(String(20))
    # 索要者相关信息
    requester_id = Column(Integer)
    requester_nickname = Column(String(20))
    # 交易的4种状态
    _pending = Column("pending", SmallInteger, default=1)

    # 精妙代码
    @property
    def pending(self):
        # 数字类型转枚举类型
        return PendingStatus(self._pending)

    @pending.setter
    def pending(self, status):
        # 枚举类型转数字类型
        self._pending = status.value

