# 精妙代码
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy
from contextlib import contextmanager


class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        """
        利用上下文管理器提交代码并判断是否有异常
        :return:
        """
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e


db = SQLAlchemy()
