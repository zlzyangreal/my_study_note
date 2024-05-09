## 1.先更新
## 2.下载依赖项
```bash
sudo apt install -y build-essential zlib1g-dev \
libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libsqlite3-dev \
libreadline-dev libffi-dev curl libbz2-dev
```
## 2.[下载包](https://www.python.org/ftp/python/3.9.10/Python-3.9.10.tgz)
## 3.解压
```bash
tar xvf Python-3.9.10.tgz
```
## 4.配置(这里是教程配置，具体配置可能会修改部分)
```bash
./configure --enable-optimizations
```
## 5.编译
```bash
make -j4
```
## 6.安装
```bash
sudo make install
```
## 7.修改软连接
查看当前软链接指向的python版本
```bash
ls /usr/bin/python -l
```
删除原来的
```bash
sudo rm -f /usr/bin/python 
```
在/usr/bin/目录创建软连接 python，定向/usr/local/bin/python3.9
```bash
sudo ln -s /usr/local/bin/python3.9 /usr/bin/python
```
检查版本
```bash
python --version
```