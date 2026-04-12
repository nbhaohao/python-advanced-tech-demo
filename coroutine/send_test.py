def gen_func():
    x = yield
    print(f'x is {x}')
    y = yield
    print(f'y is {y}')
    z = yield
    print(f'z is {z}')
    return ""


if __name__ == '__main__':
    gen = gen_func()
    try:
        gen.send(None)
        gen.send("xx1")
        gen.send("yyyy2")
        gen.send("zzz333")
    except StopIteration:
        pass  # 正常结束，不是真正的错误