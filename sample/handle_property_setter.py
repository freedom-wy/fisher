class TestClass(object):
    def __init__(self):
        self._time = None

    # property要先声明,然后再写setter
    # property会将方法转换为getter
    @property
    def time(self):
        return self._time

    # x.setter会将方法转换为setter
    @time.setter
    def time(self, value: int):
        if value < 10:
            raise ValueError("数值不符合要求")
        self._time = value


if __name__ == '__main__':
    t = TestClass()
    t.time = 1
    print(t.time)
