# 只要有 yield 关键字, 就是 generator function
def gen_func():
    yield 1
    yield 2
    yield 3


if __name__ == '__main__':
    gen = gen_func()

    # 生成器对象, 也实现了 Iterable
    for value in gen:
        print(value)
