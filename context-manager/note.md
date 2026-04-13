## Python Context Manager

### 核心概念
- `with` 语句背后就是 context manager
- 负责资源的**自动开启和关闭**，不需要手动处理
- 等价于 `try/finally`，但写法更简洁

### 两个实现方式

- **`__enter__` / `__exit__`**：在类里直接实现，适合自己写的类
- **`@contextmanager`**：用装饰器包装一个生成器函数，适合快速实现

### ★ 重点：@contextmanager 的实际价值

当你使用**第三方库或外部工具**，它没有实现 `__enter__` / `__exit__`，无法直接用 `with` 语句时，可以用 `@contextmanager` 把它包装成 context manager：

```
第三方库（没有 __enter__/__exit__）
  → 用 @contextmanager 包装
  → 变成可以用 with 语句的 context manager
  → 自动处理资源的开启和关闭
```

这样就不需要修改第三方库的代码，也能享受 `with` 语句自动管理资源的好处。

### 执行顺序

```
with xxx() as resource:
  → yield 之前的代码执行（开启资源）
  → resource 交给 with 块使用
  → with 块内的代码执行
  → with 块结束（正常或报错）
  → finally 执行（关闭资源，一定会执行）
```

### 和 FastAPI Depends 的关系

```
FastAPI Depends 的 get_session() 本质上就是 context manager 的思路：
  yield 之前  =  __enter__（创建 session）
  yield 之后  =  __exit__（commit / rollback / close）
```