"""
生成器工作原理示例

生成器对象有几个重要属性：
1. gi_frame: 生成器的帧对象，包含执行状态
2. gi_frame.f_lasti: 最后执行的字节码指令的索引
3. gi_frame.f_locals: 生成器帧的局部变量字典
4. gi_running: 生成器是否正在执行

当生成器执行时，gi_frame 包含当前帧的状态。
当生成器执行完毕，gi_frame 变为 None。
"""


def gen_func():
    """一个简单的生成器函数，演示生成器的工作原理"""
    yield 1
    age = 30  # 局部变量
    yield 2
    return "mooc"


# 演示生成器内部状态属性
if __name__ == "__main__":
    # 创建生成器对象
    gen = gen_func()

    print("初始状态:")
    print(f"  gi_frame: {gen.gi_frame}")
    print(f"  gi_running: {gen.gi_running}")

    # 第一次调用 next()
    print("\n1. 第一次调用 next(gen):")
    value1 = next(gen)
    print(f"   返回值: {value1}")
    print(f"   f_lasti (最后执行的指令索引): {gen.gi_frame.f_lasti}")
    print(f"   f_locals (局部变量): {gen.gi_frame.f_locals}")

    # 第二次调用 next()
    print("\n2. 第二次调用 next(gen):")
    value2 = next(gen)
    print(f"   返回值: {value2}")
    print(f"   f_lasti: {gen.gi_frame.f_lasti}")
    print(f"   f_locals: {gen.gi_frame.f_locals}")
    print(f"   局部变量 age: {gen.gi_frame.f_locals.get('age')}")

    # 第三次调用 next() - 将触发 StopIteration
    print("\n3. 第三次调用 next(gen):")
    try:
        value3 = next(gen)
        print(f"   返回值: {value3}")
    except StopIteration as e:
        print(f"   StopIteration 异常被触发")
        print(f"   异常值 (return 的值): {e.value}")
        print(f"   生成器状态: gi_frame = {gen.gi_frame}")

    print("\n生成器执行完毕，gi_frame 为 None 表示生成器已结束")
