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

netstat [选项]
--------------
用于显示网络状态

* -a或--all 显示所有连线中的Socket。
* -A<网络类型>或--<网络类型> 列出该网络类型连线中的相关地址。
* -c或--continuous 持续列出网络状态。
* -C或--cache 显示路由器配置的快取信息。
* -e或--extend 显示网络其他相关信息。
* -F或--fib 显示路由缓存。
* -g或--groups 显示多重广播功能群组组员名单。
* -h或--help 在线帮助。
* -i或--interfaces 显示网络界面信息表单。
* -l或--listening 显示监控中的服务器的Socket。
* -M或--masquerade 显示伪装的网络连线。
* -n或--numeric 直接使用IP地址，而不通过域名服务器。
* -N或--netlink或--symbolic 显示网络硬件外围设备的符号连接名称。
* -o或--timers 显示计时器。
* -p或--programs 显示正在使用Socket的程序识别码和程序名称。
* -r或--route 显示Routing Table。
* -s或--statistics 显示网络工作信息统计表。
* -t或--tcp 显示TCP传输协议的连线状况。
* -u或--udp 显示UDP传输协议的连线状况。
* -v或--verbose 显示指令执行过程。
* -V或--version 显示版本信息。
* -w或--raw 显示RAW传输协议的连线状况。
* -x或--unix 此参数的效果和指定"-A unix"参数相同。
* --ip或--inet 此参数的效果和指定"-A inet"参数相同。