from app.libs.db_utils import db
from sqlalchemy import Column, SmallInteger, Integer
from datetime import datetime


class Base(db.Model):
    # 使用abstract属性,sqlalchemy将不创建base表
    __abstract__ = True
    create_time = Column("create_time", Integer)
    status = Column(SmallInteger, default=1)

    def __init__(self):
        self.create_time = int(datetime.now().timestamp())

    # 精妙代码
    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}

    # 精妙代码
    def set_attrs(self, attrs_dict):
        """
        保存数据到模型类中,继而保存到数据库中
        :param attrs_dict:
        :return:
        """
        for key, value in attrs_dict.items():
            # 判断是否有key这个属性
            if hasattr(self, key) and key != "id":
                value = "、".join(value) if isinstance(value, list) else value
                # 设置属性的值
                setattr(self, key, value)

    @property
    def create_datetime(self):
        if self.create_time:
            return datetime.fromtimestamp(self.create_time)
        else:
            return None