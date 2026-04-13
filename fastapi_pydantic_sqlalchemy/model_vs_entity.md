## Model vs Entity

| Term | 用途 | 核心方法 | 数据库映射 |
|------|------|----------|------------|
| `model` | 数据验证 + 序列化（管进出 API 的数据） | `.model_dump()` | ❌ 无直接映射 |
| `entity` | 数据库记录映射（管表结构） | 由 SQLAlchemy 自动处理 | ✅ 直接 1:1 对应一行记录 |

### Model（Pydantic）

- 主要职责是**验证**，确保数据类型和格式正确
- 管"进出 API 的数据长什么样"
- 同一个业务对象通常有多个 Model，职责不同

```python
class UserCreate(BaseModel):
    name: str
    password: str          # 创建时需要

class UserResponse(BaseModel):
    id: int
    name: str              # 返回时不暴露 password
```

### Entity（SQLAlchemy）

- 对应数据库里的**一张表**，一个实例 = 表里的**一行记录**
- 数据库有什么字段，Entity 就有什么字段

```python
class UserEntity(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    password = Column(String)
    created_at = Column(DateTime)
```

### 一个业务对象的完整拆分

```
User 这个概念拆成三个东西：

UserEntity      → SQLAlchemy，1:1 对应数据库表，有所有字段
UserCreate      → Pydantic，创建时接收的数据（有 password）
UserResponse    → Pydantic，返回给前端的数据（不暴露 password）
```

> 类比前端：Entity ≈ 数据库 Schema，Model ≈ TypeScript interface