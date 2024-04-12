# 进程管理

ps （选项）
---------
查看目前目录，有哪些正在执行，以及执行状况

选项：
* -a(不加)  显示当前终端的所有进程信息    PID TTY TIME    CMD
* -u        以用户的格式显示进程信息    USER PID %CPU %MEM VSZ RSS TTY STAT START TIME COMMAND
* -x        显示后台进程运行的参数      PID TTY STAT TIME COMMAND
~~~
USER(UID)       用户名称
PID             进程号
PPID            父进程ID
C               CPU用于计算执行优先级的因子
%CPU            进程占用CPU百分比
%MEM            进程占用物理内存百分比
VSZ             进程占用的虚拟内存大小(单位KB)
RSS             进程占用的物理内存大小(单位KB) 
TT(TTY)         终端名称
STAT            进程状态
                    S-  睡眠
                    s-  表示该进程的会话是先导进程
                    N-  进程拥有比普通优先级更低的优先级
                    R-  正在运行
                    D-  短期等待
                    Z-  僵死进程
                    T-  被跟踪或者被停止
STARTED         进程启动时间
TIME            CPU时间(进程使用CPU总时间)
COMMAND(CMD)    启用进程所用的命令和参数(太长会被截断)
~~~
* -e            显示所有进程
* -f            全格式

kill （选项）（进程号）
------------------
通过进程号杀死/终止进程

**killall （进程名称）**

通过名称杀死进程，也支配通配符，这在系统负载过大而变得很慢时有用

选项：
* -9    表示强迫进程立刻停止

pstree （选项）
------------
树状展示进程

选项：
* -p    显示进程PID
* -u    显示进程的所属用户

service （服务名）（选项）
---------------------
服务管理

服务在  /etc/init.d/

选项：
* start     开始
* stop      停止
* restart   重启
* reload    重新加载
* status    查看

systemctl （选项）（服务名）
-----------------------

选项和service一样

服务在  /usr/lib/systemd/system

系列指令：
~~~
systemctl list-unit-files
查看服务开机启动状态
systemctl enable [服务名]
设置服务开机启动
systemctl disable [服务名]
关闭服务开机启动
systemctl is-enable [服务名]
查询服务是否自启动
~~~

top （选项）
----------
动态监视

选项：
* -d [秒数]     指定top命令每隔多少秒更新，默认3秒
* -i            使top不显示闲置或者僵死进程
* -p            通过指定监视进程id来仅仅监视某个进程的状态

交互操作：
* P             以CPU使用率排序
* M             以内存使用率排序
* N             以PID排序
* q             退出top

netstat （选项）
-------------
查看系统网络情况

选项：
* -an           按一定顺序排列输出
* -p            显示哪个进程在调用


## CPU监视

htop

## [GPU监视](Linux上GPU监视)
