# CMake 工程构建
**一般采用外部构建**
* 将编译输出的文件放到不同的目录中
步骤
```linux
# 外部构建

# 1.创建 build 文件夹
mkdir build
# 2.进入文件夹,编译上级目录的CMakeLists.txt,生成Makefile和其他文件
cd build
make ..
# 3.执行make命令,生成target
make
```
例子,编写一个hello的cmake文件
```cmake
cmake_minimum_required(VERSION 3.0)

project(HELLOWORLD)

add_executable(hello hello.cpp)
```
接下来执行外部构建操作

例子,多级目录cmake文件
~~~
工程目录结构:
.
|-inc
| |-swap.h
|-main.cpp
|-src
  |-swap.cpp
~~~
```cmake
cmake_minimum_required(VERSION 3.0)

project(SWAP)

include_directories(inc)

add_executable(swap main.cpp src/swap.cpp)
```
接下来执行外部构造操作