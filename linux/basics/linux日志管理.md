# 日志管理

``/var/log/``系统日志保存位置

系统日志
-------
* ``boot.log``      系统启动日志
* ``corn``[未发现]  记录与系统定时任务相关日志
* ``cups/``         记录打印信息的日志
* ``dmesg``         记录了系统在开机时内核自检的信总，**也可以用dmesg指令直接查看**
* ``btmp``          记录了错误登录的日志。**文件是二进制文件，不能vi查看，要使用lastb**
* ``lastlog``       记录了用户最后一次的登录时间日志。**二进制文件，使用lastlog**
* ``mail..``        记录邮件信息日志
* ``message``       记录文件重要消息的日志，这个日志文件中会记录Linux系统中绝大多数重要信息。**如果系统出现问题，首先要检查的就是这个文件**
* ``secure``[未发现] 记录验证和授权方面的信息，只要涉及账户和秘密的程序都会记录
* ``wtmp``          永久记录所有用户登录、注销信息，同时记录系统的启动、重启、关机事件。**二进制文件，last查看**
* ``ulmp``          记录当前已经登录的用户信息。文件会随用户的登录和注销而不断变化。不能用vi查看，只能w who users查看

rsyslogd
-----------
日志管理服务
* 查询服务是否启动``ps aux | grep "rsyslogd" | grep -v "grep"``
* 查询服务自启动状态``sysremctl list-unit-files | grep rsyslog``

日志分类
-------
日志类型
~~~
auth                        pam产生的日志
authpriv                    ssh ftp等登录信息的验证信息
corn                        时间任务相关
kern                        内核
lpr                         打印
mail                        邮件
mark(syslog)-rsyslog        服务内部的信息，事件标识
news                        新闻组
user                        用户程序产生的相关信息
uucp                        unix to nuix copy主机之间相关通信
local [1-7]                 自定义日志设置
~~~

日志级别
-------
从上到下，从低到高
~~~
debug                       有调试信息的，日志通信最多
info                        一般信息日志，最常用
warning                     警告级别
err                         错误级别，阻止某个功能或者模块不能正常工作的信息
crit                        严重级别，阻止整个系统或整个软件不能正常工作的信息
alert                       需要立刻修改的信息
emerg                       内核严重崩溃等重要信息
none                        什么都不记录
~~~

日志格式
-------
* 事件产生的时间
* 产生事件服务器的主机名
* 产生事件服务名或程序名
* 事件的具体信息

logrotate 文件配置参数
---------------------
~~~
daily                       日志的轮替周期是每天
weekly                      日志的轮替周期是每周
monthly                     日志的轮替周期是每月
rotate [数值]               保留的日志文件的个数。0指没有备份
compress                    日志轮替时，旧的日志进行压缩
create mode owner group     建立新日志，同时制定新日志的权限与所有者和所属组
mail address                当日志轮替时，输出内容通过邮件发送到指定的邮件位置
missingok                   如果日志不存在，则忽略该日志的警告信息
notifempty                  如果日志为空文件，则不进行日志轮换
minsize [数值]              日志轮换的最小值。也就是日志要达到这个最小值才会轮换，否则到时间也不轮换
size [大小]                 日志只有大于指定大小才进行日志轮替，而不是按时间
dareext                     使用日期作为日志轮替文件的后缀
sharedscripts               在此关键字之后的脚本只执行一次
prerotate/endscript         在此日志轮替之前执行脚本命令
postrotate/endscript        在此日志轮替之后执行脚本命令
~~~

查看日志内存
-----------
~~~
journalctl                                      可以查看内存日志[查看全部]
journalctl -n -3                                查看最近新3条
journalctl --since 19:00 --until 19:10:10       查看起始时间到结束时间的日志[可加日期]
journalctl -p err                               报错日志
journalctl -o verbose                           日志详细内容
journalctl——PID=1245 _COMM=sshd                 查看包含这些参数的日志
~~~
journalctl是内存日志，重启清空