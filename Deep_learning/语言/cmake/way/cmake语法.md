# 语法基本格式
语法采用: `指令(参数1 参数2 ...)`
* 参数之间用空格分开
* 指令不区分大小写
* 变量用`${}`取值,在IF语句中直接用变量名
# 重要指令
## 指定最小cmake版本

`cmake_minimum_required(VERSION versionNumber [FATAL_ERROR])`
* `versionNumber` 是版本号
* `FATAL_ERROR`是报错信息
```cmake
# CMake版本最小为2.8.3
cmake_minmum_required(VERSION 2.8.3)
```
## 定义工程名称,并可指定工程支持的语言
`project(projectname [CXX] [C] [Java])`
```cmake
# 工程名HELLO_WORD
project(HELLO_WORD)
```
## CMake 中用于输出信息
```cmake
message
# 输出一般消息。这将在构建过程中打印指定的文本
message("message text")

# 输出状态消息。这将在构建过程中打印指定的文本，并以状态消息的形式显示。
message(STATUS "message text")

# 输出警告消息。这将在构建过程中打印指定的文本，并以警告消息的形式显示。
message(WARNING "message text")

# 输出致命错误消息并终止构建。这将在构建过程中打印指定的文本，并以致命错误消息的形式显示。构建将在此处停止。
message(SEND_ERROR "message text")

# 输出详细信息。这将在构建过程中打印指定的文本，并以详细信息的形式显示。这些消息通常用于提供更详细的构建过程信息。
message(VERBOSE "message text")
```
## 显式的定义变量
`set(VAR [VALUE] [CACHE TYPE DOCSTRING [FORCE]])`
```cmake
# 设置SRC变量，其值为hello.cpp main.cpp
set(SRC hello.cpp main.cpp)
```
* SRC 变量通常用于存储源代码文件的列表
## 条件判断
 **1.比较两个字符串是否相等**
* `EQUAL` 或 `STREQUAL`
```cmake
if (variable1 STREQUAL variable2)
endif()
```
**2.比较两个字符串是否不相等**
* `NOT EQUAL` 或 `STRNEQUAL`
**3.用于比较两个字符串的字典顺序，左边的字符串是否小于右边的字符串**
* `LESS` 或 `STRLESS`
**4.用于比较两个字符串的字典顺序，左边的字符串是否大于右边的字符串**
* `GREATER` 或 `STRGREATER`
**5.用于比较两个字符串的字典顺序，左边的字符串是否小于或等于右边的字符串**
* `LESS_EQUAL` 或 `STRLESS_EQUAL`
**6.用于比较两个字符串的字典顺序，左边的字符串是否大于或等于右边的字符串**
* `GREATER_EQUAL` 或 `STRGREATER_EQUA`
## 向工程添加多个特定的头文件搜索路径
* 相当于g++ `-I`参数

`include_directories(AFTER [BEFORE] [SYSTEM] dir1 dir2 ...)`
```cmake
# 将/usr/include/mylibfolder 和 ./lib 添加到头文件搜索路径
include_directories(/usr/include/mylibfolder ./lib)
```
## 向工程添加多个特定的库文件搜索路径
* 相当于g++ `-L`参数

`link_directories(dir1 dir2 ...)`
```cmake
link_directories(/usr/include/mylibfolder ./lib)
```

## 向编译器添加定义
```cmake
add_definitions(-DRKNPU1)
```
* 向 C/C++ 编译器添加预定义的宏定义，DRKNPU1
## 向当前工程添加存放源文件的子目录,并可以指定中间二进制和目标二进制存放的位置

`add_subdirectory(source_dir [binary_dir] [EXCLUDE_FROM_ALL])`
```cmake
# 添加src子目录,src中需有一个CMakeLists.txt
add_subdirectory(src)
```
## 将符合指定模式的文件列表存储到变量中
```cmake
file(GLOB SRCS ${CMAKE_CURRENT_SOURCE_DIR}/*.cc)
```
- `file`：CMake 命令，用于操作文件和目录。
- `GLOB`：`file` 命令的子命令，用于匹配文件。
- `SRCS`：存储匹配到的文件列表的变量名。
- `${CMAKE_CURRENT_SOURCE_DIR}`：表示当前处理的 CMakeLists.txt 文件所在的目录的绝对路径。
- `/*.cc`：文件匹配模式，这里表示匹配以 `.cc` 为后缀的所有文件。
## 查找和引入外部依赖项
```cmake
find_package
# eg
find_package(Threads REQUIRED)
```
*  `Threads` 查找系统中可用的线程库
* `REQUIRED` 必须项
## 生成库文件

`add_library(libname [SHARED|STATIC|MODULE] [EXCLUDE_FROM_ALL] source1 source2 ...)`
```cmake
# 通过变量 SRC 生成 libhello.so 共享库
add_library(hello SHARED ${SRC})
```
* SHARED 动态库/ STATIC 静态库

## 添加编译参数

`add_complie_options(<option>...)`
```cmake
# 添加编译参数-wall -std=c++11
add_complie_options(-wall -std=c++11 -o2)
```
* -o2 是优化选项

## 生成可执行文件

`add_executable(exename source1 source2 ...)`
```cmake
# 编译 main.cpp 生成可执行文件 main
add_executable(main main.cpp)
```

## 为目标添加链接的共享库

`target_link_libraries(target library1<debug|optimized> libray2 ...)`
```cmake
# 将 hello 动态库文件链接到可执行文件 main
target_link_libraries(main hello)
```
## 发现目录下所有的源代码文件并将列表储存在一个变量中，这个指令临时被用来自动构建源文件列表

`aux_source_directory(dir VARIABLE)`
```cmake
# 定义 SRC 变量,其值为当前目录下所有的源代码文件
aux_source_dirctory(. SRC)
# 编译 SRC 变量所代表的源文件代码,生成 main 可执行文件
add_executable(main ${SRC})
```
## 设置目标的头文件包含路径
```cmake
target_include_directories
# eg
target_include_directories(${PROJECT_NAME} PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}
)
```
* `PRIVATE` 私有
* `CMAKE_CURRENT_SOURCE_DIR` 见 [[cmake常用变量]]
## 定义安装规则
以便在构建项目后将生成的文件安装到指定的目标位置
```cmake
install
# eg
install(TARGETS ${PROJECT_NAME} DESTINATION .)
```
- `FILES`：指定要安装的文件列表。
- `DIRECTORY`：指定要安装的目录及其内容。
- `DESTINATION`：指定安装目标的路径。
- `PERMISSIONS`：指定安装文件的访问权限。
- `COMPONENT`：指定安装组件的名称。
- `OPTIONAL`：指定安装文件或目录是可选的。
- `TARGETS` 选项指定要安装的目标类型为可执行目标或库目标