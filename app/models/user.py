from sqlalchemy import Column, Integer, String, Boolean, Float
from werkzeug.security import generate_password_hash, check_password_hash

from .base import Base


class User(Base):
    id = Column(Integer, primary_key=True)
    nickname = Column(String(24), nullable=False)
    phone_number = Column(String(18), unique=True)
    email = Column(String(50), unique=True, nullable=False)
    _password = Column('password', String(128))
    confirmed = Column(Boolean, default=False)
    beans = Column(Float, default=0)
    send_counter = Column(Integer, default=0)
    receive_counter = Column(Integer, default=0)
    wx_open_id = Column(String(50))
    wx_name = Column(String(32))

    @property
    def password(self):
        """
        读取password的值
        :return:
        """
        return self._password

    @password.setter
    def password(self, raw):
        """
        设置密码的值
        :return:
        """
        self._password = generate_password_hash(raw)

    def check_password(self, raw):
        """
        校验密码
        :param raw:
        :return:
        """
        return check_password_hash(self._password, raw)
