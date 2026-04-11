# 通过 Queue 的方式进行线程间同步.
import threading
import time
from queue import Queue


def get_detail_html(queue):
    while True:
        url = queue.get()
        # for url in detail_url_list:
        print("get detail html started")
        time.sleep(2)
        print("get detail html ended")


def get_detail_url(queue):
    print("get detail url started")
    time.sleep(4)
    for i in range(20):
        queue.put("http://projectedu.com/{id}".format(id=i))
    print("get detail url ended")


# 1. 线程通信方式 - 共享变量(不推荐).
if __name__ == '__main__':
    detail_url_queue = Queue(maxsize=1000)
    thread_detail_url = threading.Thread(target=get_detail_url, args=(detail_url_queue,))
    for i in range(10):
        html_thread = threading.Thread(target=get_detail_html, args=(detail_url_queue,))
        html_thread.start()

    start_time = time.time()

    detail_url_queue.task_done()
    detail_url_queue.join()

    thread_detail_url.start()
