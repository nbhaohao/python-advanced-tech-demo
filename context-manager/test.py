from contextlib import contextmanager


class Database:
    def __init__(self, name):
        self.name = name

    def close(self):
        print(f"Closing {self.name}")


@contextmanager
def database_context(name: str):
    print(f"Connecting to {name}")  # __enter__：开启资源
    db = Database(name)
    try:
        yield db  # 把资源交给 with 块使用
    finally:
        db.close()  # __exit__：关闭资源，一定会执行
        print(f"Disconnecting from {name}")


# 使用
with database_context("users") as db:
    print(f"Using {db.name}")
# with 块结束后，自动执行 finally 里的 close()
