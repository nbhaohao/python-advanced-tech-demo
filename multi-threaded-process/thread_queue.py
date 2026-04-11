import threading
import time

detail_url_list = []


def get_detail_html(detail_url_list):
    while True:
        if len(detail_url_list):
            url = detail_url_list.pop()
            # for url in detail_url_list:
            print("get detail html started")
            time.sleep(2)
            print("get detail html ended")


def get_detail_url(detail_url_list):
    print("get detail url started")
    time.sleep(4)
    for i in range(20):
        detail_url_list.append("http://projectedu.com/{id}".format(id=i))
    print("get detail url ended")


# 1. 线程通信方式 - 共享变量(不推荐).
if __name__ == '__main__':
    thread_detail_url = threading.Thread(target=get_detail_url, args=(detail_url_list,))
    for i in range(10):
        html_thread = threading.Thread(target=get_detail_html, args=(detail_url_list,))
        html_thread.start()

    thread_detail_url.start()
