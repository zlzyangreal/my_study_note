## 脚本输出
```shell
echo "输出内容"
```
## 注释
```shell
#单行注释
```
条件判断
-------
语法

```shell
if [ 条件判断语句 ]
then
代码
elif [ 条件判断语句 ]
代码
fi
```
* 非空返回ture
* 空返回false
* 条件判断语句两边要有空格

判断条件
~~~
字符串比较
=   

整数比较
-lt     小于
-le     小于等于
-eq     等于
-gt     大于
-ge     大于等于
-ne     不等于

文件权限判断
-r      读权限
-w      写权限
-x      执行权限

文件类型判断
-f      文件存在并且是一个常规文件
-e      文件存在
-d      文件存在并是一个目录

-z      用于测试字符串是否为空或长度为零
-n      检查给定变量是否非空
~~~
## case语句

语法
```shell
case $变量名 in
"值1")
代码
;;
"值2")
代码
;;
*)
代码
;;
esac
```

for循环
------
语法
```shell
for 变量 in 值1 值2...
do
代码
done

for((初始值;循环控制条件;变量变换))
do
代码
done
```

while循环
--------
```shell
while [ 条件判断语句 ]
do
代码
done
```