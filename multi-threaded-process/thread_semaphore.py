import threading
import time


class HtmlSpider(threading.Thread):
    def __init__(self, url, sem):
        super().__init__()
        self.url = url
        self.sem = sem

    def run(self):
        time.sleep(2)
        print("got html text successfully")
        self.sem.release()


class UrlProducer(threading.Thread):
    def __init__(self, sem):
        super().__init__()
        self.sem = sem

    def run(self):
        for i in range(10):
            self.sem.acquire()
            html_thread = HtmlSpider("http://www.baidu.com/{}".format(i), self.sem)
            html_thread.start()


if __name__ == "__main__":
    sem = threading.Semaphore(3)
    url_producer = UrlProducer(sem)
    url_producer.start()
