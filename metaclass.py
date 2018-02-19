class meta1(type):
    def __new__(cls, clsname, bases, attrs):
        attrs["a"] = 1
        attrs["b"] = 1

        return super().__new__(cls, clsname, bases, attrs)


class p2:
    def __init__(self):
        self.a = 2
        self.b = 2


class GG(p2, metaclass=meta1):
    def __init__(self):
        pass
