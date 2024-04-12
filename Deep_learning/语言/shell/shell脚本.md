命令解释器，脚本
# 脚本头文件
```shell
#!/bin/bash
```
* 使用bash解释器
# [[shell语法]]
# [[shell变量]]
# [[shell运算符]]
# 读取控制台输入
```bash
read (选项)(参数)
```
* 选项和参数之间有空格
选项
* -p    指定读取时发送出的提示语句
* -t    指定读取值的等待时间(单位秒)
# [[shell系统函数]]
# [[shell重定向]]
# 自定义函数
例子
```shell
#!/bin/bash
function getsum(){
    SUM=$[$n1+$n2]
    echo "sum=$SUM"
}

read -p "input fist number" n1
read -p "input secend number" n2

getsum $n1 $n2
```