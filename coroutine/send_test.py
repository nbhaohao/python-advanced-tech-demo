def gen_func():
    html = yield 1
    print(html)
    yield 2


if __name__ == '__main__':
    gen = gen_func()
    print(next(gen))
    print(gen.send("my html url"))
