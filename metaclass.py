def _log(phrase):
    print("{:#^40s}".format(phrase))

class meta1(type):
    def __new__(self, clsname, bases, attrs):
        _log("meta new start")
        print(self)
        print(super())
        # _log("meta new end")
        return super().__new__(self, clsname, bases, attrs)

    def __init__(cls, clsname, bases, attrs):
        _log("meta init start")
        print(cls)
        print(super())
        # _log("meta init end")
        super().__init__(clsname, bases, attrs)


class p2(metaclass=meta1):
    # def __new__(self):
    #     _log("p2 new start")
    #     print(self)
    #     print(super())
    #     _log("p2 new end")

    def __init__(self):
        _log("p2 init start")
        print(self)
        print(super())
        # _log("p2 init end")


class p3(metaclass=meta1):
    def __new__(self):
        _log("p3 new start")
        print(self)
        print(super())
        # _log("p3 new end")

    # def __init__(self, abc):
    #     self.abc = abc
    #     _log("p3 init start")
    #     print(self)
    #     print(super())
    #     _log("p3 init end")


if __name__ == "__main__":
    g = p2()
    h = p3()
