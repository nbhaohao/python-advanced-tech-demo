def gen_func():
    try:
        yield "http://www.baidu.com"
    except Exception:
        pass
    yield 2
    yield 3
    return "pudge"


if __name__ == '__main__':
    gen = gen_func()
    print(next(gen))
    print(gen.throw(Exception("test")))
    print(next(gen))
