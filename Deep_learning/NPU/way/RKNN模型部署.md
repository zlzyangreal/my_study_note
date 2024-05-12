   这里还是用的野火，版本1.5.0
## 1.库
```bash
# 工程
git clone https://gitee.com/LubanCat/lubancat_ai_manual_code.git
```
## 2.修改Cmake文件
```cmake
# 需要移动的图片和label
install(FILES ${CMAKE_CURRENT_SOURCE_DIR}/../model/16.jpg DESTINATION model)
install(FILES ${CMAKE_CURRENT_SOURCE_DIR}/../model/fire.txt DESTINATION model)
```
## 3.修改C++文件
在`postprocess.h`里面有类别总类
```cpp
OBJ_CLASS_NUM 1
```
## 3.运行shell文件
## 4.运行demo
demo 在 cpp 下面的 install
```bash
./demo <模型><图片>
```