## gcc编译选项/g++编译选项
```cmake
CMAKE_C_FLAGS
CMAKE_CXX_FLAGS
```
指定版本
```cmake
# 在CMKE_C_FLAGS编译选项后加 -std=c++11
set( CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")
```
## 编译类型(Debug,Release)
* `CMAKE_BUILD_TYPE`
```cmake
# 设定编译类型为 debug
set(CMAKE_BUILD_TYPE Debug)
# 设定编译类型为 Release
set(CMAKE_BUILD_TYPE Release)
```
## 指的是工程编译发生的目录
* 关注的是构建输出目录
```cmake
CMAKE_BINARY_DIR
PROJECT_BINARY
<projectname>_SOURCE_DIR
```
## 引用当前源代码目录
```cmake
CMAKE_CURRENT_SOURCE_DIR
```
## 指的是工程顶层目录
```cmake
CMAKE_SOURCE_DIR
PROJECT_SOURCE_DIR
<projectname>_SOURCE_DIR
```
## 当前可执行文件或共享库所在的目录
```cmaek
ORIGIN
```
## 指定 c 编译器
```cmake
CMAKE_C_COMPILER
```
## 指定 c++ 编译器
```cmake
CMAKE_CXX_COMPILER
```
 ## 可执行文件输出的存放路径
```cmake
EXECUTABLE_OUTPUT_PATH
```
## 库文件输出的存放路径
```cmake
LIBRARY_OUTPUT_PATH
```
## 指定线程库的优选标志
```cmake
THREADS_PREFER_PTHREAD_FLAG
```
* 当该变量为 `TRUE` 时，CMake 将尽量使用 [[pthreads线程库]]
* 当该变量为 `FALSE` 时，CMake 则可能选择其他可用的线程库