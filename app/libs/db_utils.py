# 精妙代码
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery
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


# 所有的filter_by方法中需要传入status=1,因此需要重写filter_by方法
class Query(BaseQuery):
    def filter_by(self, **kwargs):
        if 'status' not in kwargs.keys():
            kwargs["status"] = 1
        return super(Query, self).filter_by(**kwargs)


db = SQLAlchemy(query_class=Query)
