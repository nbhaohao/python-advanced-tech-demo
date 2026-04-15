# async for...in：异步生成器与异步迭代

## 一、引子：一段令人困惑的代码

```python
async def my_stream():
    async for chunk in some_method():
        yield chunk
```

这段代码组合了三个高级特性：`async def`、`async for`、`yield`。
它叫**异步生成器（async generator）**，常用于流式数据转发。

---

## 二、三个核心概念

### 1. `yield`（生成器）

让函数变成生成器——不一次性返回所有结果，而是"产出一个，暂停，再产出一个"。

```python
def count():
    yield 1
    yield 2
    yield 3

for x in count():   # 一次拿一个
    print(x)
```

### 2. `async def`（协程）

定义协程函数，可以在等待 IO 时让出控制权，让别的任务跑。

```python
async def fetch():
    data = await http_get(...)   # 等网络时不阻塞
    return data
```

### 3. `async for`（异步迭代）

普通 `for` 一次拿一个值；`async for` 也是一次拿一个，但**每次"拿"的过程是异步的**（拿之前可能要等网络）。

```python
async for chunk in stream:   # 等待下一个 chunk，但等的时候不阻塞
    print(chunk)
```

---

## 三、组合起来：异步生成器

```python
async def my_stream():
    async for chunk in some_method():   # 异步地一个个拿
        yield chunk                      # 拿到就立刻产出去
```

**含义**：
> "我是一个异步生成器。我会异步地从 `some_method()` 里一个个拿数据，
> **每拿到一个就立刻吐给我的调用者**，而不是等全部拿完再返回。"

### 数据流图解

```
LLM API           my_stream()           调用者（前端）
  │                   │                       │
  │── chunk 1 ──────→│                       │
  │                   │── yield chunk 1 ────→│  立刻收到
  │── chunk 2 ──────→│                       │
  │                   │── yield chunk 2 ────→│  立刻收到
  │── chunk 3 ──────→│                       │
  │                   │── yield chunk 3 ────→│  立刻收到
```

**每收到一块就立刻转发，不等所有 chunk 到齐 → 这就是流式转发。**

---

## 四、典型应用场景：LLM 流式中转层

```python
async def chat_endpoint(user_message):
    """后端 API：把 LLM 的流式输出转发给前端"""
    async for chunk in llm_client.stream(user_message):
        yield chunk   # LLM 吐一个字，立刻推给前端一个字
```

如果改用 `return`：

```python
# ❌ 失去流式
async def chat_endpoint(user_message):
    result = []
    async for chunk in llm_client.stream(user_message):
        result.append(chunk)
    return "".join(result)   # 必须等全部收完才返回 → 变成假流式
```

`yield` 版本**保留流式特性**，每一块到达就立刻往外推。

---

## 五、为什么两个 async 都不能去掉

### 核心因果链

> `async for` 内部要 `await __anext__()` → `await` 只能在协程里 → 所以外层必须 `async def`

### 实验对照表

| 写法 | 能编译？ | 能运行？ | 原因 |
|---|---|---|---|
| `async def` + `async for` | ✅ | ✅ | **正确写法** |
| `async def` + `for` | ✅ | ❌ TypeError | 普通 for 没法迭代异步对象 |
| `def` + `async for` | ❌ SyntaxError | - | `async for` 不能出现在普通函数里 |
| `def` + `for` | ✅ | ❌ TypeError | 同上 |

### 详细解释

**为什么不能用普通 `for`**：

```python
# 普通 for 的工作原理：
for x in obj:
    # 等价于不停调用 obj.__next__()

# async for 的工作原理：
async for x in obj:
    # 等价于不停调用 await obj.__anext__()
```

异步迭代器只有 `__anext__()`，没有 `__next__()`。普通 `for` 不会 `await`，无法处理。

**为什么外层必须 `async def`**：

`await` 的本质是"暂停当前协程，让事件循环跑别的任务，等结果好了再回来"。
这套机制需要协程的运行环境，普通函数没有这个能力：

```python
def normal_func():
    await something()    # ❌ SyntaxError
                         # 普通函数不知道怎么"暂停自己"
```

---

## 六、通用规则：await 的传染性

这条规则适用于**所有异步代码**，不只是 `async for`：

```python
# 场景 1：async for
async def f():
    async for x in stream:    # 内部 await __anext__()
        ...

# 场景 2：普通 await
async def f():
    data = await fetch()      # 直接 await

# 场景 3：async with
async def f():
    async with session() as s:  # 内部 await __aenter__() / __aexit__()
        ...

# 场景 4：调用其他协程
async def f():
    result = await other_async_func()
```

**统一规律：内层用了 await，外层就必须是 async**。

---

## 七、async / await 速查表

| 写法 | 含义 |
|---|---|
| `def` + `return` | 普通函数：算完一次性返回 |
| `def` + `yield` | 生成器：一个个产出 |
| `async def` + `return` | 协程：异步算完一次性返回 |
| `async def` + `yield` | **异步生成器：异步地一个个产出** |

---

## 八、调试检查清单

写异步代码时遇到报错，按这个顺序自检：

1. **这一行有 `await` / `async for` / `async with` 吗？**
2. 如果有 → 当前函数**必须是** `async def`
3. 如果当前函数是 `async def` → 调用它的地方也**必须用** `await` 或在异步上下文里
4. 最顶层需要用 `asyncio.run()` 启动事件循环

---

## 九、一句话总结

> `async def` + `async for` + `yield` 组合起来叫**异步生成器**，
> 用来**异步地一个个产出数据**，是流式转发的标准写法。
>
> 两个 `async` 缺一不可：
> **外层的 `async` 申请暂停权限，内层的 `async for` 行使暂停权限**。
>
> 核心因果链：`async for` 要 `await` → `await` 只能在协程里 → 外层必须 `async def`。

---

## 十、yield vs await：方向完全相反

### 核心区别

```python
async def my_stream():
    async for chunk in some_method():
        yield chunk      # 把 chunk 推给"调用我的人"
        # await chunk    # ❌ 完全不同的意思
```

| 关键字 | 方向 | 作用 |
|---|---|---|
| `yield chunk` | **向外推**（往调用者方向） | "我产出一个值给你" |
| `await chunk` | **向内等**（往被调用者方向） | "我等你的结果" |

### 水管中转站比喻

```
水源（LLM）  →  你（my_stream）  →  用户（前端）
              ↑                ↑
        async for(等水来)   yield(把水推出去)
```

- `async for chunk in some_method()`：在**等上游送水过来**（异步等待）
- `yield chunk`：把**水推给下游**（产出数据）

### await 后面必须跟 awaitable 对象

`await` 只能跟"还没完成、需要等待的任务"：

```python
await asyncio.sleep(1)        # 等待计时器
await http_client.get(url)    # 等待 HTTP 响应
await another_async_func()    # 等待另一个协程
```

如果 `chunk` 只是普通字符串或字典（已经是结果了），`await chunk` 会报错：

```
TypeError: object str can't be used in 'await' expression
```

### 关键认知：async for 已经帮你 await 过了

```python
async def my_stream():
    async for chunk in some_method():   # ① 这里已经在等了
        yield chunk                      # ② 这里是产出，不是等
```

`async for` 在背后偷偷做了 `chunk = await some_method().__anext__()`，
所以拿到的 `chunk` 已经是等好的结果，**不需要再 await 一次**。

### 共存场景：中间有异步处理时

```python
async def my_stream():
    async for chunk in some_method():
        processed = await transform(chunk)   # await：等转换完成
        yield processed                       # yield：把转换结果推出去
```

两者职责完全不同，可以共存：
- `await transform(chunk)`：等异步转换函数返回结果
- `yield processed`：把结果推给调用者

### 三个关键字职责对照

| 想做什么 | 用什么 |
|---|---|
| **等**一个异步任务完成，拿它的结果 | `await` |
| **产出**一个值给调用者（让调用者能拿到） | `yield` |
| **异步地一个个拿**值（边等边遍历） | `async for` |

### 一句话记忆

> `yield` 是"向外推数据"，`await` 是"向内等结果"，两个方向完全相反。
> 在异步生成器里，`async for` 已经帮你 `await` 过了，
> 你拿到的 chunk 是现成的数据，所以**只能 yield，不能再 await**——
> 因为它已经不是"未完成的任务"了。

---

## 十一、关联知识

- 这种异步生成器是 Path A（真流式）的标准实现方式
- 对比 Path B（假流式）：拿到完整结果后切片伪装成流，参见 `fake-streaming.md`
- 真流式 + 工具调用很难做，因此很多团队选择假流式作为工程妥协 