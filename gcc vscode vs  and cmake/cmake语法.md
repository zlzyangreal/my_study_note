# cmake语法

语法基本格式
------------
语法采用: `指令(参数1 参数2 ...)`
* 参数之间用空格分开
* 指令不区分大小写
* 变量用`${}`取值,在IF语句中直接用变量名

重要指令
--------
***指定最小cmake版本***

`cmake_minimum_required(VERSION versionNumber [FATAL_ERROR])`
* `versionNumber` 是版本号
* `FATAL_ERROR`是报错信息
```cmake
# CMake版本最小为2.8.3
cmake_minmum_required(VERSION 2.8.3)
```
***定义工程名称,并可指定工程支持的语言***

`project(projectname [CXX] [C] [Java])`
```cmake
# 工程名HELLO_WORD
project(HELLO_WORD)
```

***显式的定义变量***

`set(VAR [VALUE] [CACHE TYPE DOCSTRING [FORCE]])`
```cmake
# 设置SRC变量，其值为hello.cpp main.cpp
set(SRC hello.cpp main.cpp)
```
* SRC 变量通常用于存储源代码文件的列表

***向工程添加多个特定的头文件搜索路径***
* 相当于g++ `-I`参数

`include_directories(AFTER [BEFORE] [SYSTEM] dir1 dir2 ...)`
```cmake
# 将/usr/include/mylibfolder 和 ./lib 添加到头文件搜索路径
include_directories(/usr/include/mylibfolder ./lib)
```
***向工程添加多个特定的库文件搜索路径***
* 相当于g++ `-L`参数

`link_directories(dir1 dir2 ...)`
```cmake
link_directories(/usr/include/mylibfolder ./lib)
```

***生成库文件***

`add_library(libname [SHARED|STATIC|MODULE] [EXCLUDE_FROM_ALL] source1 source2 ...)`
```cmake
# 通过变量 SRC 生成 libhello.so 共享库
add_library(hello SHARED ${SRC})
```
* SHARED 动态库/ STATIC 静态库

***添加编译参数***

`add_complie_options(<option>...)`
```cmake
# 添加编译参数-wall -std=c++11
add_complie_options(-wall -std=c++11 -o2)
```
* -o2 是优化选项

***生成可执行文件***

`add_executable(exename source1 source2 ...)`
```cmake
# 编译 main.cpp 生成可执行文件 main
add_executable(main main.cpp)
```

***为目标添加链接的共享库***

`target_link_libraries(target library1<debug|optimized> libray2 ...)`
```cmake
# 将 hello 动态库文件链接到可执行文件 main
target_link_libraries(main hello)
```

***向当前工程添加存放源文件的子目录,并可以指定中间二进制和目标二进制存放的位置***

`add_subdirectory(source_dir [binary_dir] [EXCLUDE_FROM_ALL])`
```cmake
# 添加src子目录,src中需有一个CMakeLists.txt
add_subdirectory(src)
```
***发现目录下所有的源代码文件并将列表储存在一个变量中，这个指令临时被用来自动构建源文件列表***

`aux_source_directory(dir VARIABLE)`
```cmake
# 定义 SRC 变量,其值为当前目录下所有的源代码文件
aux_source_dirctory(. SRC)
# 编译 SRC 变量所代表的源文件代码,生成 main 可执行文件
add_executable(main ${SRC})
```

CMake 常用变量
--------------
* `CMAKE_C_FLAGS`,gcc编译选项
* `CMAKE_CXX_FLAGS`,g++编译选项
```cmake
# 在CMKE_C_FLAGS编译选项后加 -std=c++11
set( CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")
```
* `CMAKE_BUILD_TYPE`,编译类型(Debug,Release)
```cmake
# 设定编译类型为 debug
set(CMAKE_BUILD_TYPE Debug)
# 设定编译类型为 Release
set(CMAKE_BUILD_TYPE Release)
```
* `CMAKE_BINARY_DIR`,`PROJECT_BINARY`,`<projectname>_SOURCE_DIR`
    * 指的是工程编译发生的目录
* `CMAKE_SOURCE_DIR`,`PROJECT_SOURCE_DIR`,`<projectname>_SOURCE_DIR`
    * 指的是工程顶层目录
* `CMAKE_C_COMPILER`
    * 指定 c 编译器
* `CMAKE_CXX_COMPILER`
    * 指定 c++ 编译器
* `EXECUTABLE_OUTPUT_PATH`
    * 可执行文件输出的存放路径
* `LIBRARY_OUTPUT_PATH`
    * 库文件输出的存放路径