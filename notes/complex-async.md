🧠 Python 异步数据库 Session 管理机制笔记

📌 一、整体结构（三层模型）

底层生成器 (async generator)
↓ (async for)
中间封装 (@asynccontextmanager)
↓ (async with)
业务代码使用

⸻

🧩 二、代码结构

1️⃣ 底层：Session 生成器

async def get_session():
async with Database.db_local_session() as session:
try:
yield session
await session.commit()
except Exception:
await session.rollback()
raise

✅ 特点
• 异步生成器（async def + yield）
• 负责：
• 创建 session
• 提供 session
• commit / rollback

⸻

2️⃣ 中间层：封装为上下文管理器

from contextlib import asynccontextmanager

@asynccontextmanager
async def get_db_session():
async for session in get_session():
yield session

✅ 特点
• 使用 @asynccontextmanager
• 将“生成器”包装成“上下文管理器”
• 内部使用 async for 获取 session

⸻

3️⃣ 外层：业务使用

async with get_db_session() as session:
await session.execute(...)

✅ 特点
• 使用 async with
• 自动管理资源生命周期

⸻

🔄 三、执行流程

1. async with get_db_session()
2. 进入 get_db_session
3. 执行 async for → 调用底层 get_session
4. 创建 session
5. yield session 给调用方

6. 业务代码执行数据库操作

7. 退出 async with
8. 回到生成器 yield 之后
9. 成功 → commit
10. 异常 → rollback
11. 关闭 session

⸻

⚠️ 四、关键知识点总结

1️⃣ async def
• 定义协程函数

2️⃣ yield（异步生成器）
• 分阶段执行代码
• yield 前：准备资源
• yield 后：清理资源

3️⃣ async for
• 用于消费异步生成器
• ⚠️ 这里只在内部使用

4️⃣ async with
• 使用异步上下文管理器
• 自动调用：
•    __aenter__()
•    __aexit__()

5️⃣ @asynccontextmanager
• 把“yield 风格函数”转换为上下文管理器

⸻

❗五、常见误区

❌ 误区 1：可以 async for 外部使用

async for session in get_db_session():  # ❌ 错误
...

👉 原因：
• 被 @asynccontextmanager 修饰后
• 它已经不是 generator，而是 context manager

⸻

❌ 误区 2：可以无限获取 session

👉 错误理解：

可以不断迭代获取新的 session

👉 正确理解：
• 每次 async with → 获取一个 session
• 生命周期只持续一次使用

⸻

✅ 六、一句话总结

🔥 内部 async for 取 session，外部 async with 用 session。

⸻

🎯 七、本质理解

这个模式本质是：

使用 异步生成器 + 上下文管理器 实现数据库事务自动管理

实现效果：
• 自动 commit
• 自动 rollback
• 自动关闭连接

⸻

🧪 八、心智模型（类比）

把它想象成：
• get_session()：水厂（生产水 + 回收处理）
• get_db_session()：取一杯水的接口
• async with：你用水

👉 用完之后系统自动处理善后

⸻

🚀 九、记忆口诀

生成器负责“生产 + 善后”
async for 只在内部
async with 才是外部用法

⸻

🔍 十、FastAPI Depends 的完整调用链

假设有如下代码：

from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI()

@app.get("/users")
async def list_users(session: AsyncSession = Depends(get_session)):
result = await session.execute(...)
return result.scalars().all()

调用链可以理解为：

客户端发起请求
↓
FastAPI 匹配到路由函数
↓
发现参数 session = Depends(get_session)
↓
FastAPI 调用 get_session()
↓
执行到 yield session
↓
把 session 注入到路由函数参数里
↓
路由函数开始执行数据库操作
↓
路由函数正常结束 / 抛出异常
↓
FastAPI 回到 get_session() 的 yield 后面
↓
成功则 commit
失败则 rollback
↓
关闭 session
↓
返回响应

关键理解
• Depends(get_session) 并不是简单“调用一次函数拿返回值”
• 对于带 yield 的依赖，FastAPI 会把它当作带清理逻辑的依赖
• 也就是：
• yield 前：准备资源
• yield 中：交给路由函数用
• yield 后：做清理和善后

所以它很适合管理：
• 数据库连接 / Session
• 文件句柄
• 网络连接
• 临时事务资源

⸻

🧪 十一、最小可运行 Demo

下面是一个简化版示例，帮助你把这个模式串起来理解。

from contextlib import asynccontextmanager
from typing import AsyncIterator

class FakeSession:
async def execute(self, sql: str):
print(f"execute: {sql}")

    async def commit(self):
        print("commit")

    async def rollback(self):
        print("rollback")

class Database:
@staticmethod
async def get_session():
session = FakeSession()
print("create session")
try:
yield session
await session.commit()
except Exception:
await session.rollback()
raise
finally:
print("close session")

@asynccontextmanager
async def get_db_session() -> AsyncIterator[FakeSession]:
async for session in Database.get_session():
yield session

async def main():
async with get_db_session() as session:
await session.execute("select * from users")

正常执行时，输出顺序大致是：

create session
execute: select * from users
commit
close session

如果中间抛异常：

async def main():
async with get_db_session() as session:
await session.execute("select * from users")
raise ValueError("something wrong")

输出会变成：

create session
execute: select * from users
rollback
close session

这个 demo 说明了什么？
• yield 把 session 交出去
• 外部代码执行完成后，流程会回到 yield 后面
• 后续会根据是否出错，决定 commit 还是 rollback

⸻

🧬 十二、asynccontextmanager 的底层实现原理（进阶理解）

@asynccontextmanager 的核心作用是：

把一个“只 yield 一次的异步生成器函数”包装成异步上下文管理器。

也就是说，这样的代码：

@asynccontextmanager
async def get_db_session():
async for session in Database.get_session():
yield session

会被包装成一个支持下面接口的对象：

obj = get_db_session()
await obj.__aenter__()
...
await obj.__aexit__(...)

可以把它粗略理解成伪代码：

class AsyncContextManagerWrapper:
def __init__(self, agen):
self.agen = agen

    async def __aenter__(self):
        return await self.agen.__anext__()

    async def __aexit__(self, exc_type, exc, tb):
        if exc is None:
            try:
                await self.agen.__anext__()
            except StopAsyncIteration:
                return
        else:
            await self.agen.athrow(exc_type, exc, tb)

你可以从这个角度理解：
•    __aenter__()：推进生成器，拿到 yield 出来的资源
•    __aexit__()：把控制权送回生成器，让它继续执行 yield 后面的清理逻辑

这就是为什么：

async with get_db_session() as session:
...

退出 async with 时，会自动继续执行到：

await session.commit()

# 或

await session.rollback()

⸻

🧠 十三、把三种写法彻底区分开

1. 异步生成器

async def gen():
yield 1

使用方式：

async for x in gen():
print(x)

2. 异步上下文管理器

@asynccontextmanager
async def cm():
yield resource

使用方式：

async with cm() as resource:
...

3. FastAPI 的 yield 依赖

async def get_session():
yield session

使用方式：

session: AsyncSession = Depends(get_session)

它们的联系
• 底层都可能依赖 yield
• 但外部消费方式不同：
• 生成器 → for / async for
• 上下文管理器 → with / async with
• FastAPI 依赖 → Depends(...)

⸻

✅ 十四、最终总口诀

yield 是分界线：
前面负责准备资源
中间交给外部使用
后面负责清理资源

纯生成器，用 for / async for
contextmanager，用 with / async with
FastAPI 依赖，用 Depends