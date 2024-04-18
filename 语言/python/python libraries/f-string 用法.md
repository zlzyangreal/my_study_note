# f-string 用法
## %-formatting
Python 格式化的 OG，从一开始就在该语言中
```python
>>> name = "Eric"
>>> "Hello, %s." % name
'Hello, Eric.'
>>> name = "Eric"
>>> age = 74
>>> "Hello, %s. You are %s." % (name, age)
'Hello Eric. You are 74.'
```
缺点:使用多个参数和更长的字符串，代码将很快变得不那么容易阅读.它很冗长并且会导致错误，比如不能正确显示元组或字典
## str.format
在 Python 2.6 中引入
```python
>>> name = "Eric"
>>> age = 74
>>> "Hello, {}. You are {}.".format(name, age)
'Hello, Eric. You are 74.'
>>> "Hello, {1}. You are {0}.".format(age, name)
'Hello, Eric. You are 74.'
>>> person = {'name': 'Eric', 'age': 74}
>>> "Hello, {name}. You are {age}.".format(name=person['name'], age=person['age'])
'Hello, Eric. You are 74.'
>>> person = {'name': 'Eric', 'age': 74}
>>> "Hello, {name}. You are {age}.".format(**person)
'Hello, Eric. You are 74.'
```
缺点:处理多个参数和较长的字符串时，str.format() 仍然可能非常冗长
## f-string
亦称为格式化字符串常量（formatted string literals）
## 语法
```python
>>> name = "Eric"
>>> age = 74
>>> f"Hello, {name}. You are {age}."
'Hello, Eric. You are 74.'
# 使用大写字母 F 也是有效的
>>> F"Hello, {name}. You are {age}."
'Hello, Eric. You are 74.'
# 任意表达式
>>> f"{2 * 37}"
'74'
## 调用函数
def to_lowercase(input):
    return input.lower()

name = "Eric Idle"
f"{to_lowercase(name)} is funny."
## 选择直接调用方法
>>> f"{name.lower()} is funny."
'eric idle is funny.'
## 使用从具有 f-strings 的类创建的对象
class Comedian:
    def __init__(self, first_name, last_name, age):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age

    def __str__(self):
        return f"{self.first_name} {self.last_name} is {self.age}."

    def __repr__(self):
        return f"{self.first_name} {self.last_name} is {self.age}. Surprise!"

>>> new_comedian = Comedian("Eric", "Idle", "74")
>>> f"{new_comedian}"
'Eric Idle is 74.'
```