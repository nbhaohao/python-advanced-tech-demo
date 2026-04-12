def gen_func():
    html = yield "http://www.baidu.com"
    print(html)
    yield 2
    yield 3
    return "pudge"


if __name__ == '__main__':
    gen = gen_func()
    next(gen)
    gen.close()
    print("")
