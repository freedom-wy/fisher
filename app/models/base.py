from app.libs.db_utils import db
from sqlalchemy import Column, SmallInteger, Integer


class Base(db.Model):
    # 使用abstract属性,sqlalchemy将不创建base表
    __abstract__ = True
    # create_time = Column("create_time", Integer)
    status = Column(SmallInteger, default=1)
