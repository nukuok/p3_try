import argparse
import inspect


class Singleton(type):
    def __init__(self, *args, **kwargs):
        self.__instance = None
        super().__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        if self.__instance is None:
            self.__instance = super().__call__(*args, **kwargs)
            return self.__instance
        else:
            return self.__instance


class CustomParser(metaclass=Singleton):
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parameters = {}

    def __call__(self, func):
        sig = inspect.signature(func)
        _cpy = sig.parameters.copy()
        self.parameters = {**self.parameters, **sig.parameters}
        return func

    def gen_parser(self):
        for param in self.parameters:
            param_detail = self.parameters[param]
            print(param_detail.annotation)
            self.parser.add_argument("--" + param_detail.name,
                                     help=str(param_detail.annotation),
                                     default=param_detail.default)


@CustomParser()
def something(a, b, c: "c value" = 1):
    print(a, b, c)


@CustomParser()
def something(j, k, l: "l value" = 1.0):
    print(a, b, c, "def")


if __name__ == "__main__":
    keeper = CustomParser()
    keeper.gen_parser()
    hoge = keeper.parser.parse_args()
    print(hoge)
