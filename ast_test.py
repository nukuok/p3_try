# https://www.programcreek.com/python/example/83990/ast.walk

import ast
import inspect

from ast_test2 import mame_other

class gg:
    def cc(d, e):
        print(d, e)


G = gg()


def mame(abc):
    print(abc)


ccc = mame_other


def hoge():
    G.cc(d=1, e=2)
    print(mame)
    print(mame.__name__)
    mame(2)
    mame_other(2)
    ccc(2)
    lambda: mame(1)
    lambda: mame


if __name__ == "__main__":
    code = inspect.getsource(hoge)
    node = ast.parse(code)
    for n in ast.walk(node):
        print("{:#^60}".format(str(n)))
        if isinstance(n, ast.Call):
            if getattr(n.func, "id", None):
                print(n.func.id)
            if getattr(n.func, "attr", None):
                print(n.func.attr)

            if len(n.args) > 0:
                for arg in n.args:
                    print(arg)

            if len(n.keywords) > 0:
                for key in n.keywords:
                    print(key.arg)
                    print(key.value)
