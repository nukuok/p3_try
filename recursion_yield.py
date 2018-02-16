import types
gen_type = types.GeneratorType


def fact1(n):
    if n == 1:
        return n
    else:
        return n * fact1(n - 1)


def one_step_recursion(n):
    if n >= 2:
        m = one_step_recursion(n - 1)
        return m * n
    else:
        return 1


def one_step_yield(n):
    if n >= 2:
        m = yield one_step(n - 1)
        yield n * m
    else:
        yield 1


def fact2(n):
    stack = [one_step_yield(n)]
    last_result = None
    while stack:
        try:
            last = stack[-1]
            if isinstance(last, gen_type):
                stack.append(last.send(last_result))
            elif isinstance(last, int):
                last_result = stack.pop()
            else:
                last_result = None
        except StopIteration:
           stack.pop()

    return last_result

if __name__ == "__main__":
    # print(fact1(10))
    # print(fact1(100))
    # print(fact2(100).send(None))
    # print(fact1(1000))
    h = fact2(100)
