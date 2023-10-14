# 常用指令集

## 关机重启
shutdown -h now [立刻关机]

shutdown -r 1   [一分钟后重启]

halt [关机]

reboot [重启]

sync [保存数据到磁盘（建议关机前使用）]

## 用户切换
su -zlzyang [切换账户到zlzyang]
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
### 查看当前用户信息
whoami[显示登录用户，显示登录ip时间信息]
