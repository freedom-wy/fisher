from contextlib import contextmanager


class Mywith(object):
    def __init__(self, name):
        self.name = name

    def query(self):
        print(self.name)

    # def __enter__(self):
    #     """
    #     预处理操作
    #     :return:
    #     """
    #     print("预先处理")
    #     return self
    #
    # def __exit__(self, exc_type, exc_val, exc_tb):
    #     if exc_tb:
    #         print("异常原因: {}".format(exc_val))
    #     print("结束后处理")
    #     return True


@contextmanager
def make_mywith():
    print("预处理操作")
    yield Mywith(name="test1")
    print("结束后处理")


@contextmanager
def book_mark():
    print("《", end="")
    yield
    print("》", end="")


if __name__ == '__main__':
    # with Mywith(name="test1") as m:
    #     m.query()
    # with make_mywith() as m:
    #     m.query()
    with book_mark():
        print("明朝那些事", end="")
