```python
# ── send() 总结 ──────────────────────────

# next(g)      完全等价于 g.send(None)，只是推进，不传值
# g.send(val)  传值进去 + 推进到下一个 yield

# yield 既是出口也是入口：
def gen():
    val = yield 1
    #      ↑ 出口：send(None)  → 暂停在这里，把 1 传出去
    #  ↑ 入口：send("hi")   → 把 "hi" 传进来，赋给 val，继续执行

# 第一次 send 和之后的 send 不一样：
#
#   第一次：生成器还没暂停在任何 yield
#           没有地方接收值，只能 send(None)，作用等同于 next()
#
#   之后每次：生成器暂停在某个 yield 上
#             send(val) 先把 val 传给当前 yield 表达式
#             再推进到下一个 yield

# 一句话总结：
#   next(g)      = 推进，不传值
#   g.send(None) = 推进，不传值（和 next 一样）
#   g.send(val)  = 传值进去 + 推进

# 和 asyncio 的关系：
#   Event Loop 第一次 send(None) 启动协程
#   之后每次 IO 完成，send(结果) 把数据注入回来继续执行
```

``` python
# ── yield from 总结 ──────────────────────

# 核心心智模型：
#   yield from 是一座透明桥梁
#   外部对 outer 的操作，等价于直接操作 yield from 后面的子生成器
#   可以把子生成器的代码想象成"内联"进了 outer

# yield from 做的四件事：
#   1. 把子生成器的每个 yield 值依次传出去（和 for...in + yield 一样）
#   2. 把外部的 send() / throw() 直接转发给子生成器（双向透传）
#   3. 自动捕获子生成器的 StopIteration，不会向外抛出
#   4. 把子生成器的 return 值作为 yield from 表达式的结果

# ★ 重点：yield from vs 直接把子生成器代码拷贝进 outer
#
#   看起来这两种写法效果一样：
#
#   写法1 - yield from：
#   def outer():
#       result = yield from sub()
#
#   写法2 - 直接内联 sub 的代码：
#   def outer():
#       x = yield 1
#       y = yield 2
#       result = "sub的return值"
#
#   行为基本一致，但有一个关键区别：
#
#   直接内联：sub 的 return 触发 StopIteration，会直接向外冒泡，outer 崩掉
#   yield from：自动捕获 StopIteration，把 return 值接住赋给 result，outer 继续执行
#
#   所以 yield from 不只是"语法糖"，它多做了一件手动内联做不到的事：
#   → 捕获 StopIteration + 接收 return 值，让 outer 能优雅地拿到结果并继续

# ★ 重点：return 值的传递
def outer():
    result = yield from sub()  # sub 执行完毕抛出 StopIteration
                               # yield from 自动捕获，不会报错
                               # sub 的 return 值被赋给 result
    print(result)              # 可以直接使用 return 值

# for...in + yield  →  只透传值（单向），StopIteration 直接冒泡，return 值丢失
# yield from        →  透传值 + send + throw（双向透明管道）
#                      + 捕获 StopIteration + 接收 return 值

# ★ 重点：while True 配合 yield from 的常见模式
def middle(key):
    while True:
        result = yield from sub()  # sub 结束 → yield from 捕获 StopIteration
        print(f"完成一轮: {result}") #           → result 拿到 return 值
                                   #           → while True 重新创建新的 sub
                                   #           → 又暂停在 yield from 待命
# while True 的作用：sub 结束后重置，让 middle 永久待命，避免 StopIteration 向外冒泡

# 注意：
#   return 值不是 yield，不会出现在迭代结果里
#   只能通过 yield from 的返回值来拿到
#   直接 for...in 遍历会丢失 return 值

# 和 await 的关系：
#   await 就是 yield from 的最终形态（语法糖）
#   result = await coroutine()
#   等价于 result = yield from coroutine()
#   Event Loop 通过这座桥，直接操作最底层真正在等待的 IO
```