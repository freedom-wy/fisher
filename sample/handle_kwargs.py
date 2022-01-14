
def a(v1, *args, **kwargs):
    print(kwargs.get("name"))


if __name__ == '__main__':
    a(v1="test", name="haha")
