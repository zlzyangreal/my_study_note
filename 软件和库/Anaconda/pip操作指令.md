## 下载
```bash
pip install xxx
```
## pip更新
```bash
pip install --upgrade pip
```
## pip安装txt文件
```bash
pip install -r requirements.txt
```
## pip删除包
```bash
pip uninstall package_name
```
## pip换源
临时源
```bash
#清华源 
pip install markdown -i https://pypi.tuna.tsinghua.edu.cn/simple 
# 阿里源 
pip install markdown -i https://mirrors.aliyun.com/pypi/simple/ 
# 腾讯源 
pip install markdown -i http://mirrors.cloud.tencent.com/pypi/simple 
# 豆瓣源 
pip install markdown -i http://pypi.douban.com/simple/
```
永久源
```bash
# 清华源 
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple 
# 阿里源 
pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/ 
# 腾讯源 
pip config set global.index-url http://mirrors.cloud.tencent.com/pypi/simple 
# 豆瓣源 
pip config set global.index-url http://pypi.douban.com/simple/
# 换回默认源
pip config unset global.index-url
```