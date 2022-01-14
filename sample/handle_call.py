# 可调用对象

# 1、简化对象下方法的调用
# 2、模糊了对象和函数的区别
# 3、对象下只有一个方法


class A(object):
    def __init__(self, name):
        self.name = name

    def __call__(self, *args, **kwargs):
        print("名字为: {}".format(self.name))


a = A("张三")
a()
