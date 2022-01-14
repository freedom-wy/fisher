from sqlalchemy import Column, Integer, String, Boolean, Float
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from .base import Base
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from app.libs.db_utils import db


class User(UserMixin, Base):
    id = Column(Integer, primary_key=True)
    nickname = Column(String(24), nullable=False)
    phone_number = Column(String(18), unique=True)
    email = Column(String(50), unique=True, nullable=False)
    _password = Column('password', String(128), nullable=False)
    confirmed = Column(Boolean, default=False)
    # 鱼豆
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
        校验密码是否正确
        :param raw:
        :return:
        """
        return check_password_hash(self._password, raw)

    def generate_token(self):
        """
        生成重置密码中的token
        :return:
        """
        s = Serializer(current_app.config.get("SECRET_KEY"), current_app.config.get("TOKEN_EXPIRATION"))
        # 序列化
        return s.dumps({"id": self.id}).decode("utf-8")

    @staticmethod
    def reset_password(token, newpassword):
        """
        设置用户新密码
        :param newpassword:
        :return:
        """
        s = Serializer(current_app.config.get("SECRET_KEY"))
        # 反序列化
        try:
            data = s.loads(token.encode("utf-8"))
        except:
            # 解密token失败
            return False
        uid = data.get("id")
        # 设置新密码
        with db.auto_commit():
            user = User.query.get(uid)

            if user:
                user.password = newpassword
            else:
                return False
        return True
