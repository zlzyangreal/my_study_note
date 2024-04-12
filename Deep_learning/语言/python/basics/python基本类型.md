# python 基本类型

数值
----
***整数***

`//` 整数除法
* 结果是商的整数部分
`/` 除法
* 数学除法,得到小数
`divmod(m,n)` 求整数除法和余数
* 会得到两个整数,一个是`m//n`,另一个是`m%n`
`m**n` 求乘方
* 整数m的n次方

逻辑值
------
***整数、浮点数和复数类型***
* 0是"假",所有非0的数值都是"真"
***字符串类型***
* 空串(" ")是"假",所有空串都是"真"
***所有序列类型(包括字符串)***
* 空序列是"假",所有非空的序列都是"真"
***空值None***
* 表示"无意义"或"不知道",也是"假"

字符串
------
***特殊字符表示***
* `\\`      反斜杠符号
* `\'`      单引号
* `\"`      双引号
* `\a`      响铃
* `\b`      退格
* `\e`      转义
* `\000`    空
* `\n`      换行
* `\v`      纵向制表符
* `\t`      横向制表符
* `\r`      回车
* `\f`      换页
* `\oyy`    八进制数yy代表的字符,例如:\o12代表换行,数值参看ASCII码表
* `\xyy`    十六进制yy代表的字符

***字符串操作***
获取字符串的长度: `len` 函数

切片(slice)操作: `s[start:end:step]`
```python
# 例子
s="Hello World!"
s[3:8:2]
# 结果
# l  (空格) o
```

+: 将两个字符串进行连接,得到新的字符串

*: 将字符串重复若干次,生成新的字符串

==: 判断字符串内容是否相同

in: 判断字符串中是否包含某个字符串

删除空格:
* `str.strip` 去掉字符串前后所有的空格,内部的空格不受影响
* `str.lstrip`去掉字符串前部（左部）的所有空格
* `str.rstrip`去掉字符串后部（右部）的所有空格

判断字母数据:
* `str.isalpha`判断字符串是否全部由字母构成
* `str.isdigit`判断字符串是否全部由数字构成
* `str.isalnum`判断字符串是否仅包含字母和数字，而不含特殊字符

`split`分割`join`合并

`upper/lower/swapcase`大小写相关

`ljust/center/rjust`排版左中右对齐

`replace`替换子串

例子
```python
>>>'You are my sunshine.'.slipt(' ')
['You','are','my','sunshine.']
>>>'-'.join(["one","for","two"])
'One-for-two'
>>>'abc'.upper()
'ABC'
>>>'aBC'.lower()
'abc'
>>>'Abc'.swapcase()
'aBC"
>>>'Hello World!'.center(20)
'   Hello World!     '
>>>'Tom smiled,Tom cried,Tom shouted'.replace('Tom','Jane')
'Jane smiled,Jane cried,Jane shouted'
```