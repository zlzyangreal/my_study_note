## 返回文件名/文件路径
### 返回文件名
```shell
basename
```
### 返回文件路径
```shell
dirname
```
* 返回其父目录的绝对路径
eg
```shell
       dname=`dirname "$demo_path"`
       name=`basename $dname`
       echo "$name"
```
## 查找并打印出指定命令的完整路径
```shell
command -v
```
## 脚本执行过程中遇到错误时立即退出
```shell
set -e
```
## 停止脚本
```shell
exit
```
## 解析命令行选项和参数
Shell内置命令
```shell
getopts
```
eg
```shell
while getopts ":t:a:d:b:m" opt; do
done
```
- `getopts`：解析命令行选项和参数的命令
- `":t:a:d:b:m"`：这是一个包含所有可接受选项的字符串。每个字母代表一个选项，如果选项后面带有冒号`:`，表示该选项需要接受一个参数
- `opt`：这是一个变量，用于存储当前解析到的选项的字母
- `do`：表示循环开始的代码块
## 导出环境变量
**export**
```shell
GCC_COMPILER=aarch64-linux-gnu
export CC=${GCC_COMPILER}-gcc
export CXX=${GCC_COMPILER}-g++
```
* 使用`export`命令导出的环境变量只在当前Shell会话中有效。
* 如果要使其永久生效，可以将`export`命令放入Shell的配置文件（例如`.bashrc`或`.bash_profile`），这样每次启动Shell时都会自动导出这些变量。
## 查询指令
```shell
find
```
eg
```shell
BUILD_DEMO_NAME=yolov8
for demo_path in `find examples -name ${BUILD_DEMO_NAME}`
do
    if [ -d "$demo_path/cpp" ]
    then
        BUILD_DEMO_PATH="$demo_path/cpp"
        break;
    fi
done
```
* 是在` examples 目录`及其子目录中查找名称为 ${BUILD_DEMO_NAME} 的文件或目录
## 将未匹配到文件的通配符表达式扩展为空列表
```shell
shopt -s nullglob
```
