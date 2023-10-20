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
