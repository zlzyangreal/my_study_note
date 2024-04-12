>eg
```shell
if command -v ${CC} >/dev/null 2>&1; then  
:  
else  
echo "${CC} is not available"  
echo "Please set GCC_COMPILER for $TARGET_SOC"  
echo "such as export GCC_COMPILER=~/opt/arm-rockchip830-linux-uclibcgnueabihf/bin/arm-rockchip830-linux-uclibcgnueabihf"  
exit  
fi
```
* `command -v` 见[[shell系统函数]]
* `>/dev/null 2>&1`。这是一种常见的**重定向**语法，用于将命令的输出和错误都重定向到特殊设备 `/dev/null`，从而丢弃输出和错误信息
	* `>` 符号用于将命令的标准输出重定向到指定位置。
	- `/dev/null` 是一个特殊设备文件，它可以接受任何数据但不会保存和显
	- `2>&1` 表示将命令的标准错误（文件描述符2）重定向到与标准输出（文件描述符1）相同的位置。换句话说，将错误输出合并到标准输出中
-  检查 `${CC}` 所代表的命令是否存在（通过 `command -v ${CC}`）。
- 将命令的输出和错误都重定向到 `/dev/null`，即丢弃输出和错误信息。