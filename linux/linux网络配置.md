# Linux网络配置

ifconfig
--------
查看网络配置

ping [目的主机]
--------------
测试连通性

静态ip
------
[ip文件各系统有些许不同]

centOS：
* /etc/sysconfig/network-scripts/ifcfg-ens33(文件位置)
~~~
文件说明：
    DEVICE    = ens33                                  #接口名
    HWADDR    = 00:0C:2x:6x:0x:xx                      #MAC地址(未查到此参数)
    TYPE      = Ethernet                               #网络类型(通常是Ethernet)
    UUID      = "6e9f1b7e-4da5-404c-bd9b-5605f8eb58f2" #随机id
    ONBOOT    = "yes"                                  #系统启动时是否有效
    BOOTPROTO = "dhcp"                                 #ip的配置方法[none|sttic|bootp|dhcp](引导时不使用协议|静态分配ip|BOOTP协议|DHCP协议)
    IPADDR    = [自定义ip]                             #ip地址(自配置参数)
    GATEWAY   = [网关ip]                               #网关ip(自配置参数)
    DNS1      = [域名解析器]                           #域名解析器ip(自配置参数)
~~~
* service network restart 或者 reboot 生效配置

raspberrypi:
* /etc/dhcpcd.conf
~~~
添加：
interface wlan0  #网卡名
inform 192.168.2.218/24    #树莓派IP
static routers=192.168.2.1  #路由器IP
static domain_name_servers=192.168.2.1  #DNS，这里也是路由器IP
有线网卡：
interface eth0
static ip_address=192.168.2.219/24
static routers=192.168.2.1
static domain_name_servers=192.168.2.1
~~~

设置host映射
------------
通过主机名找到主机

* /etc/hosts

* 添加  [ip][名字]