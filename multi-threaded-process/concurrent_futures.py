from concurrent.futures import ThreadPoolExecutor, as_completed, wait
import time
from threading import Thread


def get_html(times):
    time.sleep(times)
    print("get page {} successfully".format(times))
    return times


# 立即返回 非阻塞.
# task1 = executor.submit(get_html, 3)
# task2 = executor.submit(get_html, 2)

# done 方法用于判断某个任务是否完成.
# print(task1.done())
# # time.sleep(3)
# print(task1.done())
# # 只有未开始的任务才可以 cancel.
# # print(task2.cancel())
# #result 可以获取 task 的执行结果. 阻塞
# print(task1.result())

executor = ThreadPoolExecutor(max_workers=10)
urls = [3, 2, 4]
all_task = [executor.submit(get_html, url) for url in urls]
# 哪个结果完成运行哪个, 而不是严格按照 task 顺序.
# for future in as_completed(all_task):
#     data = future.result()
#     print("get {} page successfully".format(data))


# for data in executor.map(get_html, urls):
#     print("get {} page".format(data))

wait(all_task)
print("main")
