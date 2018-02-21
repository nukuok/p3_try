import argparse
import ast
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


def mame00(a, b=1):
    sig = inspect.getsource(mame00)
    print(str(sig))
    return sig


def mame01():
    mame00(1, b=2)
    sig = inspect.getsource(mame01)
    print(str(sig))
    return sig


# https://stackoverflow.com/questions/16361390/is-there-an-ast-python3-documentation-at-least-for-the-syntax
class FuncVisit(ast.NodeVisitor):
    def __init__(self):
        self.calls = []
        self.names = []
    def generic_visit(self, node):
        # Uncomment this to see the names of visited nodes
        # print(type(node).__name__)
        ast.NodeVisitor.generic_visit(self, node)
    def visit_Name(self, node):
        self.names.append(node.id)
    def visit_Call(self, node):
        self.names = []
        ast.NodeVisitor.generic_visit(self, node)
        self.calls.append(self.names)
        self.names = []
    def visit_keyword(self, node):
        self.names.append(node.arg)


if __name__ == "__main__":
    keeper = CustomParser()
    keeper.gen_parser()
    hoge = keeper.parser.parse_args()
    print(hoge)

    m0 = mame00(1, 2)
    m1 = mame01()

    # 関数の呼び出し関係抽出 1
    h = ast.parse(m1)
    m = FuncVisit()
    m.visit(h)
    print(m.calls)

    # 関数の呼び出し関係抽出 2
    for node in ast.walk(h):
        if hasattr(node, "id"):
            print(node.id)
        elif hasattr(node, "name"):
            print(node.name)

    # 利用しない理由: 関数が複数回呼ばれる可能性があり、
    # それぞれの引数は違う可能性があるため、cliから受けるべきかどうかを一意的に判断できません。
