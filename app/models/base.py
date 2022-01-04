from app.libs.db_utils import db
from sqlalchemy import Column, SmallInteger, Integer


class Base(db.Model):
    # create_time = Column("create_time", Integer)
    status = Column(SmallInteger, default=1)
