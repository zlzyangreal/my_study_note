[参考](https://blog.csdn.net/weixin_44796670/article/details/115900538)
## 1.[opencv官方网址](https://opencv.org/releases/)
## 2.[CCMake下载](ccmake.md)
## 3.下载依赖项
```bash
sudo apt-get install build-essential libgtk2.0-dev libgtk-3-dev libavcodec-dev libavformat-dev libjpeg-dev libswscale-dev libtiff5-dev
```
## 4.创建build文件先cmake，再ccmake编辑参数
```bash
OPENCV_GENERATE_PKGCONFIG = ON
```
## 5.编译
```bash
make -j4
```
## 6.安装make
```bash
sudo make install
```

## 7.环境配置
### 1.配置pkg-config环境
opencv4.pc文件的默认路径：/usr/local/lib/pkgconfig/opencv4.pc  
若此目录下没有，可以使用以下命令搜索：

```bash
sudo find / -iname opencv4.pc
```
将路径加入到PKG_CONFIG_PATH（用vim打开）：
```bash
sudo vim /etc/profile.d/pkgconfig.sh
```
在文件后面加入下面一行：
```shell
export PKG_CONFIG_PATH=/usr/local/lib/pkgconfig:$PKG_CONFIG_PATH
```
保存并退出后激活
激活
```bash
source /etc/profile
```
用以下命令验证是否成功：
```bash
pkg-config --libs opencv4
```
* 旧版本是一大堆链接库
* 新版本就是一个world
### 2 配置动态库环境
① 打开文件（可能为空文件）：
```bash
sudo vim /etc/ld.so.conf.d/opencv4.conf
```
② 在该文件末尾加上OpenCV的lib路径，保存退出：
```bash
/usr/local/lib
```
③ 使配置的路径生效：
```bash
sudo ldconfig
```
## 8.测试OpenCV
cd 到/opencv/samples/cpp/example_cmake目录下，依次执行以下命令：
```bash
cmake .
make
./opencv_example
```