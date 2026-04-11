from threading import Thread, Condition


# condition 的重要方法: wait, notify.
class XiaoAi(Thread):
    def __init__(self, cond):
        super().__init__(name="小爱")
        self.cond = cond

    def run(self):
        with self.cond:
            self.cond.wait()
            print("{} : 在".format(self.name))
            self.cond.notify()
            self.cond.wait()
            print("{} : 好啊".format(self.name))
            self.cond.notify()
            self.cond.wait()


class TianMao(Thread):
    def __init__(self, cond):
        super().__init__(name="天猫精灵")
        self.cond = cond

    def run(self):
        with self.cond:
            print("{} : 小爱同学 ".format(self.name))
            self.cond.notify()
            self.cond.wait()
            print("{} : 我们来对古诗吧 ".format(self.name))
            self.cond.notify()
            self.cond.wait()
            print("{} : 我住在长江头 ".format(self.name))
            self.cond.notify()
            self.cond.wait()


if __name__ == '__main__':
    Cond = Condition()
    xiaoai = XiaoAi(cond=Cond)
    tianmao = TianMao(cond=Cond)

    xiaoai.start()
    tianmao.start()
