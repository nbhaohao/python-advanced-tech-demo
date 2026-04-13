## SQLAlchemy session.flush() vs session.refresh()

### flush()

- 把内存里的变更**发送到数据库**，但不提交事务（还可以回滚）
- 数据库在当前事务内生成 id、created_at 等字段，并**自动回填到对象**
- 常见场景：创建 A 之后，需要用 A 的 id 去创建关联的 B

```python
order = OrderEntity(user_id=1)
session.add(order)
print(order.id)  # None ← 还在内存里

session.flush()
print(order.id)  # 5 ← 数据库生成了 id，自动回填到对象
```

### refresh()

- 在当前事务内重新 SELECT 一次，把数据库里的完整数据拉回来
- 可选的，取决于你是否需要返回完整对象
- 常见场景：flush 之后，created_at 等字段还没同步，refresh 一下补全

```python
session.add(entity)
session.flush()  # id 回填了，但 created_at 等可能还没同步
session.refresh(entity)  # 重新拉取，所有字段补全
return entity  # ✅ 安全返回给前端
```

### create 方法的标准三步

```python
session.add(entity)  # 1. 追踪对象，纯内存，id = None
session.flush()  # 2. INSERT 到数据库，id 自动回填
session.refresh(entity)  # 3. 重新 SELECT，补全所有字段（可选）
return entity
# commit 由 get_db 依赖注入在请求结束后自动处理
```

### 什么时候用什么

| 场景          | 做法                      |
|-------------|-------------------------|
| 只需要 id 做关联  | `flush()` 就够            |
| 需要返回完整对象给前端 | `flush()` + `refresh()` |
| 不关心生成的字段    | 直接 `commit()`           |

### 一句话总结

> `flush` 负责"推出去生成数据"，`refresh` 负责"拉回来补全字段"
> commit 由 `get_db` 在请求结束后自动处理