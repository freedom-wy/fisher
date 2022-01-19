"""
hasattr判断对象中是否存在name属性或方法
getattr用于获取对象属性或方法,如果获取的是属性,如属性不存在则判断是否有默认值,如属性存在则输出属性值,如获取的是方法,则输出方法地址,后面加括号则可以运行方法
setattr给对象属性赋值,如果属性不存在,则创建该属性
"""


class TestClass(object):
    def set_attrs(self, arrts_dict: dict):
        """
        通过字典设置对象属性
        :param arrts_dict:
        :return:
        """
        for k, v in arrts_dict.items():
            # 该类不存在属性,则设置属性
            if not hasattr(self, k):
                setattr(self, k, v)

    def run(self):
        return "run"


if __name__ == '__main__':
    t = TestClass()
    test = {
        "name": "haha",
        "age": 20,
        "address": "beijing"
    }
    # 运行该属性则后面加括号
    print(getattr(t, "run")())
    t.set_attrs(test)
    print(t.name, t.age)
