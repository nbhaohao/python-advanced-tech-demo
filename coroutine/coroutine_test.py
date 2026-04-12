def gen_func():
    yield 1
    print("第二次调用")
    yield 2
    yield 3
    return "pudge"


if __name__ == '__main__':
    gen = gen_func()
    print(next(gen))
    print(next(gen))
    print(next(gen))
    print(next(gen))
