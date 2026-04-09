import threading
import time


def get_detail_html(url):
    print("get detail html started")
    time.sleep(2)
    print("get detail html ended")


def get_detail_url(url):
    print("get detail url started")
    time.sleep(2)
    print("get detail url ended")


# if __name__ == "__main__":
#     # 通过 Thread 实例化
#     thread1 = threading.Thread(target=get_detail_html, args=("",))
#     thread2 = threading.Thread(target=get_detail_url, args=("",))
#     # 设置为守护线程后, 主线程退出, 守护线程也退出.
#     thread1.daemon = True
#     thread2.daemon = True
#     start_time = time.time()
#     thread1.start()
#     thread2.start()
#     # 没有 join 会直接打印 0 秒是因为当所有线程 sleep 时, 主线程直接运行完毕.
#
#     thread1.join()
#     thread2.join()
#     print("last time: {}".format(time.time() - start_time))


# 通过继承 Thread 实现多线程
class GetDetailHtml(threading.Thread):
    def __init__(self, name):
        super(GetDetailHtml, self).__init__(name=name)

    def run(self):
        print("get detail html started")
        time.sleep(2)
        print("get detail html ended")


class GetDetailUrl(threading.Thread):
    def __init__(self, name):
        super(GetDetailUrl, self).__init__(name=name)

    def run(self):
        print("get detail url started")
        time.sleep(2)
        print("get detail url ended")


if __name__ == "__main__":
    # 通过 Thread 实例化
    thread1 = GetDetailHtml("get_detail_html")
    thread2 = GetDetailUrl("get_detail_url")
    start_time = time.time()
    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()
    print("last time: {}".format(time.time() - start_time))
