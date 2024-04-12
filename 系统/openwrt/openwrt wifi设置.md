# openwrt wifi设置

查看网卡类型
-----------
网络->无线
*  `radio0` 表示无线设备物理编号，插入多个无线网卡时就会显示多个无线设备

Master模式
-----------
Master模式也被称为接入点AP模式，是Wireless Access Point的简称，中文名称：无线接入点。 AP相当于一个连接有线网和无线网的桥梁，其主要作用是将各个无线网络客户端连接到一起，然后将无线网络接入以太网。

通俗讲，就是将连入互联网的有线网络扩展为无线网络，以供手机等无线设备连接到互联网中。

在OpenWrt中配置AP模式十分简单，只需要几步就能完成。

配置失败恢复默认无线
-------------------
```
rm /root/.init/WLAN
reboot
```

Client 模式
-----------
https://doc.embedfire.com/openwrt/user_manal/zh/latest/User_Manual/openwrt/wifi.html