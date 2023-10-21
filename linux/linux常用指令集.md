# 常用指令集

## 关机重启
shutdown -h now [立刻关机]

shutdown -r 1   [一分钟后重启]

halt [关机]

reboot [重启]

sync [保存数据到磁盘（建议关机前使用）]

clear[清理当前页面]

## 用户管理
### 用户添加
useradd zlzyang[添加用户zlzyang(默认目录，在home下创建)]

useradd -d /home/text zlzyang[指定目录]
### 修改密码
passwd zlzyang
### 用户删除
userdel zlzyang[用户删除但保留家目录]

userdel -r zlzyang[完全删除]
### 用户查询
id zlzyang
### 用户切换
su -zlzyang [切换账户到zlzyang]
### 查看当前用户信息
whoami[显示登录用户，显示登录ip时间信息]
### 用户组
在创建用户没有指定组，会创建一个新同名新组
#### 添加组
groupadd zlzyang[添加组zlzyang]
#### 删除组
groupdel zlzyang[删除组zlzyang]
#### 添加用户直接带组
useradd -g zlzyang zlzyanggroup[添加用户zlzyang到组zlzyanggruop中]
#### 修改用户的组
usermod -g zlzyang zlzyangt[将zlzyang切换到zlzyangt组]
### 用户和组相关文件
#### /etc/passwd文件
用户的配置文件，记录用户的各种信息
#### /etc/shadow
口令配置文件
#### /etc/group 文件
组的配置文件，记录Linux包含组的信息
## 用户级别
指令init 5[切换到级别5]

## 帮助指令
man [命令或配置文件]  (功能描述:获得帮助信息)

help [命令] (功能描述:获得shell内置命令的帮助信息)
## 文件目录
### pwd 
显示当前工作目录的绝对路径

### ls [选项][目录或者文件]
信息查看

选项：

-a 显示当前目录所有的文件和目录，包括隐藏的

-l 以列表的方式显示信息

### cd [参数]
切换目录

cd ~ 返回家目录

cd .. 返回上一级

### mkdir [选项][目录]
创建目录

选项：

-p 创建多级目录(默认只能创建一级)

### rmdir [选项][要删除的空目录]
删除指定空目录

rm -rf [目录]

删除非空目录

### touch [文件名]
创建空文件

### cp [选项][拷贝对象][目标位置]

-r 递归复制整个文件夹

\cp -r [拷贝对象][目标位置]

强制不提醒

## rm [选项][文件或者目录]
移除文件或者目录

-r  递归删除整个文件夹

-f  强制删除不提醒
## mv [老目录文件][新目录文件]

同目录下叫重命名，不同叫剪切移植

## cat [选项][文件]
查看文件

-n  显示行号
## more [文件]
全屏幕方式按页面显示文本文件内容
## less [文件]
查看大型文件
## echo [选项][输出内容]
输出内容到控制台
## head [指令][文件]
查看文件开头部分

head -n 5 [文件]  查看文件前5行
## tail [指令][文件]
查看文件结尾部分

tail -f [文件]
实时追踪该文档所有的更新
## >指令和>>指令
ls -l>文件

列表内容写到文件中(覆盖)

ls -al>>文件

列表的内容追加到文件末尾

cat 文件1>文件2

将文件1内容覆盖到文件2

echo "内容">>文件(追加)
## ln -s [原文件或目录][软链接]
给原文件添加软链接
## history
查看历史执行语句(在后面加数值限定查看)

!2执行历史第二条语句
## 时间日期类
### date [具体]
显示当前日期

date "%Y-%m-%d-%H-%M-%S"  年月日时分秒

### date -s [字符串时间]
设置日期

date -s "2023-10-21 9:08:1"
## cal
查看日历

cal 2023  查看2023日历
