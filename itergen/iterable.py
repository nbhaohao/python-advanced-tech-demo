"""
Python 迭代协议 (Iteration Protocol)

迭代协议是 Python 中用于支持循环和迭代的底层机制。它由两个部分组成：可迭代对象 (Iterable) 和迭代器 (Iterator)。

1. 可迭代对象 (Iterable)
   - 任何实现了 __iter__() 方法的对象都是可迭代对象。
   - __iter__() 方法必须返回一个迭代器对象。
   - 内置的可迭代对象包括列表、元组、字典、集合、字符串等。
   - 可以使用 iter() 函数获取一个可迭代对象的迭代器。

2. 迭代器 (Iterator)
   - 任何实现了 __next__() 方法的对象都是迭代器。
   - __next__() 方法返回序列中的下一个元素，如果没有更多元素，则引发 StopIteration 异常。
   - 迭代器也应该实现 __iter__() 方法，返回自身，这样迭代器本身也是可迭代的。
   - 可以使用 next() 函数手动调用迭代器的 __next__() 方法。

迭代协议的工作流程：
   1. 当使用 for 循环遍历一个可迭代对象时，Python 首先调用 iter(obj) 获取迭代器。
   2. 然后重复调用 next(iterator) 获取下一个元素，直到遇到 StopIteration 异常。

示例：
   class MyIterable:
       def __init__(self, data):
           self.data = data

       def __iter__(self):
           self.index = 0
           return self

       def __next__(self):
           if self.index >= len(self.data):
               raise StopIteration
           value = self.data[self.index]
           self.index += 1
           return value

   # 使用
   my_iterable = MyIterable([1, 2, 3])
   for item in my_iterable:
       print(item)

注意：生成器 (Generator) 是迭代器的一种特殊形式，使用 yield 关键字简化了迭代器的创建。
"""
from collections.abc import Iterable, Iterator

a = [1, 2]
iter_rator = iter(a)
print(isinstance(a, Iterable)) # True
print(isinstance(a, Iterator)) # False
print(isinstance(iter_rator, Iterator)) # True