# 模拟场景：统计每个班级的总分
# sales_sum 对应 → 收集分数的子生成器
# middle     对应 → 中间层协程
# main       对应 → 数据分发器

final_result = {}

def collect_scores(class_name):
    """收集分数，return 总分"""
    total = 0
    while True:
        score = yield              # 等待接收分数
        if score is None:          # 收到 None 表示这个班级结束了
            break
        total += score
        print(f"  [{class_name}] 收到分数: {score}, 当前合计: {total}")
    return total                   # 返回总分给 middle

# ── 版本2：有 while True ────────────────────
def middle_with_loop(key):
    while True:
        final_result[key] = yield from collect_scores(key)
        print(f"{key} 第一轮统计完成，总分: {final_result[key]}")
        # 继续循环，重新开始收集第二轮

def main():
    # 创建两个班级的 middle 协程
    m1 = middle_with_loop("高一甲班")
    m2 = middle_with_loop("高一乙班")

    # 启动
    m1.send(None)
    m2.send(None)

    print("=== 第一轮：发送第一批分数 ===")
    m1.send(90)
    m1.send(80)
    m2.send(70)
    m2.send(60)

    print("=== 第一轮结束，发送 None 结算 ===")
    m1.send(None)   # collect_scores 收到 None → break → return total
                    # middle 的 yield from 拿到 return 值
                    # print 完成
                    # while True 继续，重新进入新的 collect_scores 等待
    m2.send(None)

    print("=== 第二轮：发送第二批分数 ===")
    m1.send(100)
    m1.send(50)
    m2.send(88)

    print("=== 第二轮结束，发送 None 结算 ===")
    m1.send(None)
    m2.send(None)

if __name__ == '__main__':
    main()
    print(f"\n最终结果: {final_result}")