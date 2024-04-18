## 1.[官网](https://www.fftw.org/download.html)
## 2.安装
**在VS里面输入指令**
```bash
 lib /machine:x64 /def:libfftw3f-3.def
 lib /machine:x64 /def:libfftw3-3.def
 lib /machine:x64 /def:libfftw3l-3.def
```
![[FFTW1.png]]
## 3.老三样(过程参考[[SFML库配置]])
1. 移动 `dll`文件
2. 包含头文件
3. 链接lib
4. 加配置(附加依赖项lib)