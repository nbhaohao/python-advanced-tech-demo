from itertools import chain

# ── yield from 总结 ──────────────────────

# 核心心智模型：
#   yield from 是一座透明桥梁
#   外部对 outer 的操作，等价于直接操作 yield from 后面的子生成器
#   可以把子生成器的代码想象成"内联"进了 outer

# yield from 做的三件事：
#   1. 把子生成器的每个 yield 值依次传出去（和 for...in + yield 一样）
#   2. 把外部的 send() / throw() 直接转发给子生成器（双向透传）
#   3. 接收子生成器的 return 值作为表达式的结果

# def outer():
#     result = yield from sub()  # sub 的 return 值赋给 result
    # 等价于把 sub 的代码内联进来，行为完全一致

# for...in + yield  →  只透传值（单向）
# yield from        →  透传值 + send + throw + return（双向透明管道）

# 注意：
#   return 值不是 yield，不会出现在迭代结果里
#   只能通过 yield from 的返回值来拿到

# 和 await 的关系：
#   await 就是 yield from 的最终形态（语法糖）
#   result = await coroutine()
#   等价于 result = yield from coroutine()
#   Event Loop 通过这座桥，直接操作最底层真正在等待的 IO

my_list = [1, 2, 3]
my_dict = {
    "pudge1": "https://www.baidu.com",
    "pudge2": "https://www.zhihu.com",
}


def my_generator():
    yield "my_generator-1"
    yield "my_generator-2"
    return "my_generator-3"


def g1(iterable):
    yield iterable


def g2(iterable):
    yield from iterable

test_iterable = range(10)
for value in g1(test_iterable):
    print(value)

for value in g2(test_iterable):
    print(value)

# yield from iterable
# def my_chain(*args, **kwargs):
#     for my_iterable in args:
#         reslut = yield from my_iterable
#         print(reslut)
#         # for value in my_iterable:
#         #     yield value
#
#
# for value in my_chain(my_generator()):
#     print(value)
