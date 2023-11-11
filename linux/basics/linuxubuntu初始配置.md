# ubuntu初始配置

设定root密码
------------
sudo passwd

exit 退出

APT软件管理
-----------
~~~
* sudo apt-get update                           更新源
* sudo apt-get install [package]                安装包
* sudo apt-get remove [package]                 删除包

  sudo apt-cache search [package]               搜索软件包
* sudo apt-cache show [package]                 获取包的相关信息、如说明、大小、版本等
  sudo apt-get install [package] --reinstall    重新安装包

  sudo apt-get -f install                       修复安装
  sudo apt-get remove [package] --purge         删除包，包括配置文件等
  sudo apt-get bulid-dep [package]              安装相关的编译环境

  sudo apt-get upgrade                          更新已安装的包
  sudo apt-get dist-upgrade                     升级系统
  sudo apt-cache depends [package]              了解使用该包依赖哪些包
  sudo apt-cache rdepends [package]             查看该包被哪些包依赖
* sudo apt-get source [package]                 下载该包的源代码
~~~

换源
----
***查源***
* 目前清华最好用
* 清华源：https://mirrors.tuna.tsinghua.edu.cn/

***备份***
sudo cp /etc/apt/sources.list /etc/apt/sources.list.backup
* /etc/apt/sources.list源位置

***更新***
* 清空 echo '' > /etc/apt/sources.list
* 拷贝

SSH远程登录
----------
***安装SSH***

sudo apt-get install openssh-server

***激活***

service sshd restart

***确定***

netstat -anp