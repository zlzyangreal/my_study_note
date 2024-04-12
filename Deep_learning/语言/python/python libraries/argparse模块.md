

介绍
----
`argparse` 是一个用来解析命令行参数的 `Python` 库，它是 `Python` 标准库的一部分。基于 `python 2.7` 的 `stdlib` 代码。

`argparse` 模块使编写用户友好的命令行界面变得容易。程序定义了所需的参数，而 `argparse` 将找出如何从 `sys.argv `（命令行）中解析这些参数。`argparse` 模块还会自动生成帮助和使用消息，并在用户为程序提供无效参数时发出错误。

使用示例
-------
***使用步骤***
1. 导入`argparse`包
2. 创建 `ArgumentParser()` 参数对象
3. 调用 `add_argument()` 方法往参数对象中添加参数
4. 使用 `parse_args()` 解析添加参数的参数对象，获得解析对象
5. 程序其他部分，当需要使用命令行参数时，使用解析对象.参数获取
```python
#未使用argparese模块
import math

def cal_vol(radius,height):
    vol = math.pi * pow(radius,2) * height
    return vol

if __name__=='__main__':
    print(cal_vol(2,4))
#########################################################
#使用
import math
# 1、导入argpase包
import argparse  

def parse_args():
# 2、创建参数对象
    parse = argparse.ArgumentParser(description='Calculate cylinder volume') 
 # 3、往参数对象添加参数 
    parse.add_argument('radius', type=int, help='Radius of Cylinder') 
    parse.add_argument('height', type=int, help='height of Cylinder')
# 4、解析参数对象获得解析对象
    args = parse.parse_args()  
    return args

def cal_vol(radius, height):
    vol = math.pi * pow(radius, 2) * height
    return vol

if __name__ == '__main__':
    args = parse_args()
# 5、使用解析对象.参数获取使用命令行参数
    print(cal_vol(args.radius, args.height))  
```
* 创建对象`ArgumentParser`
```python
    """Object for parsing command line strings into Python objects.

    Keyword Arguments:
        - prog -- The name of the program (default:
            ``os.path.basename(sys.argv[0])``)
        - usage -- A usage message (default: auto-generated from arguments)
        - description -- A description of what the program does
        - epilog -- Text following the argument descriptions
        - parents -- Parsers whose arguments should be copied into this one
        - formatter_class -- HelpFormatter class for printing help messages
        - prefix_chars -- Characters that prefix optional arguments
        - fromfile_prefix_chars -- Characters that prefix files containing
            additional arguments
        - argument_default -- The default value for all arguments
        - conflict_handler -- String indicating how to handle conflicts
        - add_help -- Add a -h/-help option
        - allow_abbrev -- Allow long options to be abbreviated unambiguously
        - exit_on_error -- Determines whether or not ArgumentParser exits with
            error info when an error occurs
    """
```
* 往对象添加参数`add_argument`
```python
ArgumentParser.add_argument(name or flags...[action][nargs][const][default][type][choices][required][help][matavar][dest])
```
* `name or flags` 选项字符串的名字或者列表，例如 foo 或者 -f, --foo
* `action` 命令行遇到参数时的动作，默认值是 store
    * `-store_const`，表示赋值为const
    * `–append`，将遇到的值存储成列表，也就是如果参数重复则会保存多个值;
    * `–append_const`，将参数规范中定义的一个值保存到一个列表
    * `–count`，存储遇到的次数；此外，也可以继承 `argparse.Action` 自定义参数解析
* `nargs` 应该读取的命令行参数个数
    * 可以是具体的数字，或者是?号，当不指定值时对于 `Positional argument` 使用 `default`，对于 `Optional argument` 使用 `const`
    * 或者是 * 号，表示 0 或多个参数
    * 或者是 + 号表示 1 或多个参数
* `const` `action` 和 `nargs` 所需要的常量值
* `default` 不指定参数时的默认值
* `type` 命令行参数应该被转换成的类型
* `choices` 参数可允许的值的一个容器
* `required` 可选参数是否可以省略 (仅针对可选参数)
* `help` 参数的帮助信息，当指定为 `argparse.SUPPRESS`时表示不显示该参数的帮助信息
* `matavar` 在 `usage` 说明中的参数名称，对于必选参数默认就是参数名称，对于可选参数默认是全大写的参数名称
* `dest` 解析后的参数名称，默认情况下，对于可选参数选取最长的名称，中划线转换为下划线