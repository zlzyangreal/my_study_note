1.启动系统，进入开机界面，在界面按"e"进入编辑页面

(以CentOS为例)指示码:CentOS Linux (3.10.0-862.e17.86_64)(Core)

2.找到linux16开头行，输入init=/bin/sh

3.Ctrl+x进入单用户模式

4.输入mount -o remount,rw/

5.输入passwd  回车后输入密码

6.输入touth /.autorelabel

7.输入exec /sbin/init
