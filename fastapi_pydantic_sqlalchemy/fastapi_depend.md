## FastAPI Depends 基于 Generator 实现 Session 的原理

### get_session 的写法

```python
def get_session() -> Generator[Session, None, None]:
    session = Database.db_local_session()
    try:
        yield session  # 把 session 交给 endpoint
        session.commit()  # endpoint 正常结束后自动 commit
    except Exception:
        session.rollback()  # 出错自动回滚
        raise
    finally:
        session.close()  # 最后 always 关闭 session
```

### FastAPI Depends 内部简易原理

```python
# FastAPI 内部大概做了这些事：
def process_request():
    # 1. 调用生成器函数，拿到生成器对象
    session_generator = get_session()

    # 2. next() 推进到 yield，拿到 session（执行 yield 之前的代码）
    session = next(session_generator)

    # 3. 把 session 注入到 endpoint 函数里执行
    result = your_endpoint_function(session)

    # 4. 再次推进生成器，执行 yield 之后的代码（commit/rollback/close）
    try:
        next(session_generator)  # 执行 yield 后面的 commit + close
    except StopIteration:
        pass  # 生成器正常结束，忽略 StopIteration
```

### 执行顺序

```
请求进来
  → get_session() 创建生成器
  → next() 执行到 yield，session 创建完毕
  → session 注入到 endpoint
  → endpoint 执行（add、flush、refresh...）
  → next() 继续执行 yield 之后的代码
  → commit()    ← 自动提交
  → close()     ← 自动关闭
```

### Generator[Session, None, None] 类型注解含义

| 位置              | 类型        | 含义              |
|-----------------|-----------|-----------------|
| 1st: YieldType  | `Session` | yield 出去的值的类型   |
| 2nd: SendType   | `None`    | 不接收 send() 传入的值 |
| 3rd: ReturnType | `None`    | 生成器 return 的值类型 |

### 关键点

- `yield` 之前的代码 = 请求开始时执行（创建 session）
- `yield` 之后的代码 = 请求结束时执行（commit / rollback / close）
- FastAPI 用 `next()` 驱动生成器，本质上和你学的生成器知识完全一样
- `StopIteration` 被 FastAPI 内部捕获，不会报错