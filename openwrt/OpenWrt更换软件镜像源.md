# OpenWrt 换源

更换方法
--------
系统->软件包

配置opkg

修改/etc/opkg/distfeeds.conf 文件

国内源
------
***中科大OpenWrt源***
```
src/gz openwrt_core https://mirrors.ustc.edu.cn/openwrt/releases/21.02.0/targets/rockchip/armv8/packages
src/gz openwrt_base https://mirrors.ustc.edu.cn/openwrt/releases/21.02.0/packages/aarch64_generic/base
src/gz openwrt_luci https://mirrors.ustc.edu.cn/openwrt/releases/21.02.0/packages/aarch64_generic/luci
src/gz openwrt_packages https://mirrors.ustc.edu.cn/openwrt/releases/21.02.0/packages/aarch64_generic/packages
src/gz openwrt_routing https://mirrors.ustc.edu.cn/openwrt/releases/21.02.0/packages/aarch64_generic/routing
src/gz openwrt_telephony https://mirrors.ustc.edu.cn/openwrt/releases/21.02.0/packages/aarch64_generic/telephony
```
资料  http://mirrors.ustc.edu.cn/help/openwrt.html

***清华OpenWrt源***
```
src/gz openwrt_core https://mirrors.tuna.tsinghua.edu.cn/openwrt/releases/21.02.0/targets/rockchip/armv8/packages
src/gz openwrt_base https://mirrors.tuna.tsinghua.edu.cn/openwrt/releases/21.02.0/packages/aarch64_generic/base
src/gz openwrt_luci https://mirrors.tuna.tsinghua.edu.cn/openwrt/releases/21.02.0/packages/aarch64_generic/luci
src/gz openwrt_packages https://mirrors.tuna.tsinghua.edu.cn/openwrt/releases/21.02.0/packages/aarch64_generic/packages
src/gz openwrt_routing https://mirrors.tuna.tsinghua.edu.cn/openwrt/releases/21.02.0/packages/aarch64_generic/routing
src/gz openwrt_telephony https://mirrors.tuna.tsinghua.edu.cn/openwrt/releases/21.02.0/packages/aarch64_generic/telephony
```
资料  https://mirrors.tuna.tsinghua.edu.cn/help/openwrt/

***OpenWrt官方源***
```
src/gz openwrt_core https://downloads.openwrt.org/releases/21.02.0/targets/rockchip/armv8/packages
src/gz openwrt_base https://downloads.openwrt.org/releases/21.02.0/packages/aarch64_generic/base
src/gz openwrt_luci https://downloads.openwrt.org/releases/21.02.0/packages/aarch64_generic/luci
src/gz openwrt_packages https://downloads.openwrt.org/releases/21.02.0/packages/aarch64_generic/packages
src/gz openwrt_routing https://downloads.openwrt.org/releases/21.02.0/packages/aarch64_generic/routing
src/gz openwrt_telephony https://downloads.openwrt.org/releases/21.02.0/packages/aarch64_generic/telephony
```