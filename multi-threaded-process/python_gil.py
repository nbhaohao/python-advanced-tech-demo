# gil 使得同一个时刻只有一个线程在一个 cpu 上执行字节码
# 👉 即使你开了多个线程（threading）
# 👉 即使你是多核 CPU
#
# 同一个 Python 进程里：
# 	•	线程 A 执行一会儿
# 	•	然后释放 GIL
# 	•	线程 B 再执行
#
# 看起来像并发，其实是 轮流执行（切换）
import threading
import time

total = 0


def add():
    global total
    for i in range(1000000):
        tmp = total
        time.sleep(0)
        total = tmp + 1


def desc():
    global total
    for i in range(1000000):
        tmp = total
        time.sleep(0)
        total = tmp - 1


thread1 = threading.Thread(target=add)
thread2 = threading.Thread(target=desc)

thread1.start()
thread2.start()

thread1.join()
thread2.join()
print(total)
