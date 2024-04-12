# python的可迭代对象、迭代器与生成器

三者关系

![本地](python的可迭代对象、迭代器与生成器的关系.png images/python/python basic/python的可迭代对象、迭代器与生成器的关系.png>)

## 可迭代对象
可迭代对象（Iteratable Object） 是能够一次返回其中一个成员的对象，通常 for 循环 来完成此操作，如字符串、列表、元组、集合、字典等等之类的对象都属于可迭代对象。(任何你可以循环遍历的对象都是可迭代对象。)
1. 使用 isinstance()函数 判断对象是否是可迭代对象
```python
# 导入 collections 模块的 Iterable 对比对象
>>> from collections import Iterable
# 字符串是可迭代对象
>>> isinstance("kele", Iterable)
True
# 列表是可迭代对象
>>> isinstance(["kele"], Iterable)
True
# 字典是可迭代对象
>>> isinstance({"name":"kele"}, Iterable)
True
# 集合是可迭代对象
>>> isinstance({1,2}, Iterable)
True
# 数字不是可迭代对象
>>> isinstance(18, Iterable)
False
```
2. 使用 dir()函数 查看对象内所有的属性与方法
```python
# 字符串的所有属性与方法
>>> dir("kele")
[..., '__iter__', '__le__', '__len__', '__lt__', '__mod__', '__mul__', '__ne__', '__new__', '__reduce__', ...]

# 列表的所有属性与方法
>>> dir(["kele"])
[..., '__iter__', '__le__', '__len__', '__lt__', '__mul__', '__ne__', '__new__', '__reduce__',...]

# 字典的所有属性与方法
>>> dir({"name":"kele"})
[..., '__iter__', '__le__', '__len__', '__lt__', '__ne__', '__new__', '__reduce__', ...]

# 数字的所有属性与方法
# 并没有找到 __iter__
>>> dir(18)
['__abs__', '__add__', '__and__', '__bool__', '__ceil__', '__class__', '__delattr__', '__dir__', '__divmod__', '__doc__', '__eq__', '__float__', '__floor__', '__floordiv__', '__format__', '__ge__', '__getattribute__', '__getnewargs__', '__gt__', '__hash__', '__index__', '__init__', '__init_subclass__', '__int__', '__invert__', '__le__', '__lshift__', '__lt__', '__mod__', '__mul__', '__ne__', '__neg__', '__new__', '__or__', '__pos__', '__pow__', '__radd__', '__rand__', '__rdivmod__', '__reduce__', '__reduce_ex__', '__repr__', '__rfloordiv__', '__rlshift__', '__rmod__', '__rmul__', '__ror__', '__round__', '__rpow__', '__rrshift__', '__rshift__', '__rsub__', '__rtruediv__', '__rxor__', '__setattr__', '__sizeof__', '__str__', '__sub__', '__subclasshook__', '__truediv__', '__trunc__', '__xor__', 'bit_length', 'conjugate', 'denominator', 'from_bytes', 'imag', 'numerator', 'real', 'to_bytes']
```
3. 对比可迭代对象与不可迭代对象的所有属性与方法 **可迭代对象都构建了 ``__iter__`` 方法，而不可迭代对象没有构建，因此我们也可通过此特点来判断某一对象是不是可迭代对象。**
```python
# 没有定义 __iter__ 方法则是不可迭代对象
>>> from collections import Iterable
>>> class IsIterable:
        pass
>>> isinstance(IsIterable(), Iterable)
False

# 定义 __iter__ 方法则是可迭代对象
>>> class IsIterable:
        def __iter__(self):
            pass
>>> isinstance(IsIterable(), Iterable)
True
```
### 迭代器
迭代器（Iterator） 是同时实现`__iter__()` 与 `__next__()` 方法的对象
* 可通过 `__next__()` 方法或者一般的 for 循环进行遍历，能够记录每次遍历的位置，迭代器对象从集合的第一个元素开始访问，直到所有的元素被访问完结束，迭代器只能往前不能后退，终止迭代则会抛出 StopIteration 异常
1. 迭代器是可迭代对象
```python
>>> from collections import Iterable
# 以前面得到的迭代器为例
>>> isinstance("kele".__iter__(), Iterable)
True
```
2. 使用 dir()函数 查看迭代器所有的属性与方法
```python
>>> dir("kele".__iter__(), Iterable)
# 迭代器同时实现
# __iter__ 与 __next__ 方法
[..., '__iter__', '__le__', '__length_hint__', '__lt__', '__ne__', '__new__', '__next__', ...]
```
3. 使用 `__next__()` 方法获取迭代器中的元素
```python
>>> str_iterator = "kele".__iter__()
>>> str_iterator.__next__()
'k'
>>> str_iterator.__next__()
'e'
>>> str_iterator.__next__()
'l'
>>> str_iterator.__next__()
'e'
>>> str_iterator.__next__()
# 终止迭代则会抛出 StopIteration 异常
Traceback (most recent call last):
  File "<input>", line 1, in <module>
StopIteration
```
4. 使用 next() 与 iter() 方法来实现相同的效果
```python
# 使用 iter() 方法获取一个迭代器
>>> str_iterator = iter("kele")
# 使用 next() 方法获取迭代器中的元素
>>> next(str_iterator)
'k'
>>> next(str_iterator)
'e'
>>> next(str_iterator)
'l'
>>> next(str_iterator)
'e'
>>> next(str_iterator)
# 终止迭代则会抛出 StopIteration 异常
Traceback (most recent call last):
  File "<input>", line 1, in <module>
StopIteration
```
5. 例子实现一个迭代器类，返回偶数
```python
>>> class MyIterator:
        """
        迭代器类
        Author：可乐python说
        """
        def __init__(self):
            self.num = 0
        def __iter__(self):
            return self
        def __next__(self):
            return_num = self.num
            # 只要值大于等于6，就停止迭代
            if return_num >= 6:
                raise StopIteration
            self.num += 2
            return return_num

>>> my_iterator = MyIterator()
>>> next(my_iterator)
0
>>> next(my_iterator)
2
>>> next(my_iterator)
4
>>> next(my_iterator)
Traceback (most recent call last):
  File "<input>", line 1, in <module>
StopIteration
```
6. 对异常进行处理，获取到 StopIteration 异常便退出循环
```python
>>> class MyIterator:
        # 以上略...
        def __next__(self):
            return_num = self.num
            # 只要值大于等于6，就停止迭代
            if return_num >= 6:
                raise StopIteration
            self.num += 2
            return return_num

>>> my_iterator = MyIterator()
>>> while True:
        try:
            my_num = next(my_iterator)
        except StopIteration:
            break
        print(my_num)

0
2
4
```
* 对迭代器捕获异常后，其实就是实现了与 for 循环类似的效果，这也正是 for 循环底层实现的方式，当迭代一个可迭代对象时，for 循环通过 iter() 方法获取要迭代的项，并使用 next() 方法返回后续的项
* 迭代器可通过两种方式获取
    1. 调用迭代器类中的方法直接返回迭代器
    2. 可迭代对象通过执行 __ iter()__ 方法获取，迭代器在一定程度上节省了内存，需要时才去获取对应的数据
* 不想遵循迭代器协议，即不想实现`__iter__()` 与 `__next__()` 方法 ，但我们又想实现与迭代器相同的功能，这时，就需要使用到一种特殊的迭代器，这正是我们接下来要介绍的内容 生成器
## 生成器
Python 中，提供了两种 生成器（Generator） ，一种是生成器函数，另一种是生成器表达式
* 生成器函数
    * 定义与常规函数相同，区别在于，它使用 yield 语句 而不是 return 语句 返回结果， yield 语句一次返回一个结果，在每个结果中间，会暂停并保存当前所有的运行信息，以便下一次执行 next() 方法时从当前位置继续运行
* 生成器表达式
    * 与列表推导式类似，区别在于，它使用小括号  () 包裹，而不是中括号，生成器返回按需产生结果的一个对象，而不是一次构建完整的列表
1. 动手实现一个生成器函数
```python
>>> def my_generator():
        my_num = 0
        while my_num < 5:
            yield my_num
            my_num += 1

>>> generator_ = my_generator()
# 得到一个生成器对象
>>> type(generator_)
<class 'generator'>
```
2. 生成器也是迭代器
```python
# 以上略...
>>> generator_ = my_generator()
# 可发现 __iter__ 与 __next__ 方法
>>> dir(generator)
[..., '__iter__', '__le__', '__lt__', '__name__', '__ne__', '__new__', '__next__', ..., 'send', 'throw']
```
3. 传统方式获取生成器的元素
```python
# 以上略...
>>> generator_ = my_generator()
>>> next(generator_)
0
>>> next(generator_)
1
>>> next(generator_)
2
>>> next(generator_)
3
>>> next(generator_)
4
>>> next(generator_)
# 终止迭代则会抛出 StopIteration 异常
Traceback (most recent call last):
  File "<input>", line 1, in <module>
StopIteration
```
4. 使用 for 循环获取生成器元素
```python
# 以上略...
>>> generator_ = my_generator()
>>> for num_ in generator_:
        print(num_)

0
1
2
3
4
```

对于相同数量的项，列表生成式和生成器在内存消耗上存在巨大差异